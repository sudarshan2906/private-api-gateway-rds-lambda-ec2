import boto3


class Api:
    def __init__(self, api_name, region):
        self.api_name = api_name
        self.api_id = ""
        self.deploy_id = ""
        self.client_api_gateway = boto3.client('apigateway', region_name=region)

    def get_api_id(self):
        response = self.client_api_gateway.get_rest_apis()
        for api in response['items']:
            if api['name'] == self.api_name:
                self.api_id = api['id']
        return self.api_id

    def create_deployment(self):
        response = self.client_api_gateway.create_deployment(restApiId=self.api_id, stageName='test')
        self.deploy_id = response['id']

    def set_policy(self, vpc_id):
        policy = '{"Version":"2012-10-17","Statement":[{"Effect":"Deny","Principal":"*","Action":"execute-api:Invoke",' \
                 '"Resource":"arn:aws:execute-api:ap-south-1:193175317457:'+self.api_id+'/*/*/*","Condition":{"StringNotEquals":{' \
                 '"aws:sourceVpc":"'+vpc_id+'"}}},{"Effect":"Allow","Principal":"*","Action":"execute-api:Invoke",' \
                 '"Resource":"arn:aws:execute-api:ap-south-1:193175317457:'+self.api_id+'/*/*/*"}]}'
        self.client_api_gateway.update_rest_api(restApiId=self.api_id,
                                                patchOperations=[
                                                    {
                                                        'op': 'replace',
                                                        'path': '/policy',
                                                        'value': policy
                                                    }
                                                ])

    def set_vpc_endpoint(self, vpc_endpoint_id):
        self.client_api_gateway.update_rest_api(restApiId=self.api_id,
                                                patchOperations=[
                                                    {
                                                        'op': 'add',
                                                        'path': '/endpointConfiguration/vpcEndpointIds',
                                                        'value': vpc_endpoint_id
                                                    }
                                                ])