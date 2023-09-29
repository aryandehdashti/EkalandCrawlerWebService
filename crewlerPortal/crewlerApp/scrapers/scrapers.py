import pandas as pd
import baninopc, berozkala, digikala, exo, lioncomputer, meghdadit, shopmit,toprayan

def fetchProducts():
    df = pd.read_csv('./source.csv')
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

    