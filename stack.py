import boto3
import time
from botocore.client import ClientError


class Stack:
    def __init__(self, stack_name, template_url, database_name, db_instance_identifier, lambda_function_name,
                 api_name, hosting_s3_name, region):
        self.stack_name = stack_name
        self.template_url = template_url
        self.database_name = database_name
        self.db_instance_identifier = db_instance_identifier
        self.lambda_function_name = lambda_function_name
        self.api_name = api_name
        self.hosting_s3_name = hosting_s3_name
        self.client_cloudforamtion = boto3.client('cloudformation', region_name=region)
        self.client_s3 = boto3.client('s3', region_name=region)

    # if stack is in rollback stage then stack get deleted and then it gets created.
    # if stack is in create stage then it gets updated

    def create_update_stack(self):
        status = self.status_stack()
        if status == 'ROLLBACK_COMPLETE' or status == 'ROLLBACK_FAILED' or status == 'UPDATE_ROLLBACK_COMPLETE' or \
                status == 'DELETE_FAILED':
            self.delete_object()
            self.client_cloudforamtion.delete_stack(StackName=self.stack_name)
            print("deleting stack")
            while self.status_stack() == 'DELETE_IN_PROGRESS':
                time.sleep(2)
            print("stack deleted")
            self.create_stack()
            print("creating stack")
        elif status == 'CREATE_COMPLETE' or status == 'UPDATE_COMPLETE':
            self.update_stack()
            print("updating stack")
        else:
            self.create_stack()
            print("creating stack")
        while self.status_stack() == 'CREATE_IN_PROGRESS' or \
                self.status_stack() == 'UPDATE_IN_PROGRESS' or \
                self.status_stack() == 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS':
            time.sleep(2)
        print("stack created")
        return self.status_stack()

    def create_stack(self):
        try:
            self.client_cloudforamtion.create_stack(
                StackName=self.stack_name,
                TemplateURL=self.template_url,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Parameters=[
                    {
                        'ParameterKey': "DataBaseName",
                        'ParameterValue': self.database_name
                    },
                    {
                        'ParameterKey': "DbInstanceIdentifier",
                        'ParameterValue': self.db_instance_identifier
                    },
                    {
                        'ParameterKey': "LambdaFunctionName",
                        'ParameterValue': self.lambda_function_name
                    },
                    {
                        'ParameterKey': "ApiName",
                        'ParameterValue': self.api_name
                    },
                    {
                        'ParameterKey': "S3Name",
                        'ParameterValue': self.hosting_s3_name
                    }
                ]
            )
        except ClientError as ce:
            print(ce)
            exit()

    def update_stack(self):
        try:
            self.client_cloudforamtion.update_stack(
                StackName=self.stack_name,
                TemplateURL=self.template_url,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Parameters=[
                    {
                        'ParameterKey': "DataBaseName",
                        'ParameterValue': self.database_name
                    },
                    {
                        'ParameterKey': "DbInstanceIdentifier",
                        'ParameterValue': self.db_instance_identifier
                    },
                    {
                        'ParameterKey': "LambdaFunctionName",
                        'ParameterValue': self.lambda_function_name
                    },
                    {
                        'ParameterKey': "ApiName",
                        'ParameterValue': self.api_name
                    },
                    {
                        'ParameterKey': "S3Name",
                        'ParameterValue': self.hosting_s3_name
                    }
                ]
            )
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                print("Stack Already Updated")
            else:
                print(ce)
                exit()

    def status_stack(self):
        try:
            stack = self.client_cloudforamtion.describe_stacks(StackName=self.stack_name)
            status = stack['Stacks'][0]['StackStatus']
            return status
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                print("No stack present")
            else:
                print(ce)
                exit()

    def delete_object(self):
        try:
            res = self.client_s3.list_objects(Bucket=self.hosting_s3_name)
            for list_key in res['Contents']:
                self.client_s3.delete_object(Bucket=self.hosting_s3_name, Key=list_key['key'])
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'NoSuchBucket':
                print(ce)
            else:
                print(ce)
                exit()
