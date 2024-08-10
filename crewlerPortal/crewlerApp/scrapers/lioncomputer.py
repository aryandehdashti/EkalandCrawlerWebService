import requests
from bs4 import BeautifulSoup
import re
import logging
import os

# SEARCH_URL = 'https://www.lioncomputer.com/shop/search?q='

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
        respond = requests.get(productUrl)
        respond.raise_for_status()

        soup = BeautifulSoup(respond.content, 'html.parser')
        rawProduct = soup.find('div',{'id':"product-body"})
        if not rawProduct:
            raise ValueError("Product not found on page")
        
        if productUrl == None or 'ناموحود' in rawProduct.find('strong').text:
            productName = 'ناموحود'
            color = 'ناموحود'
            status = 'ناموحود'
            warranty = 'ناموحود'
            price = 'ناموحود'
            supplier = 'lioncomputer'
            url = 'ناموجود'
            logger.info(f"Product not in stock: {productName}")

        else:
            productName = rawProduct.find('h1').text
            color = rawProduct.find_all(string=re.compile("رنگ"))[0] if len(rawProduct.find_all(string=re.compile("رنگ"))) > 0 else 'نامعلوم'
            status = 'موجود'
            warranty = rawProduct.find_all(string=re.compile("گارانتی"))[0].text.strip() if  len(rawProduct.find_all(string=re.compile("گارانتی"))) > 0 else 'موجود نیست'
            price = rawProduct.find('strong').text.strip().replace(' تومان','')
            supplier = 'lioncomputer'
            url = productUrl
            # logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")

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
#         res = requests.get(SEARCH_URL+productName)
#         soup = BeautifulSoup(res.content, 'html.parser')
#         rawSearchResult = soup.find('div',{'class': 'products-grid'}).find_all('div',{'class': 'product-outer'})[0]
#         return productParser(rawSearchResult.find('a').get('href') if rawSearchResult.find('h5').text in productName else None)
#     except:pass


