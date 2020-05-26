## Use case
Run SQL query directly on a database via an API call, currently only select query's and setup for SQL Server only.

## Installation and Configuration
Install Python 3.7, the 64 bit Windows installer can be found [here](https://www.python.org/downloads/release/python-377/), **ensure you check add to path during installation**.

<sup>*(Note that this app will not work with Python 3.8+ as packages used have not yet been updated to support the newer version of Python)*</sup>

Clone this repo, navigate to the downloaded repo folder using command line tool and run the command:

 `pip install -r requirements.txt`
 
 This will use the Python package manager to download and install all the required packages.

In the config<i></i>.py file provide your own database connection details, save the file with your new details.

<sup>*Example config<i></i>.py file*</sup>

    USERNAME = 'Anthony.ODonnell'
    PASSWORD = 'admin'
    SERVER = 'mydb.co.uk'
    

## Run App
Using the command line from the downloaded repo folder run the following command

    flask run
This starts the application running and it will now be listening for requests on http://localhost:5000/

If you need the application be accessible from another computer then run the following command

    flask run --host=0.0.0.0
**Be aware this application is only for local development and not production ready!**

## Use App
Using Postman, you can now post a request with *Content-type* header of *application/json* to following end point:

    http://localhost:5000/DB/select

Replace DB in the URL with the name of the database you wish to run the query against, the end point only expects post requests and is expecting a JSON body containing the SQL query to be ran in this format:

    {"query": "select * from users"}
    
When running more complicated SQL queries you may need to escape some characters with a backslash to avoid breaking the JSON formatting, it is possible to use Postman variables in the JSON body being sent.
