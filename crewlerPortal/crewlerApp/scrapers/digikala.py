import requests
import re
import logging
import os

PRODUCT_URL = 'https://api.digikala.com/v2/product/'

def productParser(productURL,identifier):
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
        productID = re.search(r'dkp-(\d+)', productURL).group(1)
        respone = requests.get(PRODUCT_URL + str(productID) + '/')
        respone.raise_for_status()
        product = respone.json()["data"]["product"]
        # logger.info(f"{respone.status_code} code recieved for this URL:{productURL}")

        varients = []
        if product == None:
            return[{
                "identifier":identifier,
                "title": "ناموجود",
                "color": "ناموجود",
                "status": "ناموجود",
                "warranty": "ناموجود",
                "insurance":"ندارد",
                "price": "ناموجود",
                "supplier": "ناموجود",
                "url": "ناموجود"
            }]
        
        for item in product["variants"]:
            if "color" in product:
                jsonProduct = {
                    "identifier": identifier,
                    "title": product["title_fa"],
                    "color": item["color"]["title"],
                    "status": product["status"],
                    "warranty": item["warranty"]["title_fa"],
                    "insurance":"ندارد",
                    "price": item["price"]["selling_price"],
                    "supplier": "digikala",
                    "url": productURL
                }
            else:
                jsonProduct = {
                    "identifier": identifier,
                    "title": product["title_fa"],
                    "color": 'ندارد',
                    "status": product["status"],
                    "warranty": item["warranty"]["title_fa"],
                    "insurance":"ندارد",
                    "price": item["price"]["selling_price"],
                    "supplier": "digikala",
                    "url": productURL
                }
                varients.append(jsonProduct)
        # logger.info(f"Successfully parsed product: {identifier} - digikala (multiple colors and warranties)")
        return varients   
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching product: {productURL} ({e})")
        return []
    except ValueError as e:
        logger.error(f"Error parsing product: {productURL} ({e})")
        return []
  

# def findProduct(productName):
#     try:
#         searchResult = str(requests.get(SEARCH_URL + productName).json()["data"]["products"][0]["id"])
#         product = requests.get(PRODUCT_URL + searchResult + "/").json()["data"]["product"]
#         return productParser(product if product["title_fa"] in productName else None)

#     except:
#         pass


