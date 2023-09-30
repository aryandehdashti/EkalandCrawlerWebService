import requests
from bs4 import BeautifulSoup
import re


SEARCH_URL = 'https://exo.ir/index.php?route=product/search&search='

def productParser(productUrl):
        if productUrl is not None:
            respond = requests.get(productUrl)
            soup = BeautifulSoup(respond.content, 'html.parser')
            rawProduct = soup.find('div',{'class':'col-sm-7 d-flex flex-column'})
            if len(rawProduct.findAll(string=re.compile("ناموجود"))) == 0:
                productName = rawProduct.find('h1',{'class':'fs-2 font-latin-yekan fw-bold mb-2'}).text
                color = 'نامعلوم'
                status = 'موجود'
                warranty = rawProduct.find('div',{'id':'float-price'}).find('div',{'class':'small text-center'}).findAll('span')[1].text
                price = rawProduct.find('h2',{'class':'fw-bold','id':'price'}).text
                supplier = 'Exo'
                url = productUrl
            else:
                productName = rawProduct.find('h1',{'class':'fs-2 font-latin-yekan fw-bold mb-2'}).text
                color = 'نامعلوم'
                status = 'ناموجود'
                warranty = 'ناموجود'
                price = 'ناموجود'
                supplier = 'Exo'
                url = productUrl
            return[{
                "title": productName,
                "color": color,
                "status": status,
                "warranty":warranty,
                "insurance":"ندارد",
                "price":price,
                "supplier":supplier,
                "url": url
            }]

def findProduct(productName):
    try:
        res = requests.get(SEARCH_URL + productName)
        soup = BeautifulSoup(res.content, 'html.parser')
        rawSearchResult = soup.find('div',{'class': 'grid-product'}).find('a').get('href') if len(soup.findAll('div',{'class': 'grid-product'})) > 0 else None
        return productParser(rawSearchResult)
    except:pass

