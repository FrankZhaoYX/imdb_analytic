from requests import get
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

years_url = [str(i) for i in range(2000,2022)]
pages = [str(i) for i in range(1,10)]



# Preparing the monitoring of the loop

requests = 0
runtimes=[]


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

def metadata_scrape(url):
    print(url)

# For every year in the interval 2000-2022
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:
        if requests > 11:
            break
        start_time = time.time()
        # Make a get request
        response = get('https://www.imdb.com/search/title?release_date=' + year_url +
        '&sort=num_votes,desc&page=' + page, headers = headers)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time.time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        # clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 200:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

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
            # print(name)
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
            link = "www.imdb.com" + link
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