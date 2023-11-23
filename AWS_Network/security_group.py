import boto3
import sys
import ingress_rules
import ingress_rules_production
client = boto3.client('ec2')


class Extras:
    sgIds = []    # Ids generated during SG creation

    def __init__(self, vpc_name, vpc_id_to_use):
        self.vpc_name = vpc_name
        self.vpc_id_to_use = vpc_id_to_use

    def sg_group(self, name):
        #
        response = client.create_security_group(
            Description=f'{name}',
            GroupName=f'{name}',
            VpcId=f"{self.vpc_id_to_use[0]}",
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f'{self.vpc_name}_security_group_{name}'
                        },
                    ]
                },
            ],
        )
        self.sgIds.append(response['GroupId'])   # appends security group ID
        print(f" Security group {name} with groupId {response['GroupId']} "
              f"has been created in VPC {self.vpc_id_to_use[0]}.")

        return response

    def create_security_group(self):
        data = {
            "development": {
                "sg_name": ["load_balancer:development", "webserver:development", "databases:development"]
            },
            "production": {
                "sg_name": ["load_balancer:production", "webserver:production", "databases:production"]
            },
            "Exit": 'exit',
        }
        index = 0
        print("Please, select your environment")
        for item in data:
            print(f'{index + 1}) {item}')
            index += 1
        try:
            selection = int(input("Selection (Number only): "))
            if selection not in range(1, 4):
                print("Please, the value must be between 1 and 3 inclusive")
                Extras.create_security_group(self)
            elif selection in range(1, 4):
                #index = 0
                if selection == 1:
                    for value in data["development"]["sg_name"]:
                        Extras.sg_group(self, value)
                elif selection == 2:
                    for value in data["production"]["sg_name"]:
                        Extras.sg_group(self, value)
                elif selection == 3:
                    print("Thank you for using our program. Bye.")
                    sys.exit()
                return selection    # Project Environment type
        except ValueError:
            print("Please, only numbers are allowed")
            Extras.create_security_group(self)

    def ingress_rules(self):
        print(Extras.sgIds)
        selection = Extras.create_security_group(self)
        if selection == 1:
            ingress_rule_object = ingress_rules.Traffic(Extras.sgIds[0], Extras.sgIds[1])
            # part of code imported from ingress rules
            imported_code = [ingress_rule_object.rule_load_balancer_dev(), ingress_rule_object.rule_webserver_dev(),
                             ingress_rule_object.rule_database_dev()]
            print(imported_code)
            index = 0
            for identity in Extras.sgIds:
                response = client.authorize_security_group_ingress(
                    GroupId=f'{identity}',
                    IpPermissions=[
                        imported_code[index]
                    ],
                )
                index += 1
        elif selection == 2:
            ingress_rule_object = ingress_rules_production.Traffic(Extras.sgIds[0], Extras.sgIds[1])
            # part of code imported from ingress rules
            imported_code = [ingress_rule_object.rule_load_balancer_dev(), ingress_rule_object.rule_webserver_dev(),
                             ingress_rule_object.rule_database_dev()]
            index = 0
            for identity in Extras.sgIds:
                response = client.authorize_security_group_ingress(
                    GroupId=f'{identity}',
                    IpPermissions=[
                        imported_code[index]
                    ],
                )
                index += 1


