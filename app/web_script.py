import requests
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np, pandas as pd
import time
import logging

class imdb_script:

    def bs4_parser(self, url):
        try:
            # Make the GET request
            response = requests.get(url, headers=self.headers)

            # Raise an exception for HTTP errors
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx, 5xx)

            # Process the response
            logging.info("Request was successful!")
            return BeautifulSoup(response.text, 'html.parser')
                    
        except requests.exceptions.HTTPError as http_err:
            logging.critical("HTTP error occurred: {}".format(http_err))  # e.g., 404 or 500 error
        except requests.exceptions.ConnectionError:
            logging.critical("Connection error occurred. Please check your network.")
        except requests.exceptions.Timeout:
            logging.critical("The request timed out.")
        except requests.exceptions.RequestException as err:
            logging.critical("An error occurred: {}".format(err))


    def metadata_scrape(self, url):
        # print(url)
        mv_info = self.bs4_parser(url)

        # Pause the loop
        sleep(randint(8,15))

        # Scrape the Gnere of movie
        genre_raw = mv_info.find_all('span', class_='ipc-chip__text')
        genre_set = []
        # print(genre_set)
        for tmp in genre_raw:
            # print(tmp.get_text())
            genre_set.append(tmp.get_text())
        self.genres.append(genre_set)


        raw = mv_info.find_all('li', attrs={'data-testid': 'title-pc-principal-credit'})
        # Scrape the Director
        # director_raw = mv_info.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
        # print(director_raw.get_text())
        director_raw = raw[0].find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        director_set = [tmp.get_text() for tmp in director_raw]
        # print(director_set)
        self.directors.append(director_set)

        # Scrape the Writer
        writer_raw = raw[1].find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        writer_set = [tmp.get_text() for tmp in writer_raw]
        # print(writer_set)
        self.writers.append(writer_set)


        # Scrape the Stars
        star_raw = raw[2].find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        star_set = [tmp.get_text() for tmp in star_raw]
        # print(star_set)
        self.stars.append(star_set)

        # Screape the number of reviews
        reviews_raw = mv_info.find('ul', class_= "ipc-inline-list sc-3243f83b-0 lazyWW baseAlt", attrs={'data-testid': 'reviewContent-all-reviews'})
        review = reviews_raw.find_all('span', class_='score')
        # print(review[0].get_text())
        self.reviews.append(review[0].get_text())

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
        length = metadata_set[1].get_text()
        self.lengths.append(length)
        rating_year = metadata_set[2].get_text()
        self.rating_years.append(rating_year)

        # Scrape the IMDB_rating
        imdb = float(container.find('span', class_= "ipc-rating-star--rating").get_text())
        self.imdb_ratings.append(imdb)

        # Scrape the votes
        vote_text = container.find('span', class_='ipc-rating-star--voteCount').get_text(strip=True)
        vote = vote_text.strip("()")
        self.votes.append(vote)

        # Scrape the Metasocre
        m_scroe = int(container.find("span", class_= "sc-b0901df4-0 bXIOoL metacritic-score-box").get_text())
        self.metascores.append(m_scroe)

        # Scrape the centent
        content = container.find('div', class_= "ipc-html-content-inner-div").get_text()
        self.contents.append(content)

        # Scrape Each movie Metadata 
        link = container.find('a', class_= "ipc-title-link-wrapper")['href']
        link = "http://www.imdb.com" + link
        self.metadata_scrape(link)
        


    def web_scrape(self):
        # For every year in the interval 2000-2022
        for year_url in self.years_url:
            # For every page in the interval 1-4
            for page in self.pages:
                if self.request_count > 0:
                    break
                start_time = time.time()
                # Make a get request
                url = 'https://www.imdb.com/search/title?release_date=' + year_url + '&sort=num_votes,desc&page=' + page
                # Parse the content of the request with BeautifulSoup
                page_html = self.bs4_parser(url)

                # Pause the loop
                sleep(randint(8,15))

                # Monitor the requests
                self.request_count += 1
                elapsed_time = time.time() - start_time
                logging.info('Request:{}; Frequency: {} requests/s'.format(self.request_count, self.request_count/elapsed_time))
                # clear_output(wait = True)

                # # Throw a warning for non-200 status codes
                # if response.status_code != 200:
                #     warn('Request: {}; Status code: {}'.format(requests, response.status_code))

                # Break the loop if the number of requests is greater than expected
                if self.request_count > 200:
                    logging.info('Number of requests was greater than expected.')
                    break

                mv_containers = page_html.find_all('li', class_ = 'ipc-metadata-list-summary-item')
                # print(len(mv_containers))
                for container in mv_containers:
                    self.scrape_mv(container)
                    break

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
        return movie_raw

    def __init__(self):
        self.names = []
        self.years = []
        self.lengths = []
        self.rating_years = []
        self.imdb_ratings = []
        self.metascores = []
        self.votes = []
        self.contents = []
        self.genres = []
        self.directors = []
        self.writers = []
        self.stars = []
        self.reviews=[]
        self.years_url = [str(i) for i in range(2000,2022)]
        self.pages = [str(i) for i in range(1,10)]
        # Preparing the monitoring of the loop
        self.request_count = 0
        self.runtimes=[]
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

