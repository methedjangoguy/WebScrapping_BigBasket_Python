import os
from datetime import datetime, timedelta
import logging
from config.config import configuration
import requests
from bs4 import BeautifulSoup

_scrape_logger = logging.getLogger("webscrapper")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_data(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            _scrape_logger.error(f"Failed to retrieve content, status code: {response.status_code}")
            return None
    except Exception as e:
        _scrape_logger.error(f"An error occurred: {e}")
        return None

def parse_data(html, products_list, counter):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.findAll('div', class_='SKUDeck___StyledDiv-sc-1e5d9gk-0 eA-dmzP')
    if not products:
        # No products found, likely reached the end of the listings
        return False
    
    for product in products:
        try:
            product_brand_name = product.find('span', class_='Label-sc-15v1nk5-0 BrandName___StyledLabel2-sc-hssfrl-1 gJxZPQ keQNWn').text.strip()
            if not product_brand_name:  # Checks if name is empty
                raise ValueError("Name not found")
        except Exception:
            product_brand_name = "No Manufacturer Name"

        try:
            product_name = product.find('h3', class_='block m-0 line-clamp-2 font-regular text-base leading-sm text-darkOnyx-800 pt-0.5 h-full').text.strip()
            if not product_name:  # Checks if name is empty
                raise ValueError("Name not found")
        except Exception:
            product_name = "No Product Name"

        product_quantity = "No Product Quantity"
        try:
            product_quantity = product.find('span', class_='Label-sc-15v1nk5-0 PackChanger___StyledLabel-sc-newjpv-1 gJxZPQ cWbtUx').text.strip()
            if not product_quantity:  # Checks if name is empty
                raise ValueError("Quantity not found")
        except Exception:
            try:
                product_quantity = product.find('span', class_='Label-sc-15v1nk5-0 CosmeticSelector___StyledLabel2-sc-81mggp-1 gJxZPQ hLFUWM').text.strip()
            except AttributeError:
                try:
                    product_quantity = product.find('span', class_='Label-sc-15v1nk5-0 gJxZPQ truncate').text.strip()
                except AttributeError:
                    product_quantity
            
        try:
            product_offered_price = product.find('span', class_='Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi').text.strip()
            if not product_offered_price:  # Checks if name is empty
                raise ValueError("Price not found")
        except Exception:
            product_offered_price = "No Product Price"

        try:
            product_original_price = product.find('span', class_='Label-sc-15v1nk5-0 Pricing___StyledLabel2-sc-pldi2d-2 gJxZPQ hsCgvu').text.strip()
            if not product_original_price:  # Checks if name is empty
                raise ValueError("Price not found")
        except Exception:
            product_original_price = "No Product Price"

        try:
            product_discount = product.find('span', class_='font-semibold lg:text-xs xl:text-sm leading-xxl xl:leading-md').text.strip()
        except Exception:
            product_discount = "No Discount"

        try:
            product_sale_price = product.find('span', class_='Label-sc-15v1nk5-0 gJxZPQ lg:text-sm xl:text-md font-semibold pr-5 py-0.5 ml-12').text.strip()
            if not product_sale_price:  # Checks if name is empty
                raise ValueError("Sale Price not found")
        except Exception:
            product_sale_price = "No Product Sale Price"
        
        _scrape_logger.info(f"Product Brand Name: {product_brand_name}")
        _scrape_logger.info(f"Product Name: {product_name}")
        _scrape_logger.info(f"Product Quantity: {product_quantity}")
        _scrape_logger.info(f"Product Offered Price: {product_offered_price}")
        _scrape_logger.info(f"Product Original Price: {product_original_price}")
        _scrape_logger.info(f"Product Sale Price: {product_sale_price}")
        _scrape_logger.info(f"Product Discount: {product_discount}")
        print("-------------")
        products_list.append({"Product Brand Name":product_brand_name, "Product Name": product_name, "Product Quantity":product_quantity, "Product Offered Price":product_offered_price, "Product Original Price":product_original_price,"Product Sale Price": product_sale_price, "Product Discount":product_discount})
        counter += 1
    
    # Products found, continue scraping
    return True, counter