
class Traffic:
    def __init__(self, group_id1, group_id2):
        self.group_id1 = group_id1
        self.group_id2 = group_id2

    def rule_load_balancer_dev(self):
        rules = {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'Access from (via HTTP) Internet',
                    },
                ],
                'ToPort': 80,
            }
        return rules

    def rule_webserver_dev(self):
        rules = {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'ToPort': 80,
            'UserIdGroupPairs': [
                {
                    'Description': 'HTTP traffic from load balancer SG ',
                    'GroupId': f"{self.group_id1}",
                },
            ],
        }
        return rules

    def rule_database_dev(self):
        rules = {
            'FromPort': 80,
            'IpProtocol': 'tcp',
            'ToPort': 80,
            'UserIdGroupPairs': [
                {
                    'Description': 'Traffic from webserver SG ',
                    'GroupId': f"{self.group_id2}",
                },
            ],
        }
        return rules
