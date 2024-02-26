import log.log as log
from scrapper.webscrapper import *
from config.config import configuration
import pandas as pd

_root_logger = log.setup_custom_logger("root")

base_url = configuration.get_property("base_url")
categories = configuration.get_property("categories")

def main():
    _root_logger.info(f"Process Execution Started.\n")
    for category in categories:
        products_list = []  # Initialize list to store product data
        product_counter = 0  # Initialize product counter
        page = 1
        while True:
            url_with_pagination = f"{base_url}{category}/?page={page}"
            _root_logger.info(f"\nScraping {url_with_pagination}")
            _root_logger.info(f"Scraping......\n")
            
            html = get_data(url_with_pagination)
            if html:
                found_products = parse_data(html, products_list, product_counter)
                if not found_products:
                    _root_logger.info("Reached the end of the product listings.")
                    break
            else:
                break
            page += 1
        
        # Convert the list of dictionaries into a Pandas DataFrame
        df = pd.DataFrame(products_list)
        # Save the DataFrame to a CSV file
        df.to_csv(f'./archive/{category}.csv', index=False, encoding='utf-8-sig')
        _root_logger.info(f"Total products scraped from {category} category: {len(products_list)}\n")
        _root_logger.info(f"Data saved to {category}.csv\n")
    _root_logger.info(f"Process Execution Ended.")

if __name__ == '__main__':
    main()