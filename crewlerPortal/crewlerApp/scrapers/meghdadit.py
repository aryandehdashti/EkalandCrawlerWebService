import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://meghdadit.com'
SEARCH_URL = 'https://meghdadit.com/productlist/?s='

def productParser(productUrl):
    try:
        respond = requests.get(productUrl)
        soup = BeautifulSoup(respond.content, 'html.parser')
        rawProduct = soup.find('div',{'class':'rtl summary-left-pane'})
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
                "title": productName,
                "color": color,
                "status": status,
                "warranty":warranty,
                "insurance":"ندارد",
                "price":price,
                "supplier":supplier,
                "url": url})
        return products
    except: pass
    if productUrl == None :
        productName = 'ناموحود'
        color = 'ناموحود'
        status = 'ناموحود'
        warranty = 'ناموحود'
        price = 'ناموحود'
        supplier = 'meghdadit'
        url = productUrl
        return[{
        "title": productName,
        "color": color,
        "status": status,
        "warranty":warranty,
        "insurance":"ندارد",
        "price":price,
        "supplier":supplier,
        "url": url}]

def findProduct(productName):
    try:
        res = requests.get(SEARCH_URL + productName)
        soup = BeautifulSoup(res.content, 'html.parser')
        rawSearchResult = soup.find('ul',{'id':'SharedMessage_ContentPlaceHolder1_divThumbnailView'}).find('li')
        return productParser(BASE_URL+rawSearchResult.find('a').get('href') if rawSearchResult is not None and rawSearchResult.find('a').text in productName else None)
    except: pass