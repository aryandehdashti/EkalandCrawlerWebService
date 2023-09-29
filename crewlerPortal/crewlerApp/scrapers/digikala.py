import requests

BASE_URL = 'https://www.digikala.com'
SEARCH_URL = 'https://api.digikala.com/v1/search/?q='
PRODUCT_URL = 'https://api.digikala.com/v1/product/'

def productParser(product):
    varients = []
    if product == None:
        return{
            "title": "ناموجود",
            "color": "ناموجود",
            "status": "ناموجود",
            "warranty": "ناموجود",
            "price": "ناموجود",
            "supplier": "ناموجود",
            "url": "ناموجود"
        }
    for item in product["variants"]:
        jsonProduct = {
            "title": product["title_fa"],
            "color": item["color"]["title"],
            "status": product["status"],
            "warranty": item["warranty"]["title_fa"],
            "price": item["price"]["selling_price"],
            "supplier": "digikala",
            "url": BASE_URL + product["url"]["uri"]
        }
        varients.append(jsonProduct)
    return varients


def findProduct(productName):
    try:
        searchResult = str(requests.get(SEARCH_URL + productName).json()["data"]["products"][0]["id"])
        product = requests.get(PRODUCT_URL + searchResult + "/").json()["data"]["product"]
        return productParser(product if product["title_fa"] in productName else None)

    except:
        return 'Not Found from Digikala'

