from sql import db_api
import web_script
import logging
import pandas as pd


def main():
    logging.basicConfig(
    level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Print to console (stdout)
        # logging.FileHandler("app.log")  # Optionally log to a file named app.log
    ]
)
    db_manager = db_api.db_manager()

    db_manager.use_db("imdb")

    sql_tmp = """CREATE TABLE bronze_dataset(
    movie varchar(255) NOT NULL,
    year varchar(255) NOT NULL,
    length varchar(255) NOT NULL,
    genre varchar(255) NOT NULL,
    US_certificates varchar(10) NOT NULL,
    imdb float NOT NULL,
    metascore int NOT NULL,
    votes int NOT NULL,
    reviews varchar(10) NOT NULL,
    directors varchar(255) NOT NULL,
    writers varchar(255) NOT NULL,
    stars varchar(255) NOT NULL,
    contents varchar(255) NOT NULL
    );"""
    db_manager.create_table(sql_tmp,"bronze_dataset")

    logging.info("table bronze_dataset is created")

    imdb_scrape_driver = web_script.imdb_script()
    imdb_raw = imdb_scrape_driver.web_scrape()
    logging.info(imdb_raw.info())
    for i, row in imdb_raw.iterrows():
        # sql = "INSERT INTO imdb.bronze_dataset VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        sql = "INSERT INTO imdb.movie_raw_db VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        tuple_transformed = ()
        for column in imdb_raw.columns:
            if isinstance(row[column],list):
                tmp_value = ""
                print(row[column])
                for tmp in row[column]:
                    tmp_value += tmp +', '
                tuple_transformed +=(tmp_value,)
            else:
                tuple_transformed += (row[column],)
            print(f"Column: {column}, Value: {row[column]}, Data Type: {type(row[column])}")
        print("-------")
        print(tuple_transformed)
        db_manager.insert_table(sql,tuple_transformed)
        db_manager.CONN.commit()

if __name__ == "__main__":
    main()
    