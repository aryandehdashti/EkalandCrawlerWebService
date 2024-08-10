import requests
from bs4 import BeautifulSoup
import logging
import os

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
    log_file_path = os.path.join(os.getcwd(), 'product_parser.log')  
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)  

    try:
        respond = requests.get(productURL)
        respond.raise_for_status()

        soup = BeautifulSoup(respond.content, 'html.parser')
        rawProducts = soup.find('div',{'class':'shoplist'})
        if not rawProducts:
            raise ValueError("Product not found on page")
        
        rawProducts = rawProducts.find_all('div',{'class':'shop-row'})
        products = []
        for item in rawProducts:
            if item != '\n':
                if item.get('data-mojod') == '1':

                    title = item.find('h3',{'class':'nameH3'}).text
                    color = 'نامشخص'
                    status = 'موجود'
                    warranty = 'ناموجود' if len(item.findAll('span',{'class':'guarantee'})) == 0 else item.find('span',{'class':'guarantee'}).find('span').text
                    price = item.get('data-price')
                    supplier = f"emalls - {item.find('a',{'class':'shoplogotitle'}).text}"
                    url = item.find('a',{'class':'btn shop-button'}).get('href')

                    products.append({
                    "identifier":identifier,
                    "title": title,
                    "color": color,
                    "status": status,
                    "warranty":warranty,
                    "insurance":"ندارد",
                    "price":price,
                    "supplier":supplier,
                    "url": url
                })
        return products
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching product: {productURL} ({e})")
        return []
    except ValueError as e:
        logger.error(f"Error parsing product: {productURL} ({e})")
        return []



