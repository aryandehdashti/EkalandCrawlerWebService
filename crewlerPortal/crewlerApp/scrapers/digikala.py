import requests
import re

PRODUCT_URL = 'https://api.digikala.com/v1/product/'

def productParser(productURL,identifier):
    productID = re.search(r'dkp-(\d+)', productURL).group(1)
    product = requests.get(PRODUCT_URL + str(productID) + '/').json()["data"]["product"]
    varients = []
    if product == None:
        return[{
            "identifier":identifier,
            "title": "ناموجود",
            "color": "ناموجود",
            "status": "ناموجود",
            "warranty": "ناموجود",
            "insurance":"ندارد",
            "price": "ناموجود",
            "supplier": "ناموجود",
            "url": "ناموجود"
        }]
    for item in product["variants"]:
        jsonProduct = {
            "identifier": identifier,
            "title": product["title_fa"],
            "color": item["color"]["title"],
            "status": product["status"],
            "warranty": item["warranty"]["title_fa"],
            "insurance":"ندارد",
            "price": item["price"]["selling_price"],
            "supplier": "digikala",
            "url": productURL
        }
        varients.append(jsonProduct)
    return varients


# def findProduct(productName):
#     try:
#         searchResult = str(requests.get(SEARCH_URL + productName).json()["data"]["products"][0]["id"])
#         product = requests.get(PRODUCT_URL + searchResult + "/").json()["data"]["product"]
#         return productParser(product if product["title_fa"] in productName else None)

#     except:
#         pass
