import mysql.connector
import json


def dbConnect():
    # Read JSON data into the datastore variable
    with open('config.json') as json_file:
        data = json.load(json_file)

    # Connect to Database
    try:
        mydb = mysql.connector.connect(
            host=data['staging']['dbName'],
            user=data['staging']['userName'],
            passwd=data['staging']['password'],
            database=data['staging']['schema'],
            port=data['staging']['port'],
        )

        return mydb
    except:
        return 0
