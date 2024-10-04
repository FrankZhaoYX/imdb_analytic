import constant as constant
import mysql.connector
import os
import logging


class db_manager:

    CONN = None
    CURSOR = None
    db = None

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Print to console (stdout)
            # logging.FileHandler("app.log")  # Optionally log to a file named app.log
        ]
    )


    # def mysql_connect():
    #     MYSQL_HOST = os.getenv('MYSQL_HOST') or constant.my_sql_config.LOCAL_MYSQL_HOST
    #     MYSQL_PORT = os.getenv('MYSQL_PORT') or constant.my_sql_config.LOCAL_MYSQL_PORT
    #     MYSQL_USER = os.getenv('MYSQL_USER') or constant.my_sql_config.LOCAL_MYSQL_USER
    #     MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or constant.my_sql_config.LOCAL_MYSQL_PASSWORD
    #     MYSQL_DATABASE = os.getenv('MYSQL_DATABASE') or constant.my_sql_config.LOCAL_MYSQL_DATABASE
    #     # Connect to the MySQL database
    #     try:
    #         connection = mysql.connector.connect(
    #             host=MYSQL_HOST,
    #             port=MYSQL_PORT,
    #             user=MYSQL_USER,
    #             password=MYSQL_PASSWORD,
    #             database=MYSQL_DATABASE
    #         )

    #         if connection.is_connected():
    #             logging.info(f"Successfully connected to MySQL database '{MYSQL_DATABASE}'")
    #             return connection
    #     except mysql.connector.Error as err:
    #         logging.critical("Error while connecting to MySQL", err)

    def use_db(self, db_name):
        self.CURSOR.execute(f"use {db_name};")
        logging.info(f"Using database: {db_name}")
        self.db = db_name



    def initial_db(self,db_name):
        self.CURSOR.execute(f"SHOW DATABASES LIKE '{db_name}';")
        result = self.CURSOR.fetchone()
        if result:
            logging.info(f"Database '{db_name}' already exists.")
        else:
            self.CURSOR.execute(f"CREATE DATABASE '{db_name}';")
            self.CURSOR.execute("select database();")
            # Fetch and print the database name
            current_db = self.CURSOR.fetchone()
            for tmp in current_db:
                logging.info(f"Database selected: '{tmp}'")
        logging.info("Database is existed in server now")

    # def create_table(sql_query):
    #     conn = mysql_connect()
    #     cursor = conn.cursor()
    #     cursor.execute("use imdb;")

    def __init__(self):
        MYSQL_HOST = os.getenv('MYSQL_HOST') or constant.my_sql_config.LOCAL_MYSQL_HOST
        MYSQL_PORT = os.getenv('MYSQL_PORT') or constant.my_sql_config.LOCAL_MYSQL_PORT
        MYSQL_USER = os.getenv('MYSQL_USER') or constant.my_sql_config.LOCAL_MYSQL_USER
        MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or constant.my_sql_config.LOCAL_MYSQL_PASSWORD
        MYSQL_DATABASE = os.getenv('MYSQL_DATABASE') or constant.my_sql_config.LOCAL_MYSQL_DATABASE
        # Connect to the MySQL database
        try:
            self.CONN = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )

            if self.CONN.is_connected():
                logging.info(f"Successfully connected to MySQL database '{MYSQL_DATABASE}'")
                self.CURSOR = self.CONN.cursor()
        except mysql.connector.Error as err:
            logging.critical("Error while connecting to MySQL", err)
