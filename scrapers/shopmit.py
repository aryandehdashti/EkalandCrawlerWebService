from bs4 import BeautifulSoup
import urllib3

SEARCH_URL = 'https://shopmit.net/search/'

def productParser(productUrl):
    http = urllib3.PoolManager()
    response = http.request('GET', productUrl)
    soup = BeautifulSoup(response.data, 'html.parser')
    rawProduct = soup.find('div',{'class':'sb_page_section'})
    if rawProduct.find('div',{'class':'sb_product_inventory'}).find('strong').text == 'موجود!':
        products = []
        for warranty_ in rawProduct.findAll('label',{'class':'sb_form_radiobox d-flex justify-content-between'}):
            productName = rawProduct.find('h1',{'class':'sb_product_title mt-4 mt-lg-0'})
            status = rawProduct.find('div',{'class':'sb_product_inventory'}).find('strong').text
            warranty = warranty_.find('span',{'class':'sb_form_radiobox_title sb_font_m'})
            price = warranty_.find('strong').text
            supplier = 'Shopmit'
            url = productUrl
            products.append({
                "title": productName,
                "status": status,
                "warranty":warranty,
                "price":price,
                "supplier":supplier,
                "url": url})
        return products
    elif rawProduct.find('div',{'class':'sb_product_inventory'}).find('strong').text == 'ناموجود':
        return{
        "title": 'ناموحود',
        "status": 'ناموحود',
        "warranty":'ناموحود',
        "price":'ناموحود',
        "supplier":'Shopmit',
        "url": productUrl}

def findProduct(productName):
  http = urllib3.PoolManager()
  response = http.request('GET', SEARCH_URL + productName)
  soup = BeautifulSoup(response.data, 'html.parser')
  rawSearchResult = soup.find('div', {'class': 'sb_item_info'})
  if productName in rawSearchResult.find('a', {'class': 'sb_item_title'}).text:
    return productParser(rawSearchResult.find('a',{'class':'sb_item_title'}).get('href'))
  else:
    return None



