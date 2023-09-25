import requests
from bs4 import BeautifulSoup
import json 
import re

SEARCH_URL = 'https://baninopc.com/backend/api/search?keyword='
PRODUCT_URL = 'https://baninopc.com/product/'

def productParser(productUrl):
    respond = requests.get(productUrl)
    soup = BeautifulSoup(respond.content, 'html.parser')
    rawProduct = soup.find('div',{'class':'product-detail pt-3 col-span-1 md:col-span-3 lg:col-span-1 space-y-2.5'})
    productName = rawProduct.find("h2", {"class":"text-lg font-semibold"}).text
    color = rawProduct.find("span", {"class":"p-1 border-l text-center text-gray-500 border-gray-300 last-of-type:border-none text-xs md:p-2 md:text-sm lg:text-base"}).text
    warranty = rawProduct.find("span", {"class":"p-1 border-l text-center text-gray-500 border-gray-300 last-of-type:border-none text-xs md:p-2 md:text-sm lg:text-base"}).text.replace("گارانتی شرکتی :", "")
    price = rawProduct.find("span", {"id":"product-price"}).text
    status = 'ناموجود' if 'محصول مورد نظر در حال حاضر موجود نمی‌باشد' in rawProduct else 'موجود'
    supplier = 'Baninopc'
    url = productUrl
    return {
        "title": productName,
        "color": color,
        "status": status,
        "warranty":warranty,
        "price":price,
        "supplier":supplier,
        "url": url
    }

def findProduct(productName):
    res = requests.get(SEARCH_URL+productName)
    product = json.loads(res.content)["products"][0] if len(json.loads(res.content)) > 0 else None
    if product is not None:
        uniqueId = product["uniqueId"]
        slug = product["slug"]
        return productParser(PRODUCT_URL+uniqueId+'/'+slug)

    else:
        return 'Not found in Baninopc'
    
findProduct('گوشی موبایل سامسونگ مدل GALAXY A34 ظرفیت 128 گیگابایت و رم 8 گیگابایت')
