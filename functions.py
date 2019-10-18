import os
import zipfile
import boto3


def upload_html(bucket_name, file_name, region):
    data = open(file_name, 'rb')
    s3_resource = boto3.resource('s3', region_name=region)
    s3_resource.Bucket(bucket_name).put_object(Key=file_name, Body=data, ContentType='text/html')


class Functions:
    def __init__(self, region):
        self.client_s3 = boto3.client('s3', region_name=region)

    def upload_object(self, bucket_name, filename, location):
        self.client_s3.upload_file(filename, bucket_name, location)

    def upload_file_folder(self, bucket_name, folder_name):
        for file in os.listdir(folder_name):
            self.client_s3.upload_file(folder_name + '/' + file, bucket_name, file)

    def upload_zip_object(self, bucket_name, input_filename, output_filename, location):
        zip = zipfile.ZipFile(output_filename, "w")
        zip.write(input_filename, os.path.basename(input_filename))
        zip.close()
        self.upload_object(bucket_name, output_filename, location)
        os.remove(output_filename)