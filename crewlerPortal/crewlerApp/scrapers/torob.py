import requests
import logging
import os


SELLERS_URL = 'https://api.torob.com/v4/base-product/sellers/?source=next_desktop&discover_method=direct&_bt__experiment=&search_id=&cities=&province=&prk='

def  productParser(productURL, identifier):
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
        respone =  requests.get(SELLERS_URL + productURL.split("/")[4])
        respone.raise_for_status()
        rawProducts = respone.json()['results']
        products = []
        for item in rawProducts:
            if item["availability"]:
                jsonProduct = {
                        "identifier": identifier,
                        "title": item["name1"],
                        "color": "نامعلوم",
                        "status": "موجود",
                        "warranty": item["name2"],
                        "insurance":"نامعلوم",
                        "price": item["price"],
                        "supplier": f"Torob - {item['shop_name']}",
                        "url": item["page_url"]
                    }
                products.append(jsonProduct)
        return products   
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching product: {productURL} ({e})")
        return []
    except ValueError as e:
        logger.error(f"Error parsing product: {productURL} ({e})")
        return []


        