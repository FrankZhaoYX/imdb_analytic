import db_api

db = db_api.db_manager()
db.initial_db("imdb")
db.use_db("imdb")
sql1= """CREATE TABLE movie_raw_db(
    movie varchar(255),
    year varchar(255),
    length varchar(255),
    genre varchar(255),
    US_certificates varchar(10),
    imdb float,
    metascore int,
    votes varchar(10),
    reviews varchar(10),
    directors varchar(255),
    writers varchar(255),
    stars varchar(255),
    contents varchar(255)
    );"""
db.create_table(sql1,"movie_raw_db")
db.check_table("movie_raw_db")
