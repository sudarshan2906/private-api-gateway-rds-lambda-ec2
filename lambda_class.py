import boto3


class Lambda:
    def __init__(self, lambda_function_name, region):
        self.client_lambda = boto3.client('lambda', region_name=region)
        self.lambda_function_name = lambda_function_name

    def set_environment_variable(self, db_instance, username, password, database_name):
        self.client_lambda.update_function_configuration(
            FunctionName=self.lambda_function_name,
            Environment={
                'Variables': {
                    'db_instance_identifier': db_instance,
                    'username': username,
                    'password': password,
                    'database_name': database_name
                }
            }
        )

    def start_lambda(self):
        self.client_lambda.invoke(FunctionName=self.lambda_function_name)
