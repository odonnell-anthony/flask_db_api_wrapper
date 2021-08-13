## Use case
Run SQL query directly on a SQL Server database via an API call, currently only select query's.

## Configuration
In the config<i></i>.py file provide your own database connection details, save the file with your new details.

<sup>*Example config<i></i>.py file*</sup>

    USERNAME = 'Anthony.ODonnell'
    PASSWORD = 'admin'
    SERVER = 'mydb.co.uk'
    

------------


## Run App (Without Docker)
Install Python 3.7, the 64 bit Windows installer can be found [here](https://www.python.org/downloads/release/python-377/), **ensure you check add to path during installation**.

Clone this repo, navigate to the downloaded repo folder using command line tool and run the command:
```
pip install -r requirements.txt
```
Set environment variables, commands below are for powershell:
```
$env:FLASK_APP = 'app.py'
$env:FLASK_ENV = 'Development'
```
 
Run the application with the following command:
```
flask run
```
This starts the application running and it will now be listening for requests on http://localhost:5000/

#### Options
By default the application will run on port 5000 and only be available via local 127.0.0.1 or localhost, you can change this with the flask run options.
You can set the host option with `-h` or `--host` to set the interface and the port option with `-p` or `--port` setting what they are bound to:
```
flask run --host=0.0.0.0 --port 80
```
The above command makes the application available  from any other machine on the local network via the hosts IP and it is running on port 80.
Use `flask run --help` for further options.

------------

**Be aware this application is only for local development and not production ready!**

------------



## Run App using Docker
Build with command:
```
docker-compose build
```
Run in the background with command:
```
docker-compose up -d
```
The application will now be available from any other machine on the local network via the hosts IP running on port 80.

View logs with command:
```
docker-compose logs --tail 10 api_db_wrapper
```

Stop the application running with:
```
docker-compose down
```

------------


## Use App
Using Postman, you can now post a request with *Content-type* header of *application/json* to following end point:

    http://localhost:5000/DB/query

Replace DB in the URL with the name of the database you wish to run the query against, the end point only expects post requests and is expecting a JSON body containing the SQL query to be ran in this format:

    {"query": "select * from users"}
    
When running more complicated SQL queries you may need to escape some characters with a backslash to avoid breaking the JSON formatting, it is possible to use Postman variables in the JSON body being sent.