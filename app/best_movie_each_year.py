from sql import db_api

db_manager = db_api.db_manager()

db_manager.use_db("imdb")

# dump bronze functions to a silver_raw

sql_query = "Create Table best_movie_each_year as SELECT ,MAX(metascore) FROM silver_dataset WHERE Metascore > 0;"
db_manager.CURSOR.execute(sql_query)

# Fetch all rows from the executed query
outcome_1 = db_manager.CURSOR.fetchall()

# Print the result
for row in outcome_1:
    print(row)