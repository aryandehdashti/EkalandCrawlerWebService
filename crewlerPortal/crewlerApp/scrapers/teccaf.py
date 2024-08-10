import requests
from bs4 import BeautifulSoup
import re
import logging
import os

def productParser(productUrl, identifier):
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

    try:
        if productUrl is not None:
            respond = requests.get(productUrl)
            respond.raise_for_status()

            soup = BeautifulSoup(respond.content, 'html.parser')
            rawProduct = soup.find('div',{'class':'summary-inner set-mb-l reset-last-child'})
            if not rawProduct:
                raise ValueError("Product not found on page")

            if len(rawProduct.findAll(string=re.compile("استعلام قیمت"))) == 0:
                productName = rawProduct.find('h1',{'class':'product_title entry-title wd-entities-title'}).text
                color = 'نامعلوم'
                status = 'موجود'
                warranty = rawProduct.find('li',{'style':'text-align: justify;'}).text
                
                rawPrice = rawProduct.find('p',{'class':'price'}).text
                numbers_only = []  
                for char in rawPrice:  
                    if char.isdigit() or char == ',':  
                        numbers_only.append(char)  
                price = ''.join(numbers_only).replace(',', '')  
                
                supplier = 'Teccaf'
                url = productUrl
                # logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")

            else:
                productName = rawProduct.find('h1',{'class':'product_title entry-title wd-entities-title'}).text
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
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching product: {productUrl} ({e})")
        return []
    except ValueError as e:
        logger.error(f"Error parsing product: {productUrl} ({e})")
        return []

