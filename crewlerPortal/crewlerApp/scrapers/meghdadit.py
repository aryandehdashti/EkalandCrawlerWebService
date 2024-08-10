import requests
from bs4 import BeautifulSoup
import json
import logging
import os

# BASE_URL = 'https://meghdadit.com'
# SEARCH_URL = 'https://meghdadit.com/productlist/?s='

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
        rawProduct = soup.find('div',{'class':'rtl summary-left-pane'})
        if not rawProduct:
            raise ValueError("Product not found on page")
        
        products = []
        for product in json.loads(rawProduct.find('input',{'id':'hfdPrices'}).get('value')):
            productName = rawProduct.find('span', {"id":"SharedMessage_ContentPlaceHolder1_lblItemTitle"}).text
            color = product["ProductColorTitle"] if product["ProductColorTitle"] != None else 'نامعلوم'
            status = "موجود"
            warranty = product["WarrantyTitle"] if product["WarrantyTitle"] is not None else 'نامعلوم'
            price = product["FormattedPrice"]
            supplier = 'meghdadit'
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
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching product: {productUrl} ({e})")
        return []
    except ValueError as e:
        logger.error(f"Error parsing product: {productUrl} ({e})")
        return []
    if productUrl == None :
        productName = 'ناموحود'
        color = 'ناموحود'
        status = 'ناموحود'
        warranty = 'ناموحود'
        price = 'ناموحود'
        supplier = 'meghdadit'
        url = productUrl
        logger.info(f"Product not in stock: {productName}")
        return[{
        "identifier": identifier,
        "title": productName,
        "color": color,
        "status": status,
        "warranty":warranty,
        "insurance":"ندارد",
        "price":price,
        "supplier":supplier,
        "url": url}]

# def findProduct(productName):
#     try:
#         res = requests.get(SEARCH_URL + productName)
#         soup = BeautifulSoup(res.content, 'html.parser')
#         rawSearchResult = soup.find('ul',{'id':'SharedMessage_ContentPlaceHolder1_divThumbnailView'}).find('li')
#         return productParser(BASE_URL+rawSearchResult.find('a').get('href') if rawSearchResult is not None and rawSearchResult.find('a').text in productName else None)
#     except: pass