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
    except: pass
    if productUrl == None :
        productName = 'ناموحود'
        color = 'ناموحود'
        status = 'ناموحود'
        warranty = 'ناموحود'
        price = 'ناموحود'
        supplier = 'meghdadit'
        url = productUrl
        return{
        "title": productName,
        "color": color,
        "status": status,
        "warranty":warranty,
        "price":price,
        "supplier":supplier,
        "url": url}

    else:
        products = []
        for product in json.loads(rawProduct.find('input',{'id':'hfdPrices'}).get('value')):
            productName = rawProduct.find('span', {"id":"SharedMessage_ContentPlaceHolder1_lblItemTitle"}).text
            color = product["ProductColorTitle"]
            status = "موجود"
            warranty = product["WarrantyTitle"]
            price = product["FormattedPrice"]
            supplier = 'meghdadit'
            url = productUrl
            products.append({
                "title": productName,
                "color": color,
                "status": status,
                "warranty":warranty,
                "price":price,
                "supplier":supplier,
                "url": url})
    return products

def findProduct(productName):
    res = requests.get(SEARCH_URL + productName)
    soup = BeautifulSoup(res.content, 'html.parser')
    rawSearchResult = soup.find('ul',{'id':'SharedMessage_ContentPlaceHolder1_divThumbnailView'}).find('li')
    return productParser(BASE_URL+rawSearchResult.find('a').get('href') if productName in rawSearchResult.find('a').text else None)


productParser('https://meghdadit.com/product/19/kingston-kvr-ddr2-2gb-800mhz-cl6-dimm-16-chip-desktop-ram/')