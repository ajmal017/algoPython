import mysql.connector
import json


def dbConnect(environment):
    # Read JSON data into the datastore variable
    with open('config.json') as json_file:
        data = json.load(json_file)

    # Connect to Database
    try:
        mydb = mysql.connector.connect(
            host=data[environment]['dbName'],
            user=data[environment]['userName'],
            passwd=data[environment]['password'],
            database=data[environment]['schema'],
            port=data[environment]['port'],
        )

        return mydb
    except:
        return 0
