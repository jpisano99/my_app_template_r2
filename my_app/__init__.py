import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from my_app.settings import app_cfg, db_config
from base64 import b64encode
from my_app.my_secrets import passwords

app = Flask(__name__)

# Assign App Config Variables / Create a random token for Flask Session
token = os.urandom(64)
token = b64encode(token).decode('utf-8')
app.config['SECRET_KEY'] = token

# Where am I ?
if os.getenv("PYTHONANYWHERE_DOMAIN") is None:
    python_anywhere = False
else:
    python_anywhere = True

# Get the Passwords and Keys
print()
print("\tI have a DB Password: ", my_secrets.passwords["DB_PASSWORD"])
print("\tI have an API Key: ", my_secrets.passwords["SS_TOKEN"])
print("\tI have an Flask Secret Key: ", app.config['SECRET_KEY'])
print("\tPythonAnywhere detection is:", python_anywhere)
print()

#
# database connection settings
#
if python_anywhere is True:
    # This is for a local SQL Server
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' +\
                                                db_config['USER'] +\
                                            ':'+db_config['PASSWORD'] +\
                                            '@'+db_config['HOST']+':3306'
else:
    # This is for pythonAnywhere it requires "import MySQLdb"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' +\
                                                db_config['USER'] +\
                                            ':'+db_config['PASSWORD'] +\
                                            '@'+db_config['HOST']

print('\t\tDatabase Connection String:', app.config['SQLALCHEMY_DATABASE_URI'])

# Create an engine and connect to the engine / server
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])  # connect to server

# Create DEFAULT Database from the Settings file
engine.execute("CREATE SCHEMA IF NOT EXISTS `" + db_config['DATABASE'] + "`;")  # create db
engine.execute("USE " + db_config['DATABASE'] + ";")  # select new db

# Update the URI and attach the schema
# app.config['SQLALCHEMY_BINDS']= {
#     'dev':        'mysqldb://localhost/users',
#     'prod':       'sqlite:////path/to/appmeta.db'
# }
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] + "/" + db_config['DATABASE']
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#
# # Create db for SQL Alchemy
db = SQLAlchemy(app)

# Are we connected ?
db_host = []
db_port = []
db_user = []
db_status = (db.engine.execute("SHOW VARIABLES WHERE Variable_name = 'port'"))
for x in db_status:
    db_port = x.values()

db_status = (db.engine.execute("SHOW VARIABLES WHERE Variable_name = 'hostname'"))
for x in db_status:
    db_host = x.values()

db_status = (db.engine.execute('SELECT USER()'))
for x in db_status:
    db_user = x.values()

print('\tYou are connected to MySQL Host '+db_host[1]+' on Port '+db_port[1]+' as '+db_user[0])


from my_app import views
from my_app import models
