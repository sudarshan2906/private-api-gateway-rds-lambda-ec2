import boto3

client = boto3.client('apigateway', region_name="ap-south-1")


class Api:
    def __init__(self, api_name):
        self.api_name = api_name
        self.api_id = ""
        self.deploy_id = ""

    def get_api_id(self):
        response = client.get_rest_apis()
        for api in response['items']:
            if api['name'] == self.api_name:
                self.api_id = api['id']
        return self.api_id

    def create_deployment(self):
        response = client.create_deployment(restApiId=self.api_id, stageName='test')
        self.deploy_id = response['id']