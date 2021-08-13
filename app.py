import struct
from datetime import datetime, timedelta
import json
import pyodbc
import config
from flask import Flask, Response, request, jsonify
app = Flask(__name__)


@app.route('/')
def root_route():
    return Response("Its running!", 200)


@app.route('/<db>/query', methods=['GET', 'POST'])
def select_route(db):
    try:
        database = db
        data = request.get_json()
        query = data["query"]
        query = (query)
    except Exception as e:
        template = "Failed to get database or query from request \n An exception of type {0} occurred. \n Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        return message
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.SERVER +
                              ';DATABASE='+database+';UID='+config.USERNAME+';PWD=' + config.PASSWORD)
    except Exception as e:
        template = "Failed to connect to database \n An exception of type {0} occurred. \n Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        return message

    def convertDateTimeObjectToTimeStamp(fromConvertor):
        # https://stackanswers.net/questions/how-do-i-unpack-a-sql-server-datetime-in-a-pyodbc-output-converter-function
        result = struct.unpack("<2l", fromConvertor)
        days_since_1900 = result[0]
        partial_day = round(result[1] / 300.0, 3)
        date_time = datetime(
            1900, 1, 1) + timedelta(days=days_since_1900) + timedelta(seconds=partial_day)
        return date_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:23]

    try:
        cursor = cnxn.cursor()
        cursor.execute(query)
        cnxn.add_output_converter(
            pyodbc.SQL_TYPE_TIMESTAMP, convertDateTimeObjectToTimeStamp)
        description = cursor.description
        column_names = [col[0] for col in description]
        data = [dict(zip(column_names, row))
                for row in cursor.fetchall()]
        output = json.dumps(data, indent=4)
        return Response(output, 200, {'Content-Type': 'application/json;'})
    except Exception as e:
        template = "Failed to run query supplied. An exception of type {0} occurred.\nArguments:{1!r}"
        message = template.format(type(e).__name__, e.args)
        return Response(message, 400)
    finally:
        cursor.close()
        cnxn.close()


@app.route('/<db>/commit', methods=['GET', 'POST'])
def update_route(db):
    message = jsonify({"Message": "Not implemented."})
    return (message, 503)


@app.errorhandler(404)
def page_not_found(e):
    nothing_here = jsonify({'error': 'Cannot find what you requested.'})
    return (nothing_here, 404)


@app.errorhandler(500)
def page_not_found(e):
    nothing_here = jsonify({'error': 'Something went wrong.'})
    return (nothing_here, 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)