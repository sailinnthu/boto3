My VPC Setup in boto3

#SINGAPORE

#reference http://www.cloudygoodness.com/?p=646

# method-1 (Singapore)
# import boto3
# ec2 = boto3.resource('ec2', region_name="ap-southeast-1")
# vpc = ec2.create_vpc(CidrBlock='10.10.0.0/16')

# method-1 
# import boto3 (London)
# ec2_london = boto3.resource('ec2', region_name="eu-west-2")
# vpc = ec2_london.create_vpc(CidrBlock='192.168.0.0/16')

# method-1 with client
# import boto3
# ec2 = boto3.resource('ec2', region_name="ap-southeast-1")
# client = boto3.client('ec2', region_name="ap-southeast-1")
# sg_vpc = ec2.create_vpc(CidrBlock='10.10.0.0/16')
# client.create_route(RouteTableId=public_route_table.id,DestinationCidrBlock='0.0.0.0/0',GatewayId=igw.id)

# import boto3, EC2.Client, EC2.ServiceResource
import boto3
singapore = boto3.Session(profile_name='singapore')
singapore_client = boto3.Session(profile_name='singapore')
ec2 = singapore.resource('ec2')
ec2_client = singapore_client.client('ec2')

import boto3
>>> ec2 = boto3.resource('ec2', region_name="ap-southeast-1")
>>> ec2_client = boto3.client('ec2', region_name="ap-southeast-1")
# create vpc
sg_vpc = ec2.create_vpc(CidrBlock='10.10.0.0/16')
sg_vpc.modify_attribute(EnableDnsSupport={'Value':True})
sg_vpc.modify_attribute(EnableDnsHostnames={'Value':True})
# tag vpc 
sg_vpc.create_tags(Tags=[{'Key':'Name','Value':'singapore_vpc'}])

# create 1xPublic Subnet & 2xPrivate Subnets
subnet1 = sg_vpc.create_subnet(CidrBlock='10.10.1.0/24',AvailabilityZone='ap-southeast-1a')
subnet1.meta.client.modify_subnet_attribute(SubnetId=subnet1.id, MapPublicIpOnLaunch={"Value": True})
subnet2 = sg_vpc.create_subnet(CidrBlock='10.10.2.0/24',AvailabilityZone='ap-southeast-1b')
subnet3 = sg_vpc.create_subnet(CidrBlock='10.10.3.0/24',AvailabilityZone='ap-southeast-1a')

# create tag for subnets
subnet1_tag=[subnet1.id]
subnet2_tag=[subnet2.id]
subnet3_tag=[subnet3.id]

ec2_client.create_tags(Resources=subnet1_tag,Tags=[{'Key':'Name','Value':'public_subnet'}])
ec2_client.create_tags(Resources=subnet2_tag,Tags=[{'Key':'Name','Value':'private_subnet_1'}])
ec2_client.create_tags(Resources=subnet3_tag,Tags=[{'Key':'Name','Value':'private_subnet_2'}])

# create Internet Gateway and attach to vpc
igw = ec2.create_internet_gateway()
igw.attach_to_vpc(VpcId=sg_vpc.id)

# Query RouteTableId
public_route_table = list(sg_vpc.route_tables.all())[0]
# add a default route, for Public Subnet, pointing to Internet Gateway 
ec2_client.create_route(RouteTableId=public_route_table.id,DestinationCidrBlock='0.0.0.0/0',GatewayId=igw.id)
public_route_table.associate_with_subnet(SubnetId=subnet1.id)

# create a route table for 2xPrivate Subnets
private_route_table = ec2.create_route_table(VpcId=sg_vpc.id)
private_route_table.associate_with_subnet(SubnetId=subnet2.id)
private_route_table.associate_with_subnet(SubnetId=subnet3.id)

# create a security group called "public_sg" for Public Subnet
security_group1 = ec2.create_security_group(GroupName='public_sg',Description='public_sg',VpcId=sg_vpc.id)
security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=80,ToPort=80)
security_group1.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=443,ToPort=443)

## security_group1 = list(sg_vpc.security_groups.all())[1]

# create a network interface for EC2 Instance
#network_interface = ec2.create_network_interface(SubnetId=subnet1.id,Groups=[security_group1.id])


# Launch an EC2 Instance
public_instance_1 = subnet1.create_instances(
		ImageId='ami-dc9339bf',
		MinCount=1,
    	MaxCount=1,
    	KeyName='vcloudynet-sg',
    	InstanceType='t2.micro',
    	SecurityGroupIds=[ security_group1.id ]
    	#NetworkInterfaces=[{'NetworkInterfaceId': network_interface.id,'DeviceIndex':0}]
	)

# Allocate Elastic IP 
eip_for_nat_gateway = ec2_client.allocate_address(Domain='vpc')
allocation_id = eip_for_nat_gateway['AllocationId']

# create NAT Gateway and associate with Elastic IP
nat_gw = ec2_client.create_nat_gateway(SubnetId=subnet1.id,AllocationId=allocation_id)
nat_gw_id = nat_gw['NatGateway']['NatGatewayId']


# Create a default route pointing to NAT Gateway for 2xPrivate Subnets
ec2_client.create_route(RouteTableId=private_route_table.id,DestinationCidrBlock='0.0.0.0/0',NatGatewayId=nat_gw_id)

# create a security group called "private_sg" for Private Subnet
security_group2 = ec2.create_security_group(GroupName='private_sg',Description='private_sg',VpcId=sg_vpc.id)
# Allow All Traffic from Public Subnet 10.10.1.0/24 to Private Subnet
security_group2.authorize_ingress(CidrIp='10.10.1.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)

# Allow All Traffic between 2 x Private Subnets
security_group2.authorize_ingress(CidrIp='10.10.2.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)
security_group2.authorize_ingress(CidrIp='10.10.3.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)
# # Allow All Traffic from Private Subnet 10.10.2.0/24 & 10.10.2.0/24
security_group1.authorize_ingress(CidrIp='10.10.2.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)
security_group1.authorize_ingress(CidrIp='10.10.3.0/24',IpProtocol='-1',FromPort=-1,ToPort=-1)

# Create 2xInstances in Private Subnets
private_instance_1 = subnet2.create_instances(
		ImageId='ami-dc9339bf',
		MinCount=1,
    	MaxCount=1,
    	KeyName='vcloudynet-sg',
    	SecurityGroupIds=[ security_group2.id ],
    	InstanceType='t2.micro'
	)
private_instance_2 = subnet3.create_instances(
		ImageId='ami-dc9339bf',
		MinCount=1,
    	MaxCount=1,
    	KeyName='vcloudynet-sg',
    	SecurityGroupIds=[ security_group2.id ],
    	InstanceType='t2.micro'
	)


=========================
# LONDON

import boto3
ec2 = boto3.resource('ec2', region_name="eu-west-2")
client = boto3.client('ec2', region_name="eu-west-2")

london_vpc = ec2.create_vpc(CidrBlock='172.16.0.0/16')
client.modify_vpc_attribute(VpcId=london_vpc.id,EnableDnsSupport={'Value':True})
client.modify_vpc_attribute(VpcId=london_vpc.id,EnableDnsHostnames={'Value':True})

subnet1 = london_vpc.create_subnet(CidrBlock='172.16.1.0/24',AvailabilityZone='eu-west-2a')
subnet1.meta.client.modify_subnet_attribute(SubnetId=subnet1.id, MapPublicIpOnLaunch={"Value": True})
subnet2 = london_vpc.create_subnet(CidrBlock='172.16.2.0/24',AvailabilityZone='eu-west-2b')
subnet3 = london_vpc.create_subnet(CidrBlock='172.16.3.0/24',AvailabilityZone='eu-west-2a')

london_igw = ec2.create_internet_gateway()
london_igw.attach_to_vpc(VpcId=london_vpc.id)

public_route_table = list(london_vpc.route_tables.all())[0]
client.create_route(RouteTableId=public_route_table.id,DestinationCidrBlock='0.0.0.0/0',GatewayId=london_igw.id)
public_route_table.associate_with_subnet(SubnetId=subnet1.id)

private_route_table = ec2.create_route_table(VpcId=london_vpc.id)
private_route_table.associate_with_subnet(SubnetId=subnet2.id)
private_route_table.associate_with_subnet(SubnetId=subnet3.id)

security_group = ec2.create_security_group(GroupName='public_sg',Description='public_sg',VpcId=london_vpc.id)
security_group.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
security_group.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=80,ToPort=80)
security_group.authorize_ingress(IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=443,ToPort=443)
security_group = list(london_vpc.security_groups.all())[1]

# Create a Network Interface
network_interface = ec2.create_network_interface(SubnetId=subnet1.id,Groups=[security_group.id])

# Launch an instance with defining NetworkInterfaces

instance_london = ec2.create_instances(
		ImageId='ami-dc9339bf',
		MinCount=1,
    	MaxCount=1,
    	KeyName='vcloudynet-sg',
    	InstanceType='t2.micro',
    	NetworkInterfaces=[{'NetworkInterfaceId': network_interface.id,'DeviceIndex':0}]
	)

# Allocate Elastic IP

eip = client.allocate_address(Domain='vpc')
a = client.describe_addresses()
for b in a['Addresses']:
	print b['AllocationId']

c= b['AllocationId']
nat_gw = ec2_client.create_nat_gateway(SubnetId=subnet1.id,AllocationId=c)

nat_gw_id = nat_gw['NatGateway']['NatGatewayId']


# Create a default route pointing to NAT Gateway for 2xPrivate Subnets
client.create_route(RouteTableId=private_route_table.id,DestinationCidrBlock='0.0.0.0/0',NatGatewayId=nat_gw_id)

===========================================
# Launch instance without defining NetworkInterfaces
instance_sg3 = subnet1.create_instances(
		ImageId='ami-dc9339bf',
		MinCount=1,
    	MaxCount=1,
    	KeyName='vcloudynet-sg',
    	SecurityGroupIds=[ security_group.id ],
    	InstanceType='t2.micro'
	)

# Launch instance with Network Interface Define
# create a network interface for EC2 Instance
network_interface = ec2.create_network_interface(SubnetId=subnet1.id,Groups=[security_group1.id])
# Launch an EC2 Instance
public_instance_1 = ec2.create_instances(
		ImageId='ami-dc9339bf',
		MinCount=1,
    	MaxCount=1,
    	KeyName='vcloudynet-sg',
    	InstanceType='t2.micro',
    	NetworkInterfaces=[{'NetworkInterfaceId': network_interface.id,'DeviceIndex':0}]
	)
#Allocate EIP

eip1 = ec2_client.allocate_address(Domain='vpc')
eip2 = ec2_client.allocate_address(Domain='vpc')
eip3 = ec2_client.allocate_address(Domain='vpc')
eip = list(ec2.vpc_addresses.all())[0]


https://github.com/boto/boto3/issues/779
http://blog.codebender.cc/2015/10/09/writing-automation-tools-for-amazon-web-services/

===========================================

### Method 1
### Assign EIP and Associate to NAT Gateway
import boto3
ec2 = boto3.resource('ec2', region_name="eu-west-2")
client = boto3.client('ec2', region_name="eu-west-2")
vpc = ec2.create_vpc(CidrBlock='10.10.0.0/16')
subnet1 = vpc.create_subnet(CidrBlock='10.10.1.0/24',AvailabilityZone='eu-west-2a')
subnet1.meta.client.modify_subnet_attribute(SubnetId=subnet1.id, MapPublicIpOnLaunch={"Value": True})

eip_for_nat_gateway = ec2_client.allocate_address(Domain='vpc')
>>> a = client.describe_addresses()
>>> for b in a['Addresses']:
...print b['AllocationId']
eipalloc-3790c652
>>> c= b['AllocationId']
>>> print c
eipalloc-3790c652

#Now I assign c as AllocationId
nat_gw = client.create_nat_gateway(SubnetId=subnet1.id,AllocationId=c)

### Method 2

>>> eip_for_nat_gateway = ec2_client.allocate_address(Domain='vpc')
>>> print eip_for_nat_gateway
{u'PublicIp': '52.221.98.20', u'Domain': 'vpc', u'AllocationId': 'eipalloc-1991c77c', 'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': '8f44054f-8dcb-4f32-ac0f-e482611900a4', 'HTTPHeaders': {'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding', 'server': 'AmazonEC2', 'content-type': 'text/xml;charset=UTF-8', 'date': 'Thu, 23 Feb 2017 19:38:29 GMT'}}}
>>> allocation_id=eip_for_nat_gateway['AllocationId']
>>> print allocation_id
eipalloc-1991c77c
# Now assign allocation_id as AllocationId
nat_gw = client.create_nat_gateway(SubnetId=subnet1.id,AllocationId=allocation_id)

### How to Tag Instances

>>> instance_iterator = list(ec2.instances.all())
>>> print instance_iterator
[ec2.Instance(id='i-097cdfbf0f0c116f7')]
>>> instance_iterator = list(ec2.instances.all())[0]
>>> print instance_iterator
ec2.Instance(id='i-097cdfbf0f0c116f7')
>>> print instance_iterator.id
i-097cdfbf0f0c116f7
>>> 

