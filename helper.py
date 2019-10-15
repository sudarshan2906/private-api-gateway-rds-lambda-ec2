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
    s3 = boto3.client('s3', region_name=REGION)
    try:
        s3.create_bucket(Bucket=DATA_BUCKET, CreateBucketConfiguration={'LocationConstraint': REGION})
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Data Bucket Already Created")
        else:
            print(ce)
    except Exception as e:
        print(e)
        exit()
    functions.upload_file_folder(DATA_BUCKET, "Template")
    functions.upload_zip_object(DATA_BUCKET, "lambda_function.py", "lambda_function.zip", "lambda_function.zip")


if __name__ == "__main__":
    upload_template_python_scripts()
    Stack = stack.Stack(STACK_NAME, TEMPLATE_URL, DATABASE_NAME, DB_INSTANCE_IDENTIFIER, LAMBDA_FUNCTION_NAME, API_NAME, HOSTING_S3_NAME)
    status = Stack.create_update_stack()

    # creation and insertion of data to database

    DB = db.Database(DB_INSTANCE_IDENTIFIER, USERNAME, PASSWORD, DATABASE_NAME)
    DB.create_table()
    DB.insert_data()
    HOST = DB.get_host()

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

    Api_Gateway = api_gateway.Api(API_NAME)
    api_id = Api_Gateway.get_api_id()
    Api_Gateway.create_deployment()
    print("Api Deployed")
    api_url = api_id + ".execute-api.ap-south-1.amazonaws.com/test"
    print(api_url)

    # updating api_url value in html
    # uploading html to s3 for static page hosting

    client = boto3.resource("s3")
    functions.upload_html(HOSTING_S3_NAME, 'index.html')
    url = "http://"+HOSTING_S3_NAME+".s3-website.ap-south-1.amazonaws.com"
    print(url)
    webbrowser.open(url, new=2)
