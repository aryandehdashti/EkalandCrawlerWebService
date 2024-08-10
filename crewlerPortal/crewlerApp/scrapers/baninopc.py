import requests
from bs4 import BeautifulSoup
import re
import logging
import os

# SEARCH_URL = 'https://baninopc.com/backend/api/search?keyword='
# PRODUCT_URL = 'https://baninopc.com/product/'

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
    log_file_path = os.path.join(os.getcwd(), 'product_parser.log')  
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)  

    try:
        respond = requests.get(productUrl)
        respond.raise_for_status()

        soup = BeautifulSoup(respond.content, 'html.parser')
        rawProduct = soup.find('div',{'class':'product-detail pt-3 col-span-1 md:col-span-3 lg:col-span-1 space-y-2.5'})
        if not rawProduct:
            raise ValueError("Product not found on page")
        
        productName = rawProduct.find("h1", {"class":"font-bold"}).text
        color = rawProduct.find("span", {"class":"p-1 border-l text-center text-gray-500 border-gray-300 last-of-type:border-none text-xs md:p-2 md:text-sm lg:text-base"}).text if len(rawProduct.findAll(string=re.compile('محصول مورد نظر در حال حاضر موجود نمی‌باشد'))) == 0 and len(rawProduct.findAll("span", {"class":"p-1 border-l text-center text-gray-500 border-gray-300 last-of-type:border-none text-xs md:p-2 md:text-sm lg:text-base"})) > 0 else 'ناموجود'
        # warranty = 'ناموجود' if len(rawProduct.findAll(string=re.compile('محصول مورد نظر در حال حاضر موجود نمی‌باشد'))) > 0 and len(rawProduct.findAll("span", {"class":"p-1 border-l text-center text-gray-500 border-gray-300 last-of-type:border-none text-xs md:p-2 md:text-sm lg:text-base"}))==0 else rawProduct.find("span", {"class":"p-1 border-l text-center text-gray-500 border-gray-300 last-of-type:border-none text-xs md:p-2 md:text-sm lg:text-base"}).text.replace("گارانتی شرکتی :", "")
        warranty = 'ناموجود' 
        price = 'ناموجود' if len(rawProduct.findAll(string=re.compile('محصول مورد نظر در حال حاضر موجود نمی‌باشد'))) > 0 else rawProduct.find("span", {"id":"product-price"}).text
        status = 'ناموجود' if len(rawProduct.findAll(string=re.compile('محصول مورد نظر در حال حاضر موجود نمی‌باشد'))) > 0 else 'موجود'
        supplier = 'Baninopc'
        url = productUrl
        # logger.info(f"Successfully parsed product: {productName} (multiple colors and warranties)")
        return [{
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
#         product = json.loads(res.content)["products"][0] if len(json.loads(res.content)['products']) > 0 else None
#         if product is not None:
#             uniqueId = product["uniqueId"]
#             slug = product["slug"]
#             return productParser(PRODUCT_URL+uniqueId+'/'+slug)

#     except: pass
    