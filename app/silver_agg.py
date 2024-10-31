from sql import db_api

db_manager = db_api.db_manager()

db_manager.use_db("imdb")

sql_tmp = """CREATE TABLE imdb_genre(
genre varchar(255) NOT NULL,
frequency int NOT NULL
);"""

db_manager.create_table(sql_tmp,"imdb_genre")

# Aggregation distribute_by_year
sql_query = "SELECT genre from silver_dataset "
db_manager.CURSOR.execute(sql_query)

distribute_by_year = db_manager.CURSOR.fetchall()

genre_dict = {}

for row in distribute_by_year:
    # Split the string by commas and strip any leading/trailing spaces from each item
    genres_list = [genre.strip() for genre in row[0].split(',')]
    genres_list.pop()
    for tmp in genres_list:
        if tmp not in genre_dict:
            genre_dict[tmp]=1
        else:
            genre_dict[tmp] = genre_dict[tmp] + 1
    # print(genres_list)
# print(genre_dict)
for key, value in genre_dict.items():
    sql = "INSERT INTO imdb.imdb_genre VALUES (%s,%s);"
    tuple_tmp = (key,value)
    db_manager.insert_table(sql,tuple_tmp)
    db_manager.CONN.commit()