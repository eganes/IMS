import boto3
import botocore.exceptions
import sys
import security_group
client = boto3.client('ec2')

def object_creation():
    items = ["VPC","private subnet 1", "private subnet 2", "private subnet 3", "private subnet 4"]
    cidrs = []
    vpc_name = input("What is the vpc name ? : ")
    print("Please, give the cidrs of the following in the form (x.x.x.x/00)")
    index = 0
    for item in items:
        item = input(f"{item} cidr : ")
        cidrs.append(item)
    vpc_object = VPC(f'{cidrs[0]}', f'{vpc_name}', f'{cidrs[1]}', f'{cidrs[2]}', f'{cidrs[3]}', f'{cidrs[4]}')
    # Attaching internet gateway and creates subnets
    vpc_object.attach_internet_gateway()
    vpc_object.private_subnets()
    # Creates security group
    extra_object = security_group.Extras(f'{vpc_name}',
                                         vpc_object.vpc_id_to_use) # sends values to security group object
    try:
        extra_object.ingress_rules()
    except botocore.exceptions:
        print("Security group and rules should be verified maybe created already.")
        sys.exit()
    except ValueError:
        print("An error encountered, please try later.")
        sys.exit()


class VPC:
    vpc_id_to_use = []

    def __init__(self, cidr, vpc_name, cidr_sub1, cidr_sub2, cidr_sub3, cidr_sub4):
        self.cidr = cidr
        self.vpc_name = vpc_name
        self.cidr_sub1 = cidr_sub1
        self.cidr_sub2 = cidr_sub2
        self.cidr_sub3 = cidr_sub3
        self.cidr_sub4 = cidr_sub4

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
            return response['InternetGateway']['InternetGatewayId']
        except botocore.exceptions.ClientError:
            print("Sorry, an error occured, verify your vpc cidr or try later")
            sys.exit()

    def attach_internet_gateway(self):
        try:
            vpc_object = VPC(self.cidr, self.vpc_name, self.cidr_sub1, self.cidr_sub2, self.cidr_sub3, self.cidr_sub4)
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

    def subnet(self, name, zone, cidr):
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
        print(f" Subnet {name} with subnet_id {response['Subnet']['SubnetId']} has been created.")
        return response