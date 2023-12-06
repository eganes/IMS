import boto3
import botocore.exceptions
import sys
import security_group
import route_table
client = boto3.client('ec2')


def attach_route_to_subnet_gateway(route_table_id, subnet_id, gateway_id):
    response1 = client.associate_route_table(
        RouteTableId=f'{route_table_id}',
        SubnetId=f'{subnet_id}',
    )
    return response1



def object_creation():
    items = ["VPC", "private subnet 1", "private subnet 2",
             "private subnet 3", "private subnet 4", "public subnet 1", "public subnet 2"]
    cidrs = []
    vpc_name = input("What is the vpc name ? : ")
    print("Please, give the cidrs of the following in the form (x.x.x.x/00)")
    index = 0
    for item in items:
        item = input(f"{item} cidr : ")
        cidrs.append(item)
    vpc_object = VPC(f'{cidrs[0]}', f'{vpc_name}', f'{cidrs[1]}', f'{cidrs[2]}', f'{cidrs[3]}'
                     , f'{cidrs[4]}', f'{cidrs[5]}', f'{cidrs[6]}')
    # Attaching internet gateway and creates subnets
    vpc_object.attach_internet_gateway()
    vpc_object.private_subnets()
    # Creates security group
    extra_object = security_group.Extras(f'{vpc_name}',
                                         vpc_object.vpc_id_to_use) # sends values to security group object
    route_table_object = route_table.RouteTable(f'{vpc_name}', vpc_object.vpc_id_to_use,
                                                f'{cidrs[0]}', vpc_object.igw_id[0])
    route_table_ids = route_table_object.route_table_ids

    try:
        extra_object.ingress_rules()
        route_table_object.create_route_table()
        index = 0
        for value in vpc_object.subnet_ids:
            attach_route_to_subnet_gateway(route_table_ids[index], value, vpc_object.igw_id[0])
    except botocore.exceptions:
        print("Security group and rules or other properties should be verified maybe created already.")
        sys.exit()
    except ValueError:
        print("An error encountered, please try later.")
        sys.exit()


class VPC:
    vpc_id_to_use = []
    igw_id = []
    subnet_ids = []

    def __init__(self, cidr, vpc_name, cidr_sub1, cidr_sub2, cidr_sub3, cidr_sub4, cidr_sub5, cidr_sub6):
        self.cidr = cidr
        self.vpc_name = vpc_name
        self.cidr_sub1 = cidr_sub1
        self.cidr_sub2 = cidr_sub2
        self.cidr_sub3 = cidr_sub3
        self.cidr_sub4 = cidr_sub4
        self.cidr_sub5 = cidr_sub5
        self.cidr_sub6 = cidr_sub6

    def vpc(self):
        try:
            response = client.create_vpc(
                CidrBlock=f'{self.cidr}',
                InstanceTenancy='default',
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': f'{self.vpc_name}'
                            },
                        ]
                    },
                ]
            )
            vpc_idd = self.vpc_id_to_use.append(response['Vpc']['VpcId'])
            print(f"VPC {self.vpc_name} created with id  :{response['Vpc']['VpcId']} ")
            return [response, self.vpc_name, response['Vpc']['VpcId']]
        except botocore.exceptions.ClientError:
            print("Sorry, an error occured, verify your vpc cidr or try later")
            sys.exit()

    def internet_gateway(self):
        try:
            response = client.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType':  'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': f'{self.vpc_name}_internet_gateway'
                            },
                        ]
                    },
                ],
            )
            self.igw_id.append(response['InternetGateway']['InternetGatewayId'])
            return response['InternetGateway']['InternetGatewayId']
        except botocore.exceptions.ClientError:
            print("Sorry, an error occured, verify your vpc cidr or try later")
            sys.exit()

    def attach_internet_gateway(self):
        try:
            vpc_object = VPC(self.cidr, self.vpc_name, self.cidr_sub1,
                             self.cidr_sub2, self.cidr_sub3, self.cidr_sub4, self.cidr_sub5, self.cidr_sub6)
            vpc_id = vpc_object.vpc()[2]
            internet_gateway_id = vpc_object.internet_gateway()
            response = client.attach_internet_gateway(
                InternetGatewayId=f'{internet_gateway_id}',
                VpcId=f'{vpc_id}')
            status = response['ResponseMetadata']['HTTPStatusCode']
            if status == 200:
                print(f"Internet gateway created and attached to vpc with id  :  {vpc_id} ")
            return response
        except botocore.exceptions.ClientError:
            print("Sorry, an error occured, verify your vpc cidr or try later")
            sys.exit()

    def private_subnets(self):
        try:
            data = {
                "subnet1": [f'{self.vpc_name}_private_insurance_subnet_1a', 'us-east-1a', self.cidr_sub1],
                "subnet2": [f'{self.vpc_name}_private_insurance_subnet_1b', 'us-east-1b', self.cidr_sub2],
                "subnet3": [f'{self.vpc_name}_private_insurance_subnet_1c', 'us-east-1a', self.cidr_sub3],
                "subnet4": [f'{self.vpc_name}_private_insurance_subnet_1d', 'us-east-1b', self.cidr_sub4],
            }
            vpc_object = VPC(self.cidr, self.vpc_name, self.cidr_sub1, self.cidr_sub2,
                             self.cidr_sub3, self.cidr_sub4)
            for data1 in data:
                name = data[f'{data1}'][0]
                zone = data[f'{data1}'][1]
                subnet_cidr = data[f'{data1}'][2]
                vpc_object.subnet(name, zone, subnet_cidr)
        except botocore.exceptions.ClientError as err:
            print(err)
            print("Sorry, an error occured, verify your  cidrs or other info or try later")
            sys.exit()

    def public_subnets(self):
        try:
            data = {
                "subnet1": [f'{self.vpc_name}_public_insurance_subnet_1a', 'us-east-1a', self.cidr_sub5],
                "subnet2": [f'{self.vpc_name}_public_insurance_subnet_1b', 'us-east-1b', self.cidr_sub6],
            }
            vpc_object = VPC(self.cidr, self.vpc_name, self.cidr_sub1, self.cidr_sub2,
                             self.cidr_sub3, self.cidr_sub4, self.cidr_sub5, self.cidr_sub6)
            for data1 in data:
                name = data[f'{data1}'][0]
                zone = data[f'{data1}'][1]
                subnet_cidr = data[f'{data1}'][2]
                vpc_object.subnet(name, zone, subnet_cidr)
        except botocore.exceptions.ClientError as err:
            print(err)
            print("Sorry, an error occured, verify your  cidrs or other info or try later")
            sys.exit()

    def subnet(self, name, zone, cidr):
        vpc_object = VPC(self.cidr, self.vpc_name, self.cidr_sub1, self.cidr_sub2, self.cidr_sub3, self.cidr_sub4)
        response = client.create_subnet(
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name
                        },
                    ]
                },
            ],
            AvailabilityZone=zone,
            CidrBlock=cidr,
            VpcId=self.vpc_id_to_use[0], )
        self.subnet_ids.append(response['Subnet']['SubnetId'])  # appends subnet ids
        print(f" Subnet {name} with subnet_id {response['Subnet']['SubnetId']} has been created.")
        return response
