import boto3
import botocore
client = boto3.client('ec2')


class RouteTable:
    route_table_ids = []

    def __init__(self, vpc_name, vpc_id_to_use, route_table_name):
        self.vpc_name = vpc_name
        self.vpc_id_to_use = vpc_id_to_use
        self.route_table_name = route_table_name

    def create_route_table(self):
        response = client.create_route_table(
            VpcId=f'{self.vpc_id_to_use}',
            TagSpecifications=[
                {
                    'ResourceType': 'route-table',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f'{self.vpc_name}_route_table_{self.route_table_name}'
                        },
                    ]
                },
            ]
        )
        self.route_table_ids.append(response['RouteTable']['RouteTableId'])
        print(f" route table {self.route_table_name} with route table Id {response['RouteTable']['RouteTableId']} "
              f"has been created in VPC {response['RouteTable']['VpcId']}.")
        return response


table = RouteTable("test", "vpc-071d1fae34c4e3836", "Test_rt").create_route_table()
print(table)
