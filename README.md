# IMDB Data Analysis project using Python, MySQL and Tableau
##
# Step 1 set local DB:
Deploy the local Mysql server through docker, and test it.
using Mysql 8.0 \
The config of [Mysql](./docker-compose.yml)
# Step 2 Scrap data:
Using Beautifulsoud to Scrap the information from IMDB website and inject it into mysql_server

Bronze data set total __546__

# Step 3 Clean the data:

Because In the bronze table, all the TV-seris data metascore is 0. In this case, the app extract data with metascore greater than 0 as silver level dataset. Regular the data from bronze_dataset. For example, transform the length from char to Time type, change vote and reviews from char to Int type.\
Silver data set total __487__


# Step 4: Extract more silver table for future analytic:
Silver table: Best_movie_each_year, distribute_by_genres
