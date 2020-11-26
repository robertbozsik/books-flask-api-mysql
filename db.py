# 1. pip3 install pymysql
# https://pymysql.readthedocs.io/en/latest/user/examples.html
# 2. pip3 install python-dotenv
# python-dotenv reads the key-value pair from .env file and adds them to environment variable.
# https://pypi.org/project/python-dotenv/


import os
from dotenv import load_dotenv
from pathlib import Path
import pymysql
# import getpass


# explicitly providing path to '.env'
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# connecting to a local MySQL database
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user=os.getenv('MY_SQL_USER'),
    # password=getpass.getpass(),
    password=os.getenv('MY_SQL_PASSWORD'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

create_database = 'CREATE DATABASE IF NOT EXISTS books'
use_database = 'USE books'
create_table = """ CREATE TABLE IF NOT EXISTS books (
                    id INT NOT NULL AUTO_INCREMENT,
                    author VARCHAR(255) NOT NULL,
                    language VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    PRIMARY KEY(id)
                ) """

cursor = connection.cursor()

cursor.execute(create_database)
cursor.execute(use_database)
cursor.execute(create_table)

# connection is not autocommit by default. So you must commit to save your changes.
connection.commit()
connection.close()
