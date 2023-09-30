import pandas as pd
from . import baninopc, berozkala, digikala, exo, lioncomputer, meghdadit, shopmit,toprayan
import os


def fetchProducts():
    thisFilePath = os.path.dirname(os.path.abspath(__file__))
    csvFilePath = os.path.join(thisFilePath,'source.csv')
    df = pd.read_csv(csvFilePath)
    products = df['نام']

    result = []
    for product_ in products:
        result.append(baninopc.findProduct(product_))
        result.append(berozkala.findProduct(product_))
        result.append(digikala.findProduct(product_))
        result.append(exo.findProduct(product_))
        result.append(lioncomputer.findProduct(product_))
        result.append(meghdadit.findProduct(product_))
        result.append(shopmit.findProduct(product_))
        result.append(toprayan.findProduct(product_))
    return result

