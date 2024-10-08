import requests
from bs4 import BeautifulSoup
import re
import logging
import os

SEARCH_URL = 'https://exo.ir/index.php?route=product/search&search='

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

    try:
        if productUrl is not None:
            respond = requests.get(productUrl)
            respond.raise_for_status()

            soup = BeautifulSoup(respond.content, 'html.parser')
            rawProduct = soup.find('div',{'class':'col-sm-7 d-flex flex-column'})
            if not rawProduct:
                raise ValueError("Product not found on page")

            if len(rawProduct.findAll(string=re.compile("ناموجود"))) == 0:
                productName = rawProduct.find('h1',{'class':'fs-2 font-latin-yekan fw-bold mb-2'}).text
                color = 'نامعلوم'
                status = 'موجود'
                warranty = rawProduct.find('div',{'id':'float-price'}).find('div',{'class':'small text-center'}).findAll('span')[1].text
                price = rawProduct.find('h2',{'class':'fw-bold','id':'price'}).text
                supplier = 'Exo'
                url = productUrl
                # logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")

            else:
                productName = rawProduct.find('h1',{'class':'fs-2 font-latin-yekan fw-bold mb-2'}).text
                color = 'نامعلوم'
                status = 'ناموجود'
                warranty = 'ناموجود'
                price = 'ناموجود'
                supplier = 'Exo'
                url = productUrl
                logger.info(f"Product not in stock: {productName}")
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


# def findProduct(productName):
#     try:
#         res = requests.get(SEARCH_URL + productName)
#         soup = BeautifulSoup(res.content, 'html.parser')
#         rawSearchResult = soup.find('div',{'class': 'grid-product'}).find('a').get('href') if len(soup.findAll('div',{'class': 'grid-product'})) > 0 else None
#         return productParser(rawSearchResult)
#     except:pass

