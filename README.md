# A Simple Website hosted in S3
This project Consist of a Simple UI hosted in Aws S3. This website takes customer Id as input and passes it to api
gateway which invokes a lambda function. This lambda function access the database created in rds mysql and return the
number of transaction and sum of amount back to website.
# Files
- **helper.py** - This file has the main function of the project. Flow of main the function -
    - Definition of all the parameter used in the project.
    - Upload the template and lambda python scripts to s3 bucket.
    - Creating or updating stack.
    - creation and insertion of data to database.
    - deployment of api gateway.
    - uploading the html file to s3.
    - opening the website in default browser.
- **stack.py** - This file contains a Stack class which handles all the stack functions like create, delete and  update a stack using boto3.
- **api_gateway.py** - This file contains a api class which handles all the api function like getting the api id, deployment of api.
- **function.py** - Comprises of upload functions like upload a folder, file or zip file to s3.
- **template.ymal** - A cloudforamtion template which comprises of configuration of database(rds), api gateway with a 
get method, api role, lambda function, lambda role, hosting s3 bucket.
- **database_creation_insertion.py** - This file contains a database class which handles all the database function like 
creating tables and inserting data in tables.
- **index.html** - This file contains a simple UI for the website.

# Output
A simple website is hosted in Aws S3 which returns the number of transaction made by the customer.
