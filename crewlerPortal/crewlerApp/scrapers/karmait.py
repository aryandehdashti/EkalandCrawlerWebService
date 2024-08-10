import requests
from bs4 import BeautifulSoup
import re
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService


def productParser(productUrl,identifier):
    """
    Parses product information from a given URL.

    Args:
        productUrl (str): The URL of the product page.
        identifier (str): An identifier for the product.

    Returns:
        list: A list of dictionaries containing product information,
              or an empty list if parsing fails.

    Logs:
        - INFO: Successful product parsing with details.
        - ERROR: Any exceptions encountered during parsing.
        - DEBUG: Detailed information about the parsing process (optional).

    Saves logs to a file named 'product_parser.log' in the current working directory.
    """

    # # Configure logging to save to a file
    log_file = os.path.join(os.getcwd(), 'product_parser.log')  # Create log file in current directory
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)  # Get logger for current module
    logging.getLogger('mozila_driver').setLevel(logging.WARNING)

    try:
        if productUrl is not None:
            service = FirefoxService(executable_path=GeckoDriverManager().install()) 
            driver = webdriver.Firefox(service=service)  
            driver.get(productUrl)
            WebDriverWait(driver, 3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
            rawProduct = soup.find('div',{'class':'summary entry-summary'})
            if not rawProduct:
                raise ValueError("Product not found on page")

            if len(rawProduct.findAll(string=re.compile("ناموجود"))) == 0:
                productName = rawProduct.find('h1',{'class':'product_title'}).text
                color = 'نامعلوم'
                status = 'موجود'
                warranty = rawProduct.find('span',{'class':' thwvsf-item-span item-span-text '}).text
                price = rawProduct.find('span',{'class':'woocommerce-Price-amount amount price_sale'}).text
                
                supplier = 'Karmait'
                url = productUrl
                # logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")

            else:
                productName = rawProduct.find('h1',{'class':'product_title'}).text
                color = 'نامعلوم'
                status = 'ناموجود'
                warranty = 'ناموجود'
                price = 'ناموجود'
                supplier = 'Teccaf'
                url = productUrl
                # logger.info(f"Product not in stock: {productName}")
            return[{
                 "identifier":identifier,
                "title": productName,
                "color": color,
                "status": status,
                "warranty":warranty,
                "insurance":"ندارد",
                "price":price,
                "supplier":supplier,
                "url": url
            }]
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        logger.error(f"Error fetching product: {productUrl} ({e})")
        return []
    except ValueError as e:
        logger.error(f"Error parsing product: {productUrl} ({e})")
        return []


