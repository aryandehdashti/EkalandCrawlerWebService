from .models import Product
from .scrapers.scrapers import fetchProducts, fetchProductSources


def fetch():
    fetchProductSources()
    rawData = fetchProducts()
    for rawData_ in rawData:
        if isinstance(rawData_,str) or rawData_ is None:pass
        else:
            for item_ in rawData_:
                product_ = Product(
                    identifier = item_["identifier"],
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

