import mysql.connector
import json

# Read JSON data into the datastore variable
with open('config.json') as json_file:
    data = json.load(json_file)

# Use the new datastore datastructure
print(data['staging']['dbName'])

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="yourusername",
#     passwd="yourpassword"
# )

# print(mydb)

# function dbConnect(environment) {
#   return new Promise((resolve, reject) => {
#     let host = config[environment].dbName;
#     let user = config[environment].userName;
#     let password = config[environment].password;
#     let schema = config[environment].schema;
#     let port = config[environment].port;

#     //Create connection to mySQL
#     var con = mysql.createConnection({
#       host: host,
#       user: user,
#       password: password,
#       database: schema,
#       port: port
#     });
#     //Connect to DB
#     con.connect(function(err) {
#       if (err) reject(err);
#       else {
#         console.log("Connected to mySQL database successfully.");
#         resolve(con);
#       }
#     });
#   });
# }

# function dbEndConnection(con) {
#   con.end();
#   return 1;
# }

# module.exports.dbConnect = dbConnect;
# module.exports.dbEndConnection = dbEndConnection;
