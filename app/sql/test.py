import db_api

db = db_api.db_manager()
db.initial_db("imdb")
db.use_db("imdb")