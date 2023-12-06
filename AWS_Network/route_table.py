import boto3
import botocore
client = boto3.client('ec2')


class RouteTable:
    route_table_ids = []
    table_names = ["private", "public"]  # Additional names for route tables

    def __init__(self, vpc_name, vpc_id_to_use, vpc_cidr, id_igw):
        self.vpc_name = vpc_name
        self.vpc_id_to_use = vpc_id_to_use
        self.vpc_cidr = vpc_cidr
        self.id_igw = id_igw

    def properties_of_route_tables(self):
        route_table = {
            "route_table_1": {
            },
            "route_table_2": {
                "routes": [{"destination": f'0.0.0.0/0', "Target": f'{self.id_igw}'}]
            },

        }
        return route_table

    def create_route_table(self):
        # creates route table with routes
        route_table_object = RouteTable(self.vpc_name, self.vpc_id_to_use, self.vpc_cidr, self.id_igw)
        object_property = route_table_object.properties_of_route_tables()
        for value in range(1, 3):  # limits number of route tables to 2, can be increased.
            if value == 1:
                route_table_object.route_table(route_table_object.table_names[0])  # creates route table
            elif value == 2:  # uses second properties
                route_table_object.route_table(route_table_object.table_names[1])
                response = client.create_route(  # creates routes
                    DestinationCidrBlock=f"{object_property['route_table_2']['routes'][0]['destination']}",
                    GatewayId=f"{object_property['route_table_2']['routes'][0]['Target']}",
                    RouteTableId=f'{self.route_table_ids[value-1]}', )
                return response

    def route_table(self, route_table_name):
        response = client.create_route_table(
            VpcId=f'{self.vpc_id_to_use[0]}',
            TagSpecifications=[
                {
                    'ResourceType': 'route-table',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f'{self.vpc_name}_route_table_{route_table_name}'
                        },
                    ]
                },
            ]
        )
        self.route_table_ids.append(response['RouteTable']['RouteTableId'])
        print(f" route table f'{self.vpc_name}_route_table_{route_table_name}' "
              f"with route table Id {response['RouteTable']['RouteTableId']} "
              f"has been created in VPC {response['RouteTable']['VpcId']}.")
        return response

