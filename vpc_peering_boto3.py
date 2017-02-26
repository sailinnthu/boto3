VPC Peering in boto3 

import boto3
ec2 = boto3.resource('ec2', region_name="ap-southeast-2")
ec2_client = boto3.client('ec2', region_name="ap-southeast-2")

# create first_vpc
first_vpc = ec2.create_vpc(CidrBlock='10.10.0.0/16')
first_vpc.modify_attribute(EnableDnsSupport={'Value':True})
first_vpc.modify_attribute(EnableDnsHostnames={'Value':True})

# create second_vpc
second_vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
second_vpc.modify_attribute(EnableDnsSupport={'Value':True})
second_vpc.modify_attribute(EnableDnsHostnames={'Value':True})

# tag first_vpc 
first_vpc.create_tags(Tags=[{'Key':'Name','Value':'first_vpc'}])
# tag second_vpc 
second_vpc.create_tags(Tags=[{'Key':'Name','Value':'second_vpc'}])

# create Public Subnet & Private Subnet in first_vpc 
subnet1 = first_vpc.create_subnet(CidrBlock='10.10.1.0/24',AvailabilityZone='ap-southeast-2a')
subnet1.meta.client.modify_subnet_attribute(SubnetId=subnet1.id, MapPublicIpOnLaunch={"Value": True})
subnet2 = first_vpc.create_subnet(CidrBlock='10.10.2.0/24',AvailabilityZone='ap-southeast-2b')

# create Public Subnet & Private Subnet in second_vpc 
subnet3 = second_vpc.create_subnet(CidrBlock='192.168.1.0/24',AvailabilityZone='ap-southeast-2a')
subnet3.meta.client.modify_subnet_attribute(SubnetId=subnet3.id, MapPublicIpOnLaunch={"Value": True})
subnet4 = second_vpc.create_subnet(CidrBlock='192.168.2.0/24',AvailabilityZone='ap-southeast-2b')

# create tag for subnets in first_vpc
subnet1_tag=[subnet1.id]
subnet2_tag=[subnet2.id]
ec2_client.create_tags(Resources=subnet1_tag,Tags=[{'Key':'Name','Value':'vpc1_public_subnet'}])
ec2_client.create_tags(Resources=subnet2_tag,Tags=[{'Key':'Name','Value':'vpc1_private_subnet'}])
# create tag for subnets in second_vpc
subnet3_tag=[subnet3.id]
subnet4_tag=[subnet4.id]
ec2_client.create_tags(Resources=subnet3_tag,Tags=[{'Key':'Name','Value':'vpc2_public_subnet'}])
ec2_client.create_tags(Resources=subnet4_tag,Tags=[{'Key':'Name','Value':'vpc2_private_subnet'}])

# create Internet Gateway and attach to first_vpc
igw1 = ec2.create_internet_gateway()
igw1.attach_to_vpc(VpcId=first_vpc.id)

# create Internet Gateway and attach to second_vpc
igw2 = ec2.create_internet_gateway()
igw2.attach_to_vpc(VpcId=second_vpc.id)

# create tag for Internet Gateways
igw1_tag=[igw1.id]
igw2_tag=[igw2.id]
ec2_client.create_tags(Resources=igw1_tag,Tags=[{'Key':'Name','Value':'vpc1_igw'}])
ec2_client.create_tags(Resources=igw2_tag,Tags=[{'Key':'Name','Value':'vpc2_igw'}])

# Query RouteTableId for first_vpc
vpc1_public_route_table = list(first_vpc.route_tables.all())[0]
# add a default route, for Public Subnet, pointing to Internet Gateway for first_vpc
ec2_client.create_route(RouteTableId=vpc1_public_route_table.id,DestinationCidrBlock='0.0.0.0/0',GatewayId=igw1.id)
vpc1_public_route_table.associate_with_subnet(SubnetId=subnet1.id)

# Query RouteTableId for second_vpc
vpc2_public_route_table = list(second_vpc.route_tables.all())[0]
# add a default route, for Public Subnet, pointing to Internet Gateway for second_vpc
ec2_client.create_route(RouteTableId=vpc2_public_route_table.id,DestinationCidrBlock='0.0.0.0/0',GatewayId=igw2.id)
vpc2_public_route_table.associate_with_subnet(SubnetId=subnet3.id)

# create tag for Public Route Tables
vpc1_public_route_table_tag=[vpc1_public_route_table.id]
vpc2_public_route_table_tag=[vpc2_public_route_table.id]
ec2_client.create_tags(Resources=vpc1_public_route_table_tag,Tags=[{'Key':'Name','Value':'vpc1_public_routes'}])
ec2_client.create_tags(Resources=vpc2_public_route_table_tag,Tags=[{'Key':'Name','Value':'vpc2_public_routes'}])

# create a route table for Private Subnet of first_vpc
vpc1_private_route_table = ec2.create_route_table(VpcId=first_vpc.id)
vpc1_private_route_table.associate_with_subnet(SubnetId=subnet2.id)

# create a route table for Private Subnet of second_vpc
vpc2_private_route_table = ec2.create_route_table(VpcId=second_vpc.id)
vpc2_private_route_table.associate_with_subnet(SubnetId=subnet4.id)

# create tag for Public Route Tables
vpc1_private_route_table_tag=[vpc1_private_route_table.id]
vpc2_private_route_table_tag=[vpc2_private_route_table.id]
ec2_client.create_tags(Resources=vpc1_private_route_table_tag,Tags=[{'Key':'Name','Value':'vpc1_private_routes'}])
ec2_client.create_tags(Resources=vpc2_private_route_table_tag,Tags=[{'Key':'Name','Value':'vpc2_private_routes'}])

# Create vpc peering between first_vpc and second_vpc
vpc1_to_vpc2_peering = ec2.create_vpc_peering_connection(
    VpcId=first_vpc.id,
    PeerVpcId=second_vpc.id,
)
# Accept vpc peering request
vpc1_to_vpc2_peering.accept()

# create tag for vpc peering
vpc1_to_vpc2_tag=[vpc1_to_vpc2_peering.id]
ec2_client.create_tags(Resources=vpc1_to_vpc2_tag,Tags=[{'Key':'Name','Value':'vpc1_to_vpc2'}])

# create routes to connect between 10.10.2.0/24 and 192.168.2.0/24 via VPC Peering Link
ec2_client.create_route(RouteTableId=vpc1_private_route_table.id,DestinationCidrBlock='192.168.2.0/24',VpcPeeringConnectionId=vpc1_to_vpc2_peering.id)
ec2_client.create_route(RouteTableId=vpc2_private_route_table.id,DestinationCidrBlock='10.10.2.0/24',VpcPeeringConnectionId=vpc1_to_vpc2_peering.id)

# create a security group called "vpc1_public_sg" for Public Subnet of first_vpc
vpc1_security_group1 = ec2.create_security_group(GroupName='vpc1_public_sg',Description='vpc1_public_sg',VpcId=first_vpc.id)
vpc1_security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
vpc1_security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=80,ToPort=80)
vpc1_security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=443,ToPort=443)
vpc1_security_group1.authorize_ingress(CidrIp='10.10.2.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)

vpc1_security_group1_tag=[vpc1_security_group1.id]
ec2_client.create_tags(Resources=vpc1_security_group1_tag,Tags=[{'Key':'Name','Value':'vpc1_public_sg'}])

# Launch an instance in vpc1's public subnet
vpc1_public_instance1 = subnet1.create_instances(
	ImageId='ami-1c47407f',
	MinCount=1,
	MaxCount=1,
	KeyName='vcloudynet-au',
	InstanceType='t2.micro',
	SecurityGroupIds=[ vpc1_security_group1.id ]
	#NetworkInterfaces=[{'NetworkInterfaceId': network_interface.id,'DeviceIndex':0}]
)

# Retrive vpc1_public_instance1's id and Tag it
vpc1_public_instance1 = list(vpc1_public_instance1)[0]
ec2_client.create_tags(Resources=[vpc1_public_instance1.id],Tags=[{'Key':'Name','Value':'vpc1_public_instance1'}])

# Create "vpc1_private_sg" for Private Subnet of first_vpc
vpc1_security_group2 = ec2.create_security_group(GroupName='vpc1_private_sg',Description='vpc1_private_sg',VpcId=first_vpc.id)
vpc1_security_group2.authorize_ingress(CidrIp='10.10.1.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)
vpc1_security_group2.authorize_ingress(CidrIp='192.168.2.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)

vpc1_security_group2_tag=[vpc1_security_group2.id]
ec2_client.create_tags(Resources=vpc1_security_group2_tag,Tags=[{'Key':'Name','Value':'vpc1_private_sg'}])
# Launch an instance in vpc1's private subnet
vpc1_private_instance1 = subnet2.create_instances(
	ImageId='ami-1c47407f',
	MinCount=1,
	MaxCount=1,
	KeyName='vcloudynet-au',
	InstanceType='t2.micro',
	SecurityGroupIds=[ vpc1_security_group2.id ]
	#NetworkInterfaces=[{'NetworkInterfaceId': network_interface.id,'DeviceIndex':0}]
)

# Retrive vpc1_private_instance1's id and Tag it
vpc1_private_instance1 = list(vpc1_private_instance1)[0]
ec2_client.create_tags(Resources=[vpc1_private_instance1.id],Tags=[{'Key':'Name','Value':'vpc1_private_instance1'}])

# create a security group called "vpc2_public_sg" for Public Subnet of second_vpc
vpc2_security_group1 = ec2.create_security_group(GroupName='vpc2_public_sg',Description='vpc2_public_sg',VpcId=second_vpc.id)
vpc2_security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
vpc2_security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=80,ToPort=80)
vpc2_security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=443,ToPort=443)
vpc2_security_group1.authorize_ingress(CidrIp='192.168.2.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)

vpc2_security_group1_tag=[vpc2_security_group1.id]
ec2_client.create_tags(Resources=vpc2_security_group1_tag,Tags=[{'Key':'Name','Value':'vpc2_public_sg'}])

# Launch an instance in vpc2's private subnet
vpc2_public_instance1 = subnet3.create_instances(
	ImageId='ami-1c47407f',
	MinCount=1,
	MaxCount=1,
	KeyName='vcloudynet-au',
	InstanceType='t2.micro',
	SecurityGroupIds=[ vpc2_security_group1.id ]
	#NetworkInterfaces=[{'NetworkInterfaceId': network_interface.id,'DeviceIndex':0}]
)

# Retrive vpc2_public_instance1's id and Tag it
vpc2_public_instance1 = list(vpc2_public_instance1)[0]
ec2_client.create_tags(Resources=[vpc2_public_instance1.id],Tags=[{'Key':'Name','Value':'vpc2_public_instance1'}])

# Create "vpc2_private_sg" for Private Subnet of second_vpc
vpc2_security_group2 = ec2.create_security_group(GroupName='vpc2_private_sg',Description='vpc2_private_sg',VpcId=second_vpc.id)
vpc2_security_group2.authorize_ingress(CidrIp='192.168.1.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)
vpc2_security_group2.authorize_ingress(CidrIp='10.10.2.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)

vpc2_security_group2_tag=[vpc2_security_group2.id]
ec2_client.create_tags(Resources=vpc2_security_group2_tag,Tags=[{'Key':'Name','Value':'vpc2_private_sg'}])
# Launch an instance in vpc2's private subnet
vpc2_private_instance1 = subnet4.create_instances(
	ImageId='ami-1c47407f',
	MinCount=1,
	MaxCount=1,
	KeyName='vcloudynet-au',
	InstanceType='t2.micro',
	SecurityGroupIds=[ vpc2_security_group2.id ]
	#NetworkInterfaces=[{'NetworkInterfaceId': network_interface.id,'DeviceIndex':0}]
)

# Retrive vpc1_private_instance1's id and Tag it
vpc2_private_instance1 = list(vpc2_private_instance1)[0]
ec2_client.create_tags(Resources=[vpc2_private_instance1.id],Tags=[{'Key':'Name','Value':'vpc2_private_instance1'}])

