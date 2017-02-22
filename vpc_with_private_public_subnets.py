# import boto3
>>> import boto3

# A resource representing EC2.
>>> ec2 = boto3.resource('ec2')

# create_vpc() is EC2 resource's one of the available actions.
>>> vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
>>> print vpc
ec2.Vpc(id='vpc-1b19bb7f')

# create_subnet() is EC2 resource's one of the available actions.
>>> subnet = ec2.create_subnet(VpcId='vpc-1b19bb7f',CidrBlock='192.168.1.0/24')
>>> print subnet
ec2.Subnet(id='subnet-8d5dcdfb')

# create_subnet() is EC2 resource's one of the available actions.
>>> subnet = ec2.create_subnet(VpcId='vpc-1b19bb7f',CidrBlock='192.168.2.0/24')
>>> print subnet
ec2.Subnet(id='subnet-655ece13')

# create_internet_gateway() is EC2 resource's one of the available actions.
>>> internet_gateway = ec2.create_internet_gateway()
>>> print internet_gateway
ec2.InternetGateway(id='igw-cc1e28a9')

# attach_internet_gateway() is EC2 VPC resource's one of the available actions.
>>> response = vpc.attach_internet_gateway(InternetGatewayId='igw-cc1e28a9')

# A low-level client representing EC2. And describe_route_tables is EC2's one of the available methods.
>>> client = boto3.client('ec2')
>>> response = client.describe_route_tables(Filters=[{'Name':'vpc-id','Values':['vpc-1b19bb7f']}])
>>> print response
{'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': 'de0b096b-b5cf-4cca-b40c-50928192ff47', 'HTTPHeaders': {'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding', 'server': 'AmazonEC2', 'content-type': 'text/xml;charset=UTF-8', 'date': 'Wed, 22 Feb 2017 14:28:19 GMT'}}, u'RouteTables': [{u'Associations': [{u'RouteTableAssociationId': 'rtbassoc-8639c7e1', u'Main': True, u'RouteTableId': 'rtb-32d7bb56'}], u'RouteTableId': 'rtb-32d7bb56', u'VpcId': 'vpc-1b19bb7f', u'PropagatingVgws': [], u'Tags': [], u'Routes': [{u'GatewayId': 'local', u'DestinationCidrBlock': '192.168.0.0/16', u'State': 'active', u'Origin': 'CreateRouteTable'}]}]}

# create_route() is the one of the available methods of A low-level client representing EC2.
# import boto3
# client = boto3.client('ec2')
 >>> response = client.create_route(RouteTableId='rtb-32d7bb56',GatewayId='igw-cc1e28a9',DestinationCidrBlock='0.0.0.0/0')


# ec2.RouteTable is A resource representing EC2 RouteTable.
# associate_subnet_cidr_block() is the one of the available methods of A low-level client representing EC2.
# import boto3
# route_table = ec2.RouteTable('id')
>>> route_table = ec2.RouteTable('rtb-32d7bb56')

# Query subnets associated with vpc-id='vpc-1b19bb7f'
>>> response = client.describe_subnets(Filters=[{'Name':'vpc-id','Values':['vpc-1b19bb7f']}])
>>> print response
{u'Subnets': [{u'VpcId': 'vpc-1b19bb7f', u'AvailableIpAddressCount': 251, u'MapPublicIpOnLaunch': False, u'DefaultForAz': False, u'Ipv6CidrBlockAssociationSet': [], u'State': 'available', u'AvailabilityZone': 'ap-southeast-2c', u'SubnetId': 'subnet-6efd4b37', u'CidrBlock': '192.168.3.0/24', u'AssignIpv6AddressOnCreation': False}, {u'VpcId': 'vpc-1b19bb7f', u'AvailableIpAddressCount': 251, u'MapPublicIpOnLaunch': False, u'DefaultForAz': False, u'Ipv6CidrBlockAssociationSet': [], u'State': 'available', u'AvailabilityZone': 'ap-southeast-2a', u'SubnetId': 'subnet-655ece13', u'CidrBlock': '192.168.2.0/24', u'AssignIpv6AddressOnCreation': False}, {u'VpcId': 'vpc-1b19bb7f', u'AvailableIpAddressCount': 251, u'MapPublicIpOnLaunch': False, u'DefaultForAz': False, u'Ipv6CidrBlockAssociationSet': [], u'State': 'available', u'AvailabilityZone': 'ap-southeast-2a', u'SubnetId': 'subnet-8d5dcdfb', u'CidrBlock': '192.168.1.0/24', u'AssignIpv6AddressOnCreation': False}], 'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': 'dc4e5898-b0b7-4b00-8a55-841fb59f6929', 'HTTPHeaders': {'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding', 'server': 'AmazonEC2', 'content-type': 'text/xml;charset=UTF-8', 'date': 'Wed, 22 Feb 2017 15:08:13 GMT'}}}


# associate_with_subnet() is one of the EC2.RouteTable Resource's available actions.
>>> route_table_association = route_table.associate_with_subnet(SubnetId='subnet-8d5dcdfb')


# Create a route table for 192.168.2.0/24 and 192.168.3.0/24 & attach to VPC
>> route_table = ec2.create_route_table(VpcId='vpc-1b19bb7f')
>>> print route_table
ec2.RouteTable(id='rtb-57214e33')

>>> route_table = ec2.RouteTable('rtb-57214e33')
>>> route_table_association = route_table.associate_with_subnet(SubnetId='subnet-6efd4b37')
>>> route_table_association = route_table.associate_with_subnet(SubnetId='subnet-655ece13')

===================================================================================
#import boto3
>>> import boto3

# A resource representing EC2
>>> ec2 = boto3.resource('ec2')

# create_vpc is EC2 resource's one of the available actions.
>>> vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
>>> print vpc
ec2.Vpc(id='vpc-1b19bb7f')

# A resource representing EC2 VPC
>>> vpc = ec2.Vpc(id='vpc-1b19bb7f') 

# subnet_create() is EC2 VPC resource's one of the available actions.
>>> subnet = vpc.create_subnet(CidrBlock='192.168.3.0/24',AvailabilityZone='ap-southeast-2c')
>>> print subnet
