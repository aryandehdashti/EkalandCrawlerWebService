from bs4 import BeautifulSoup
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

# SEARCH_URL = 'https://shopmit.net/search/'



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
    log_file = os.path.join(os.getcwd(), 'product_parser.log')  
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)  
    logging.getLogger('mozila_driver').setLevel(logging.WARNING)

    if productUrl is not None:
      try:
        service = FirefoxService(executable_path=GeckoDriverManager().install()) 
        driver = webdriver.Firefox(service=service)  
        driver.get(productUrl)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "sb_product_title")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        rawProduct = soup.find('div',{'class':'sb_page_section'})
        if not rawProduct:
            raise ValueError("Product not found on page")
        
        if rawProduct.find('div',{'class':'sb_product_inventory'}).find('strong').text == 'موجود!\t\t\t\t\t\t\t\t\t\t\t':
            products = []
            for warranty_ in rawProduct.findAll('label',{'class':'sb_form_radiobox d-flex justify-content-between'}):
                productName = rawProduct.find('h1',{'class':'sb_product_title mt-4 mt-lg-0'})
                status = rawProduct.find('div',{'class':'sb_product_inventory'}).find('strong').text
                warranty = warranty_.find('span',{'class':'sb_form_radiobox_title sb_font_m'})
                price = warranty_.find('strong').text
                supplier = 'Shopmit'
                url = productUrl
                products.append({
                    "identifier":identifier,
                    "title": productName,
                    "status": status,
                    "warranty":warranty,
                    "insurance":"ندارد",
                    "price":price,
                    "supplier":supplier,
                    "url": url})
                logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")
            return products

        elif rawProduct.find('div',{'class':'sb_product_inventory'}).find('strong').text == 'ناموجود\t\t\t\t\t\t\t\t\t\t\t':
            # logger.info(f"Product not in stock: {productName}")
            return[{
              "identifier":identifier,
            "title": 'ناموحود',
            "status": 'ناموحود',
            "warranty":'ناموحود',
            "price":'ناموحود',
            "supplier":'Shopmit',
            "url": productUrl}]
      except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        logger.error(f"Error fetching product: {productUrl} ({e})")
        return []
      except ValueError as e:
        logger.error(f"Error parsing product: {productUrl} ({e})")
        return []


# def findProduct(productName):
#     try:
#         http = urllib3.PoolManager()
#         response = http.request('GET', SEARCH_URL + productName)
#         soup = BeautifulSoup(response.data, 'html.parser')
#         rawSearchResult = soup.find('div', {'class': 'sb_item_info'}).find('a',{'class':'sb_item_title'}).get('href') if len(soup.findAll('div', {'class': 'sb_item_info'})) > 0 else None
#         return productParser(rawSearchResult if rawSearchResult is not None and rawSearchResult.find('a', {'class': 'sb_item_title'}).text in productName else None)
#     except:pass


