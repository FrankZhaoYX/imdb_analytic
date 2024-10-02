import requests
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np, pandas as pd
import time

names = []

years = []
lengths = []
rating_years = []

imdb_ratings = []
metascores = []
votes = []
contents = []

genres = []

directors = []
writers = []
stars = []

reviews=[]

years_url = [str(i) for i in range(2000,2022)]
pages = [str(i) for i in range(1,10)]



# Preparing the monitoring of the loop

request_count = 0
runtimes=[]


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

def bs4_parser(url):
    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Raise an exception for HTTP errors
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx, 5xx)

        # Process the response
        print("Request was successful!")
        return BeautifulSoup(response.text, 'html.parser')
                
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred: {}".format(http_err))  # e.g., 404 or 500 error
    except requests.exceptions.ConnectionError:
        print("Connection error occurred. Please check your network.")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as err:
        print("An error occurred: {}".format(err))


def metadata_scrape(url):
    print(url)
    mv_info = bs4_parser(url)

    # Pause the loop
    sleep(randint(8,15))

    # Scrape the Gnere of movie
    genre_raw = mv_info.find_all('span', class_='ipc-chip__text')
    genre_set = []
    # print(genre_set)
    for tmp in genre_raw:
        # print(tmp.get_text())
        genre_set.append(tmp.get_text())
    genres.append(genre_set)


    raw = mv_info.find_all('li', attrs={'data-testid': 'title-pc-principal-credit'})
    # Scrape the Director
    # director_raw = mv_info.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
    # print(director_raw.get_text())
    director_raw = raw[0].find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
    director_set = [tmp.get_text() for tmp in director_raw]
    # print(director_set)
    directors.append(director_set)

    # Scrape the Writer
    writer_raw = raw[1].find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
    writer_set = [tmp.get_text() for tmp in writer_raw]
    # print(writer_set)
    writers.append(writer_set)


    # Scrape the Stars
    star_raw = raw[2].find_all('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
    star_set = [tmp.get_text() for tmp in star_raw]
    # print(star_set)
    stars.append(star_set)

    # Screape the number of reviews
    reviews_raw = mv_info.find('ul', class_= "ipc-inline-list sc-3243f83b-0 lazyWW baseAlt", attrs={'data-testid': 'reviewContent-all-reviews'})
    review = reviews_raw.find_all('span', class_='score')
    # print(review[0].get_text())
    reviews.append(review[0].get_text())
   
    



# For every year in the interval 2000-2022
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:
        if request_count > 1:
            break
        start_time = time.time()
        # Make a get request
        url = 'https://www.imdb.com/search/title?release_date=' + year_url + '&sort=num_votes,desc&page=' + page
        # Parse the content of the request with BeautifulSoup
        page_html = bs4_parser(url)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        request_count += 1
        elapsed_time = time.time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(request_count, request_count/elapsed_time))
        # clear_output(wait = True)

        # # Throw a warning for non-200 status codes
        # if response.status_code != 200:
        #     warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if request_count > 200:
            warn('Number of requests was greater than expected.')
            break


        # print("page_html is ")
        # print('https://www.imdb.com/search/title?release_date=' + year_url +
        # '&sort=num_votes,desc&page=' + page)

        # Select all the 50 movie containers from a single page
        mv_containers_1 = page_html.find_all('div', class_ = 'ipc-metadata-list-summary-item__tc')
        mv_containers_2 = page_html.find_all('div', class_ = 'ipc-metadata-list-summary-item__c')

        # For every movie of these 50 top 25
        for container in mv_containers_1:
            # Scrape the name
            name = container.find('h3', class_ = 'ipc-title__text').get_text()
            names.append(name)
            print(name)
            # Scrape the metadata
            # metadata_set = container.find_all('span', class_ = 'sc-b189961a-8 hCbzGp dli-title-metadata-item')
            metadata_set = container.find_all('span', class_ = "sc-ab348ad5-8 cSWcJI dli-title-metadata-item")
            year = metadata_set[0].get_text()
            years.append(year)
            length = metadata_set[1].get_text()
            lengths.append(length)
            rating_year = metadata_set[2].get_text()
            rating_years.append(rating_year)

            # Scrape the IMDB_rating
            imdb = float(container.find('span', class_= "ipc-rating-star--rating").get_text())
            imdb_ratings.append(imdb)

            # Scrape the votes
            vote_text = container.find('span', class_='ipc-rating-star--voteCount').get_text(strip=True)
            vote = vote_text.strip("()")
            votes.append(vote)

            # Scrape the Metasocre
            m_scroe = int(container.find("span", class_= "sc-b0901df4-0 bXIOoL metacritic-score-box").get_text())
            metascores.append(m_scroe)

            # Scrape the centent
            content = container.find('div', class_= "ipc-html-content-inner-div").get_text()
            contents.append(content)

            # Scrape Each movie Metadata 
            link = container.find('a', class_= "ipc-title-link-wrapper")['href']
            link = "http://www.imdb.com" + link
            metadata_scrape(link)

names = []

years = []
lengths = []
rating_years = []

imdb_ratings = []
metascores = []
votes = []
contents = []

# 'genres': genres,


movie_ratings = pd.DataFrame({'movie': names,
'year': years,
'length': lengths,
'US certificates': rating_years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
})
print(movie_ratings.info())
movie_ratings.head(10)