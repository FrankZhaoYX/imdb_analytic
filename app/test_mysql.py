import web_script
import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Print to console (stdout)
        # logging.FileHandler("app.log")  # Optionally log to a file named app.log
    ]
)

test = web_script.imdb_script()

test = test.web_scrape()

pd.set_option('display.max_rows', 100)  # Default is 60
pd.set_option('display.max_columns', 20)  # Default is 20

print(test)

