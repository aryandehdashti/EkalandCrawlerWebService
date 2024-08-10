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

# BASE_URL = 'https://toprayan.com'
# SEARCH_URL = 'https://toprayan.com/home/search/'

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

    # Configure logging to save to a file
    log_file = os.path.join(os.getcwd(), 'product_parser.log')  # Create log file in current directory
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)  # Get logger for current module
    logging.getLogger('mozila_driver').setLevel(logging.WARNING)

    try:
        if productUrl is not None:
            service = FirefoxService(executable_path=GeckoDriverManager().install()) 
            driver = webdriver.Firefox(service=service)  
            driver.get(productUrl)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "d-inline-block")))

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
            rawProduct = soup.find('section',{'class': 'mb-4'})
            if not rawProduct:
                raise ValueError("Product not found on page")
            
            if rawProduct is not None and len(rawProduct.findAll(string=re.compile("متاسفانه کالا در حال حاضر موجود نیست."))) == 0:
                products = []
                for option in rawProduct.findAll('div',{'class':'price-item'}):
                    productName = rawProduct.find('h1',{'class':'title1'}).text
                    color = option.find('strong',{'class':'op-color b-left'}).text if len(option.findAll('strong',{'class':'op-color b-left'})) > 0 else 'نامعلوم'
                    status = 'موجود'
                    warranty = option.find('strong',{'class':'op-guarantee'}).text if len(option.findAll('strong',{'class':'op-guarantee'})) > 0 else 'نامعلوم'
                    # dataId  = re.search(r'data-id="(\d+)"',option).group(1)
                    price = option.find('input',{'name':'options'}).get('data-less') if option.find('input',{'name':'options'}).get('data-less') is not None else option.find('input',{'name':'options'}).get('data-cost')
                    # price = rawProduct.find('span',{'class':'f_less'}).text
                    supplier = 'Toprayan'
                    url = productUrl
                    products.append({
                        "identifier":identifier,
                        "title": productName,
                        "color": color,
                        "status": status,
                        "warranty":warranty,
                        "insurance":"ندارد",
                        "price":price,
                        "supplier":supplier,
                        "url": url})
                # logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")
                return products
            else:
                # logger.info(f"Product not in stock: {productName}")
                return[{
            "identifier":identifier,
            "title": rawProduct.find('h1',{'class':'title1'}).text,
            "color": "ناموجود",
            "status": "ناموجود",
            "warranty":"ناموجود",
            "insurance":"ندارد",
            "price":"ناموجود",
            "supplier":'Toprayan',
            "url": productUrl
            }]
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        logger.error(f"Error fetching product: {productUrl} ({e})")
        return []
    except ValueError as e:
        logger.error(f"Error parsing product: {productUrl} ({e})")
        return []



# def findProduct(productName):
#     try:
#         res = requests.get(SEARCH_URL + productName)
#         soup = BeautifulSoup(res.content,'html.parser')
#         rawSearchResult = soup.findAll('a')[1].get('href') if len(soup.findAll('a')) > 0 and soup.find_all('a')[1].text in productName else None
#         return productParser(BASE_URL+rawSearchResult if rawSearchResult is not None else None)
#     except:pass
