import boto3
import stack
import functions
from botocore.client import ClientError
import database_creation_insertion as db
import api_gateway
import webbrowser

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


if __name__ == "__main__":
    upload_template_python_scripts()
    stack_obj = stack.Stack(STACK_NAME, TEMPLATE_URL, DATABASE_NAME, DB_INSTANCE_IDENTIFIER, LAMBDA_FUNCTION_NAME,
                            API_NAME, HOSTING_S3_NAME, REGION)
    status = stack_obj.create_update_stack()

    # creation and insertion of data to database

    database_obj = db.Database(DB_INSTANCE_IDENTIFIER, USERNAME, PASSWORD, DATABASE_NAME, REGION)
    database_obj.create_table()
    database_obj.insert_data()
    HOST = database_obj.get_host()

    # updating environment variable for lambda function

    client_lambda = boto3.client('lambda')
    client_lambda.update_function_configuration(
        FunctionName=LAMBDA_FUNCTION_NAME,
        Environment={
            'Variables': {
                'host': HOST,
                'username': USERNAME,
                'password': PASSWORD,
                'database_name': DATABASE_NAME
            }
        }
    )

    # deployment of api gateway

    api_gateway = api_gateway.Api(API_NAME, REGION)
    api_id = api_gateway.get_api_id()
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
