import pymysql
HOST = "wd103rfhtoh99dg.cumd1mkctnev.ap-south-1.rds.amazonaws.com"
USERNAME = "admin"
PASSWORD = "admin123"
DATA_BASE_NAME = "sample_db"
try:
    conn = pymysql.connect(HOST,
                           user=USERNAME,
                           passwd=PASSWORD,
                           db=DATA_BASE_NAME,
                           connect_timeout=5)
except pymysql.MySQLError as e:
    print(e)
    exit()
with conn.cursor() as cur:
    cur.execute("select count(*) from Transaction t inner join Account a on t.sender_account_number = a.account_number inner join Customer c on a.customer_id = c.customer_id where c.customer_id  = 101")
    for row in cur:
        print(row[0])