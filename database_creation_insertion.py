import pymysql
import boto3

client = boto3.client('rds', region_name='ap-south-1')


class Database:
    def __init__(self, db_instance_identifier, username, password, database_name):
        try:
            self.db_instance_identifier = db_instance_identifier
            self.host = self.get_host()
            self.conn = pymysql.connect(self.host,
                                        user=username,
                                        passwd=password,
                                        db=database_name,
                                        connect_timeout=5)
        except pymysql.MySQLError as e:
            print(e)
            exit()

    def get_host(self):
        instances = client.describe_db_instances(DBInstanceIdentifier=self.db_instance_identifier)
        return instances.get('DBInstances')[0]['Endpoint']['Address']

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "create table IF NOT EXISTS Customer("
                "customer_id int NOT NULL PRIMARY KEY,"
                "name varchar(50) NOT NULL)")
            cur.execute(
                "create table IF NOT EXISTS Account("
                "account_number int NOT NULL PRIMARY KEY,"
                "customer_id int NOT NULL, FOREIGN KEY(customer_id) REFERENCES Customer(customer_id))")
            cur.execute(
                "create table IF NOT EXISTS Transaction("
                "transaction_id int NOT NULL PRIMARY KEY,"
                "sender_account_number int NOT NULL,"
                "receiver_account_number int NOT NULL,"
                "amount int NOT NULL,"
                "FOREIGN KEY(sender_account_number) REFERENCES Account(account_number),"
                "FOREIGN KEY(receiver_account_number) REFERENCES Account(account_number))")
            self.conn.commit()
            print("table created")

    def insert_data(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute('insert into Customer (customer_id, name) values(101, "Joe")')
                cur.execute('insert into Customer (customer_id, name) values(102, "Olivia")')
                cur.execute('insert into Customer (customer_id, name) values(103, "George")')
                cur.execute('insert into Customer (customer_id, name) values(104, "Emily")')
                cur.execute('insert into Customer (customer_id, name) values(105, "Leo")')
                self.conn.commit()
                cur.execute('insert into Account (account_number, customer_id) values(201, 101)')
                cur.execute('insert into Account (account_number, customer_id) values(202, 101)')
                cur.execute('insert into Account (account_number, customer_id) values(203, 102)')
                cur.execute('insert into Account (account_number, customer_id) values(204, 102)')
                cur.execute('insert into Account (account_number, customer_id) values(205, 103)')
                cur.execute('insert into Account (account_number, customer_id) values(206, 104)')
                cur.execute('insert into Account (account_number, customer_id) values(207, 105)')
                self.conn.commit()
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(301, 201, 202, 500)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(302, 202, 203, 1000)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(303, 203, 204, 1500)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(304, 204, 205, 2000)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(305, 205, 201, 2500)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(306, 206, 207, 3000)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(307, 205, 201, 3500)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(308, 205, 201, 4000)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(309, 202, 203, 4500)')
                cur.execute('insert into Transaction '
                            '(transaction_id, sender_account_number, receiver_account_number, amount) '
                            'values(310, 201, 202, 5000)')
                self.conn.commit()
            print("data inserted")
        except pymysql.err.IntegrityError:
            print("Table Already Present")
        except Exception as e:
            print(e)
            exit()
