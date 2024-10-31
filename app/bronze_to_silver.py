from sql import db_api
from datetime import timedelta
import re


def convert_duration_to_time_str(duration_str):
    # Split the duration string into hours and minutes
    parts = duration_str.split()
    hours = 0
    minutes = 0
    
    for part in parts:
        if 'h' in part:
            hours = int(part[:-1])  # Remove the 'h' and convert to int
        elif 'm' in part:
            minutes = int(part[:-1])  # Remove the 'm' and convert to int
            
    # Format as HH:MM:SS
    return f"{hours:02}:{minutes:02}:00"

def convert_vote_reviews(input):
    try:
        match = re.match(r'([\d.]+)([a-zA-Z])', input)
        number = float(match.group(1))   
        postfix = match.group(2) 
        if postfix == 'K':
            return int(number * 1000)
        if postfix == 'M':
            return int(number * 1000000)
        else:
            return 0
    except:
        return int(input)


db_manager = db_api.db_manager()

db_manager.use_db("imdb")

# Step 1: Select valid data from the bronze_dataset where Metascore > 0
sql_query = "SELECT * FROM bronze_dataset WHERE Metascore > 0;"
db_manager.CURSOR.execute(sql_query)

# Fetch all rows from the executed query (this is the valid data)
bronze_data = db_manager.CURSOR.fetchall()

#  Step 2: Now, create the silver_dataset table based on this valid data
# Create table `silver_dataset` with the fomulated structure 
sql_tmp = """CREATE TABLE silver_dataset(
movie varchar(255) NOT NULL,
year int NOT NULL,
length TIME NOT NULL,
genre varchar(255) NOT NULL,
US_certificates varchar(10) NOT NULL,
imdb float NOT NULL,
metascore int NOT NULL,
votes int NOT NULL,
reviews int NOT NULL,
directors varchar(255) NOT NULL,
writers varchar(255) NOT NULL,
stars varchar(255) NOT NULL,
contents varchar(255) NOT NULL
);"""
db_manager.create_table(sql_tmp,"silver_dataset")

silver_data = list()
# Print the fetched rows to inspect the data (optional, for debugging)
for row in bronze_data:
    tmp_tuple=()
    # clean the prefix
    movie = row[0]
    movie= movie.split('. ', 1)[1]
    tmp_tuple = tmp_tuple + (movie,)
    year = row[1]
    tmp_tuple = tmp_tuple + (year,)
    # change from string to time
    length = convert_duration_to_time_str(row[2])
    tmp_tuple = tmp_tuple + (length,)

    genre = row[3]
    tmp_tuple = tmp_tuple + (genre,)


    US_certificates = row[4]
    tmp_tuple = tmp_tuple + (US_certificates,)

    imdb = row[5]
    tmp_tuple = tmp_tuple + (imdb,)

    metascore = row[6]
    tmp_tuple = tmp_tuple + (metascore,)

    # Transform vote and reviews to numeric
    votes = convert_vote_reviews(row[7])
    tmp_tuple = tmp_tuple + (votes,)

    reviews = convert_vote_reviews(row[8])
    tmp_tuple = tmp_tuple + (reviews,)
    
    directors = row[9]
    tmp_tuple = tmp_tuple + (directors,)

    writers = row[10]
    tmp_tuple = tmp_tuple + (writers,)

    stars = row[11]
    tmp_tuple = tmp_tuple + (stars,)

    contents = row[12]
    tmp_tuple = tmp_tuple + (contents,)
    silver_data.append(tmp_tuple)

insert_query = "INSERT INTO silver_dataset VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"  # Adjust column count based on table

# Insert the valid data from bronze_data into silver_dataset
db_manager.CURSOR.executemany(insert_query, silver_data)

# Commit the transaction to save changes
db_manager.CONN.commit()

print("Data from bronze_dataset has been successfully inserted into silver_dataset.")