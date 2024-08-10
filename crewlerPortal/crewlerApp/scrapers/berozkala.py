import requests
from bs4 import BeautifulSoup
import re
import logging
import os

SEARCH_URL = 'https://berozkala.com/api/search?kw='
PRODUCT_URL = 'https://berozkala.com/fa/product/'
GET_PRICE_URL = 'https://berozkala.com/api/Options/GetPrice/'

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

    
    log_file = os.path.join(os.getcwd(), 'product_parser.log')  
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)  

    try:
        respond = requests.get(productUrl)
        respond.raise_for_status()

        soup = BeautifulSoup(respond.content,'html.parser')
        rawProduct = soup.find('div',{'class':'summary entry-summary col-lg-24 col-md-24 col-sm-21 col-xs-36'})
        if not rawProduct:
            raise ValueError("Product not found on page")

        productName = rawProduct.find('h1',{'class':'product_title entry-title'}).text.strip()
        if len(rawProduct.find_all(string=re.compile("موجود در انبار"))) > 0:
            mainPrice = soup.find('span',{'id':'_mainPrice'}).text
            rawWarranty = rawProduct.find('select',{'id':'ddl1'}).find_all('option') if rawProduct.find('select', {'id': 'ddl1'}) is not None else ['']
            rawColors = rawProduct.find('select',{'id':'ddl2'}).find_all('option') if rawProduct.find('select', {'id': 'ddl2'}) is not None else ['']
            for warranty_ in rawWarranty:
                for color_ in rawColors:
                    # return print(type(color_))
                    color = color_.text if color_ != "" else "نامعلوم"
                    status = 'موجود در انبار'
                    warranty = warranty_.text  if warranty_ != "" else "ندارد"
                    if color_ != '':
                        price = int(mainPrice) + int(requests.get(GET_PRICE_URL + color_.get('value')).json()[0]['price']) + int(requests.get(GET_PRICE_URL + warranty_.get('value')).json()[0]['price'])
                    else :
                        price = int(mainPrice) + int(requests.get(GET_PRICE_URL + warranty_.get('value')).json()[0]['price'])
                    insurance = rawProduct.find('label',{'for':'html'}).text.strip() if len(rawProduct.find_all('label',{'for':'html'})) > 0 else "ناموجود"
                    supplier = 'berozkala'
                    url = productUrl
        else:
            color = 'ناموحود'
            status = 'ناموحود'
            warranty = 'ناموحود'
            price = 'ناموحود'
            insurance = 'ناموحود'
            supplier = 'berozkala'
            url = productUrl
        # logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")
        return [{
            "identifier": identifier,
            "title": productName,
            "color": color,
            "status": status,
            "warranty":warranty,
            "price":price,
            "insurance":insurance,
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
#         product = json.loads(res.content)[0] if len(json.loads(res.content)) > 0 else None
#         if product is not None:
#             value = product["value"]
#             slug = product["slug"]
#             return productParser(PRODUCT_URL+value+'/'+slug)

#     except:pass
