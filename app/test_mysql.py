# app.py
import mysql.connector
import os

# Fetch MySQL connection details from environment variables
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    if connection.is_connected():
        print(f"Successfully connected to MySQL database '{MYSQL_DATABASE}'")
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table)
        else:
            print("No tables found in the database.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection closed.")
