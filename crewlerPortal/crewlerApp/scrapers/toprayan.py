import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://toprayan.com'
SEARCH_URL = 'https://toprayan.com/home/search/'

def productParser(productUrl):
    try:
        if productUrl is not None:
            respond = requests.get(productUrl)
            soup = BeautifulSoup(respond.content, 'html.parser')
            rawProduct = soup.find('div',{'class': 'col-12 col-md-8'})
            if rawProduct is not None and len(rawProduct.findAll(string=re.compile("متاسفانه کالا در حال حاضر موجود نیست."))) == 0:
                products = []
                for option in rawProduct.findAll('label',{'class':'alert alert-light'}):
                    productName = rawProduct.find('h1',{'class':'title1'}).text
                    color = option.find('strong',{'class':'op-color b-left'}).text if len(option.findAll('strong',{'class':'op-color b-left'})) > 0 else 'نامعلوم'
                    status = 'موجود'
                    warranty = option.find('span',{'class':'op-name one-line b-left '}).text if len(option.findAll('span',{'class':'op-name one-line b-left '})) > 0 else 'نامعلوم' +' '+ option.find('strong',{'class':'op-guarantee '}).text if len(option.findAll('strong',{'class':'op-guarantee '})) > 0 else 'نامعلوم'
                    dataId  = re.search(r'\d+',option.get('for')).group()
                    price = rawProduct.find('input',{'data-id':dataId}).get('data-cost')
                    supplier = 'Toprayan'
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
            else:
                return[{
            "title": rawProduct.find('h1',{'class':'title1'}).text,
            "color": "ناموحود",
            "status": "ناموحود",
            "warranty":"ناموحود",
            "insurance":"ندارد",
            "price":"ناموحود",
            "supplier":'Toprayan',
            "url": productUrl
            }]
    except:pass



def findProduct(productName):
    try:
        res = requests.get(SEARCH_URL + productName)
        soup = BeautifulSoup(res.content,'html.parser')
        rawSearchResult = soup.findAll('a')[1].get('href') if len(soup.findAll('a')) > 0 and soup.find_all('a')[1].text in productName else None
        return productParser(BASE_URL+rawSearchResult if rawSearchResult is not None else None)
    except:pass