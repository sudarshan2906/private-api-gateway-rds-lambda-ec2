import boto3


class Vpc:
    def __init__(self, vpc_name):
        self.ec2_client = boto3.client('ec2')
        self.vpc_name = vpc_name

    def get_vpc_id(self):
        response = self.ec2_client.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [self.vpc_name]
                }])
        return response['Vpcs'][0]['VpcId']

    def get_vpc_endpoint_id(self, vpc_id):
        response = self.ec2_client.describe_vpc_endpoints()
        endpoints = response['VpcEndpoints']
        for endpoint in endpoints:
            if endpoint['VpcId'] == vpc_id:
                return endpoint['VpcEndpointId']
