import constant as constant
import mysql.connector
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Print to console (stdout)
        # logging.FileHandler("app.log")  # Optionally log to a file named app.log
    ]
)


def mysql_connect():
    MYSQL_HOST = os.getenv('MYSQL_HOST') or constant.my_sql_config.LOCAL_MYSQL_HOST
    MYSQL_PORT = os.getenv('MYSQL_PORT') or constant.my_sql_config.LOCAL_MYSQL_PORT
    MYSQL_USER = os.getenv('MYSQL_USER') or constant.my_sql_config.LOCAL_MYSQL_USER
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or constant.my_sql_config.LOCAL_MYSQL_PASSWORD
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE') or constant.my_sql_config.LOCAL_MYSQL_DATABASE
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
            logging.info(f"Successfully connected to MySQL database '{MYSQL_DATABASE}'")
            return connection
    except mysql.connector.Error as err:
        logging.critical("Error while connecting to MySQL", err)

def initial_db(db_name):
    conn = mysql_connect()
    cursor = conn.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}';")
    result = cursor.fetchone()
    if result:
        logging.info(f"Database '{db_name}' already exists.")
    else:
        cursor.execute(f"CREATE DATABASE '{db_name}';")
        cursor.execute("select database();")
        # Fetch and print the database name
        current_db = cursor.fetchone()
        for tmp in current_db:
            logging.info(f"Database selected: '{tmp}'")
    logging.info("Database is existed in server now")

