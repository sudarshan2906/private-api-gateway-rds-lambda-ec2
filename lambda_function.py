import pymysql
import json
import os
import boto3

db_instance_identifier = os.environ['db_instance_identifier']
USERNAME = os.environ['username']
PASSWORD = os.environ['password']
DATA_BASE_NAME = os.environ['database_name']


def handler(event, context):
    try:
        client_rds = boto3.client('rds')
        instances = client_rds.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        host = instances.get('DBInstances')[0]['Endpoint']['Address']
        conn = pymysql.connect(host,
                               user=USERNAME,
                               passwd=PASSWORD,
                               db=DATA_BASE_NAME,
                               connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute(
                "select count(*), sum(t.amount) from Transaction t "
                "inner join Account a on t.sender_account_number = a.account_number "
                "inner join Customer c on a.customer_id = c.customer_id where c.customer_id  = " + str(event["customer_id"]))
            for row in cur:
                transaction = row[0]
                sum = str(row[1])
    except pymysql.MySQLError as e:
        print(e)
        exit()
    return {
        'statusCode': 200,
        'No Of Transaction': json.dumps(transaction),
        'Sum of Transaction' : json.dumps(sum)
    }