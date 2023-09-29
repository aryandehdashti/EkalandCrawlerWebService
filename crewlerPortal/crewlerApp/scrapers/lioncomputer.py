import requests
from bs4 import BeautifulSoup
import re

SEARCH_URL = 'https://www.lioncomputer.com/shop/search?q='

def productParser(productUrl):
    try:
        respond = requests.get(productUrl)
        soup = BeautifulSoup(respond.content, 'html.parser')
        rawProduct = soup.find('div',{'id':"product-body"})
    except: pass
    if productUrl == None or 'ناموحود' in rawProduct.find('strong').text:
        productName = 'ناموحود'
        color = 'ناموحود'
        status = 'ناموحود'
        warranty = 'ناموحود'
        price = 'ناموحود'
        supplier = 'lioncomputer'
        url = productUrl
    else:
        productName = rawProduct.find('h1').text
        color = rawProduct.find_all(string=re.compile("رنگ"))[0] if len(rawProduct.find_all(string=re.compile("رنگ"))) > 0 else 'نامعلوم'
        status = 'موجود'
        warranty = rawProduct.find_all(string=re.compile("گارانتی"))[0].text.strip() if  len(rawProduct.find_all(string=re.compile("گارانتی"))) > 0 else 'موجود نیست'
        price = rawProduct.find('strong').text.strip().replace(' تومان','')
        supplier = 'lioncomputer'
        url = productUrl
    
    return{
        "title": productName,
        "color": color,
        "status": status,
        "warranty":warranty,
        "price":price,
        "supplier":supplier,
        "url": url
    }


def findProduct(productName):
    try:
        res = requests.get(SEARCH_URL+productName)
        soup = BeautifulSoup(res.content, 'html.parser')
        rawSearchResult = soup.find('div',{'class': 'products-grid'}).find_all('div',{'class': 'product-outer'})[0]
        return productParser(rawSearchResult.find('a').get('href') if rawSearchResult.find('h5').text in productName else None)
    except:pass


