import boto3
import stack
import functions
from botocore.client import ClientError
import lambda_class
import api_gateway
import webbrowser
import vpc

DATA_BUCKET = "data-bucket-063"
DATABASE_NAME = "sample_db"
STACK_NAME = "week3"
TEMPLATE_URL = "https://data-bucket-063.s3.ap-south-1.amazonaws.com/template.yaml"
DB_INSTANCE_IDENTIFIER = "sudarshan1052063"
USERNAME = "admin"
PASSWORD = "admin123"
LAMBDA_FUNCTION_NAME = "lambdafunction"
API_NAME = "ApiGateway"
HOSTING_S3_NAME = "www.week3-website.com"
REGION = "ap-south-1"
VPC_NAME = "vpc"


# uploading templates and job file to S3

def upload_template_python_scripts():
    s3_client = boto3.client('s3', region_name=REGION)
    try:
        s3_client.create_bucket(Bucket=DATA_BUCKET, CreateBucketConfiguration={'LocationConstraint': REGION})
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Data Bucket Already Created")
        else:
            print(ce)
    except Exception as e:
        print(e)
        exit()
    functions_obj = functions.Functions(REGION)
    functions_obj.upload_file_folder(DATA_BUCKET, "Template")
    functions_obj.upload_zip_object(DATA_BUCKET, "lambda_function.py", "lambda_function.zip", "lambda_function.zip")
    functions_obj.upload_zip_object(DATA_BUCKET, "lambda_database_insertion.py", "lambda_database_insertion.zip",
                                    "lambda_database_insertion.zip")


if __name__ == "__main__":
    upload_template_python_scripts()
    stack_obj = stack.Stack(STACK_NAME, TEMPLATE_URL, DATABASE_NAME, DB_INSTANCE_IDENTIFIER, LAMBDA_FUNCTION_NAME,
                            API_NAME, HOSTING_S3_NAME, VPC_NAME, REGION)
    status = stack_obj.create_update_stack()

    # getting the vpc endpoint id from vpc name

    vpc_obj = vpc.Vpc(VPC_NAME)
    vpc_id = vpc_obj.get_vpc_id()
    vpc_endpoint_id = vpc_obj.get_vpc_endpoint_id(vpc_id)

    # updating environment variable for lambda functions.
    # calling the database insertion lambda function for insertion of data in datbase.

    client_lambda = boto3.client('lambda')
    lambda_obj = lambda_class.Lambda(LAMBDA_FUNCTION_NAME, REGION)
    lambda_obj.set_environment_variable(DB_INSTANCE_IDENTIFIER, USERNAME, PASSWORD, DATABASE_NAME)
    lambda_obj = lambda_class.Lambda("database_insertion", REGION)
    lambda_obj.set_environment_variable(DB_INSTANCE_IDENTIFIER, USERNAME, PASSWORD, DATABASE_NAME)
    lambda_obj.start_lambda()

    # assigning vpc endpoint id to api.
    # setting the policies for api to allow access of vpc endpoint.
    # deployment of api gateway.

    api_gateway = api_gateway.Api(API_NAME, REGION)
    api_id = api_gateway.get_api_id()
    api_gateway.set_policy(vpc_id)
    api_gateway.set_vpc_endpoint(vpc_endpoint_id)
    api_gateway.create_deployment()
    print("Api Deployed")
    api_url = api_id + ".execute-api.ap-south-1.amazonaws.com/test"
    print(api_url)

    # updating api_url value in html
    # uploading html to s3 for static page hosting

    client = boto3.resource("s3")
    functions.upload_html(HOSTING_S3_NAME, 'index.html', REGION)
    url = "http://" + HOSTING_S3_NAME + ".s3-website.ap-south-1.amazonaws.com"
    print(url)
    webbrowser.open(url, new=2)
