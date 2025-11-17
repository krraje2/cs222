import boto3
import os

dynamo_client  =  boto3.resource(service_name = 'dynamodb',region_name = 'us-east-1',
              aws_access_key_id = os.environ["AWSAccessKeyId_CS222"],
              aws_secret_access_key = os.environ["AWSSecretKey_CS222"])

product_table = dynamo_client.Table('GPA')
print(product_table.table_status)