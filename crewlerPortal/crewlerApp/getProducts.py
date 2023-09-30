from .models import Product
from .scrapers.scrapers import fetchProducts


def fetch():
    rawData = fetchProducts()
    for rawData_ in rawData:
        if isinstance(rawData_,str) or rawData_ is None:pass
        else:
            for item_ in rawData_:
                product_ = Product(
                    title = item_["title"],
                    color = item_["color"],
                    status = item_["status"],
                    warranty = item_["warranty"],
                    price = item_["price"],
                    insurance = item_["insurance"],
                    supplier = item_["supplier"],
                    url = item_["url"]
                )
                product_.save()

