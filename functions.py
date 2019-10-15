import os
import zipfile
import boto3

s3 = boto3.client('s3', region_name='ap-south-1')


def upload_object(bucket_name, filename, location):
    s3.upload_file(filename, bucket_name, location)
    s3.Object(bucket_name, location).upload_file(Filename=filename)


def upload_file_folder(bucket_name, folder_name):
    for file in os.listdir(folder_name):
        s3.upload_file(folder_name + '/' + file, bucket_name, file)


def upload_zip_object(bucket_name, input_filename, output_filename, location):
    zip = zipfile.ZipFile(output_filename, "w")
    zip.write(input_filename, os.path.basename(input_filename))
    zip.close()
    upload_object(bucket_name, output_filename, location)
    os.remove(output_filename)


def upload_html(bucket_name, file_name):
    data = open(file_name, 'rb')
    s3_resource = boto3.resource('s3', region_name='ap-south-1')
    s3_resource.Bucket(bucket_name).put_object(Key=file_name, Body=data, ContentType='text/html')
