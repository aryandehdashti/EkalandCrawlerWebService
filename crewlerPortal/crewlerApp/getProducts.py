from models import Product
from scrapers.scrapers import fetchProducts
from apscheduler. schedulers.background import BackgroundScheduler


def fetch():
    rawData = fetchProducts()
    products = []
    for rawData_ in rawData:
        product_ = Product(
            title = rawData_["title"],
            color = rawData_["color"],
            status = rawData_["status"],
            warranty = rawData_["warranty"],
            price = rawData_["price"],
            insurance = rawData_["insurance"],
            supplier = rawData_["supplier"],
            url = rawData_["url"]
        )
        product_.save()
        products.append(product_)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch,'interval', hours=12)
    scheduler.start()
