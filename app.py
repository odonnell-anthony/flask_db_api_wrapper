from flask import Flask, Response, request, jsonify
app= Flask(__name__)
import config
import pyodbc
import json




@app.route('/')
def root_route():
        return Response("Its running!", 200)


@app.route('/<db>/select', methods = ['POST'])
def select_route(db):
        try:
                database = db
                data = request.get_json()
                query=data["query"]
                query = (query)
        except Exception as e:
                template = "Failed to get database or query from request \n An exception of type {0} occurred. \n Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                return message
        try:
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.SERVER+';DATABASE='+database+';UID='+config.USERNAME+';PWD='+ config.PASSWORD)
        except Exception as e:
                template = "Failed to connect to database \n An exception of type {0} occurred. \n Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                return message
        try:
                cursor = cnxn.cursor()
                cursor.execute(query)
                description = cursor.description
                column_names = [col[0] for col in description]
                #print(column_names)
                data = [dict(zip(column_names, row))
                        for row in cursor.fetchall()]
                output = json.dumps(data, indent=4)
                #print(output)
                return Response(output, 200, {'Content-Type': 'application/json;'})
        except Exception as e:
                template = "Failed to run query supplied \n An exception of type {0} occurred. \n Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                return message
        finally:
                cursor.close()
                cnxn.close()

@app.route('/<db>/insert', methods = ['GET', 'POST'])
def insert_route(db):
        message = jsonify({"Message": "Not implemented as of yet"})
        return (message, 503)

@app.route('/<db>/update', methods = ['GET', 'POST'])
def update_route(db):
        message = jsonify({"Message": "Not implemented as of yet"})
        return (message, 503)

@app.route('/<db>/delete', methods = ['GET', 'POST'])
def delete_route(db):
        message = jsonify({"Message": "Not implemented as of yet"})
        return (message, 503)

@app.errorhandler(404)
def page_not_found(e):
    nothing_here = jsonify({'error': 'cannot find what you requested'})
    return (nothing_here, 404)