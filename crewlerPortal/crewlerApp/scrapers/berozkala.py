import requests
from bs4 import BeautifulSoup
import json 
import re

SEARCH_URL = 'https://berozkala.com/api/search?kw='
PRODUCT_URL = 'https://berozkala.com/fa/product/'
GET_PRICE_URL = 'https://berozkala.com/api/Options/GetPrice/'

def productParser(productUrl):
    respond = requests.get(productUrl)
    soup = BeautifulSoup(respond.content,'html.parser')
    rawProduct = soup.find('div',{'class':'summary entry-summary col-lg-24 col-md-24 col-sm-21 col-xs-36'})
    productName = rawProduct.find('h1',{'class':'product_title entry-title'}).text.strip()
    if len(rawProduct.find_all(string=re.compile("موجود در انبار"))) > 0:
        mainPrice = soup.find('span',{'id':'_mainPrice'}).text
        rawWarranty = rawProduct.find('select',{'id':'ddl1'}).find_all('option') if rawProduct.find('select', {'id': 'ddl1'}) is not None else ['']
        rawColors = rawProduct.find('select',{'id':'ddl2'}).find_all('option') if rawProduct.find('select', {'id': 'ddl2'}) is not None else ['']
        for warranty_ in rawWarranty:
            for color_ in rawColors:
                # return print(type(color_))
                color = color_.text if color_ is not "" else "نامعلوم"
                status = 'موجود در انبار'
                warranty = warranty_.text  if warranty_ is not "" else "ندارد"
                price = int(mainPrice) + int(requests.get(GET_PRICE_URL + color_.get('value')).json()[0]['price']) + int(requests.get(GET_PRICE_URL + warranty_.get('value')).json()[0]['price'])
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
    return {
        "title": productName,
        "color": color,
        "status": status,
        "warranty":warranty,
        "price":price,
        "insurance":insurance,
        "supplier":supplier,
        "url": url
    }
    

def findProduct(productName):
    try:
        res = requests.get(SEARCH_URL+productName)
        product = json.loads(res.content)[0] if len(json.loads(res.content)) > 0 else None
        if product is not None:
            value = product["value"]
            slug = product["slug"]
            return productParser(PRODUCT_URL+value+'/'+slug)

        else:
            return 'Not found in Berozkala'
    except:pass
