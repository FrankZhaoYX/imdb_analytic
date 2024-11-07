# IMDB Data Analysis project using Python, MySQL and Tableau
![MySQL Badge](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![Pandas Badge](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Beautiful Soup Badge](https://img.shields.io/badge/Beautiful_Soup-blue?style=for-the-badge)
![Tableau Badge](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=Tableau&logoColor=white)

### Summary
- This project used BeautifulSoup to mine movie metadata from the IMDb website, offering valuable experience in static web scraping and handling anti-scraping measures. Additionally, Tableau was used to visualize key insights from the raw dataset, providing a practical exercise in data extraction and analytics.

<img src="imdb_analytic.jpg?raw=true"/>

Inspired from Medium Article [IMDB Data Analysis project using Python, MySQL and Tableau](https://medium.com/@anitateladevalapalli777/imdb-data-analysis-project-using-python-mysql-and-tableau-758b7d0021db)

### 1. Main Techniques

- **BeautifulSoup** – Web scraping
- **Requests** – Data retrieval from web sources
- **Pandas** – Data cleaning and manipulation
- **MySQL** – Database storage and querying
- **Docker** – Containerization for environment setup
- **Tableau** – Data visualization and dashboard creation


### 2. Project details
- **BeautifulSoup** – Used for web scraping, specifically to retrieve each movie's name, and year.
```python
  def scrape_mv(self, container):
      # Scrape the name
      name = container.find('h3', class_ = 'ipc-title__text').get_text()
      self.names.append(name)
      logging.info(f"Current is scraping movie {name}")
      # Scrape the metadata
      # metadata_set = container.find_all('span', class_ = 'sc-b189961a-8 hCbzGp dli-title-metadata-item')
      metadata_set = container.find_all('span', class_ = "sc-ab348ad5-8 cSWcJI dli-title-metadata-item")
      year = metadata_set[0].get_text()
      self.years.append(year)
```
- **Requests** – Utilized for retrieving webpage data for each specified year, with robust error handling to manage potential exceptions such as HTTP errors, connection issues, and timeouts. The `bs4_parser` function below demonstrates this setup, where requests are made, errors are logged, and successful responses are parsed with BeautifulSoup:

```python
  def bs4_parser(self, url):
      try:
          # Make the GET request
          response = requests.get(url, headers=self.headers)
          response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
          
          # Process the response
          logging.info("Request was successful!")
          return BeautifulSoup(response.text, 'html.parser')
                  
      except requests.exceptions.HTTPError as http_err:
          logging.critical(f"HTTP error occurred: {http_err}")  # e.g., 404 or 500 error
      except requests.exceptions.ConnectionError:
          logging.critical("Connection error occurred. Please check your network.")
      except requests.exceptions.Timeout:
          logging.critical("The request timed out.")
      except requests.exceptions.RequestException as err:
          logging.critical(f"An error occurred: {err}")

      return None  # Return None if request fails
```
- **Pandas** – Used to transform and clean the data, then export it to CSV format to serve as the data source for injection into the MySQL server. This process ensures the data is well-structured and ready for efficient storage and querying within the database.
```python
        mv_containers = page_html.find_all('li', class_ = 'ipc-metadata-list-summary-item')
        # print(len(mv_containers))
        for container in mv_containers:
            self.scrape_mv(container)
            # break

        movie_raw = pd.DataFrame(
        {   'movie': self.names,
            'year': self.years,
            'length': self.lengths,
            'genres': self.genres,
            'US certificates': self.rating_years,
            'imdb': self.imdb_ratings,
            'metascore': self.metascores,
            'votes': self.votes,
            'reviews': self.reviews,
            'directors': self.directors,
            'writers': self.writers,
            'stars': self.stars,
            'contents': self.contents
        })
```
- **MySQL** – Used to import the CSV data into the MySQL server as part of the bronze layer, where raw data is stored. Additionally, MySQL is leveraged to transform and extract specific data into a silver layer, representing a more refined dataset ready for analysis.

```python
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
```

- **Docker** – Used for containerizing the environment, ensuring consistent and isolated setups for both the MySQL database and the Python application. The `docker-compose.yml` file below demonstrates a multi-container setup:

    ```yaml
    version: '3.8'

    services:
      mysql:
        image: mysql:8.0                    # Use MySQL 8.0 image
        container_name: mysql_server
        environment:
          MYSQL_ROOT_PASSWORD: admin        # Set a secure password
          MYSQL_DATABASE: IMDB_db           # Create a database named 'IMDB_db'
          MYSQL_USER: admin                 # Create a user named 'admin'
          MYSQL_PASSWORD: admin             # Password for 'admin'
        volumes:
          - mysql_data:/var/lib/mysql       # Persist MySQL data
        ports:
          - "3306:3306"

      python-app:
        build: ./app                        # Build the Python app using the Dockerfile
        container_name: IMDB_analysis_project
        volumes:
          - ./app:/usr/src/app              # Mount the local app directory
        working_dir: /usr/src/app
        depends_on:
          - mysql                           # Ensure MySQL starts first
        environment:
          MYSQL_HOST: mysql
          MYSQL_PORT: 3306
          MYSQL_USER: root
          MYSQL_PASSWORD: admin
          MYSQL_DATABASE: IMDB_db

    volumes:
      mysql_data:
    ```

This setup configures MySQL and a Python application service, with data persistence and environment variables for seamless integration. The `depends_on` setting ensures MySQL is ready before the Python app initializes, providing an efficient and reproducible project environment.



