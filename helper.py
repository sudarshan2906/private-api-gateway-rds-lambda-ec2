import boto3
import stack
import functions
from botocore.client import ClientError
import database_creation_insertion as db

DATA_BUCKET = "data-bucket-063"
DATA_BASE_NAME = "sample_db"
STACK_NAME = "week3"
TEMPLATE_URL = "https://data-bucket-063.s3.ap-south-1.amazonaws.com/template.yaml"
HOST = "wd103rfhtoh99dg.cumd1mkctnev.ap-south-1.rds.amazonaws.com"
USERNAME = "admin"
PASSWORD = "admin123"

parameter = {
    "data_bucket": DATA_BUCKET,
    "database_name": DATA_BASE_NAME,
    "stack_name": STACK_NAME,
    "template_url": TEMPLATE_URL
}


# uploading templates and job file to S3

def upload_template():
    s3 = boto3.resource('s3')
    try:
        s3.create_bucket(Bucket=DATA_BUCKET, CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Data Bucket Already Created")
        else:
            print(ce)
    except Exception as e:
        print(e)
        exit()
    functions.upload_file_folder(DATA_BUCKET, "Template")


if __name__ == "__main__":
    upload_template()
    # Stack = stack.Stack(parameter)
    # Stack.create_update_stack()
    DB = db.Database(HOST, USERNAME, PASSWORD, DATA_BASE_NAME)
