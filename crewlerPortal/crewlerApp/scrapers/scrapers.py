import pandas as pd
from . import baninopc, berozkala, digikala, exo, lioncomputer, meghdadit, shopmit,toprayan
from crewlerApp.models import SourceProduct
import os


def sourceFiles(path='sources'):
    thisFilePath = os.path.dirname(os.path.abspath(__file__))
    csvFolderPath = os.path.join(thisFilePath,path)
    paths =[]
    for file in os.listdir(csvFolderPath):
        if file.endswith("xlsx"):
            filePath = os.path.join(csvFolderPath, file)

            paths.append(filePath)
    return paths

def createProductSource(title,ID,URL,provider):
    if 'http' in URL :
        sourceProduct = SourceProduct(
        title = title,
        identifier = ID,
        URL = URL,
        provider = provider,
        is_active = True
        )
        sourceProduct.save()

def fetchProductSources():
    sourcesPath = sourceFiles()
    for file in sourcesPath:
        df = pd.DataFrame(pd.read_excel(file))
        for i in range(len(df)):
            productTitle = df.iloc[i-1]['productTitle']
            productID = df.iloc[i-1]['productID']
            baninopcURL = df.iloc[i-1]['baninopcURL']
            berozkalaURL = df.iloc[i-1]['berozkalaURL']
            digikalaURL = df.iloc[i-1]['digikalaURL']
            exoURL = df.iloc[i-1]['exoURL']
            lioncomputerURL = df.iloc[i-1]['lioncomputerURL']
            meghdaditURL = df.iloc[i-1]['meghdaditURL']
            shopmitURL = df.iloc[i-1]['shopmitURL']
            toprayanURL = df.iloc[i-1]['toprayanURL']
            createProductSource(productTitle,productID,baninopcURL,'baninopc')
            createProductSource(productTitle,productID,berozkalaURL,'berozkala')
            createProductSource(productTitle,productID,digikalaURL,'digikala')
            createProductSource(productTitle,productID,exoURL,'exo')
            createProductSource(productTitle,productID,lioncomputerURL,'lioncomputer')
            createProductSource(productTitle,productID,meghdaditURL,'meghdadit')
            createProductSource(productTitle,productID,shopmitURL,'shopmit')
            createProductSource(productTitle,productID,toprayanURL,'toprayan')
        os.remove(file)

def fetchProducts():
        allSourceProducts = SourceProduct.objects.all()
        result = []
        for SP in allSourceProducts:
            if SP.is_active:
                if SP.provider == 'baninopc':
                    result.append(baninopc.productParser(SP.URL,SP.identifier))
                elif SP.provider == 'berozkala':
                    result.append(berozkala.productParser(SP.URL,SP.identifier))
                elif SP.provider == 'digikala':
                    result.append(digikala.productParser(SP.URL,SP.identifier))
                elif SP.provider == 'exo':
                    result.append(exo.productParser(SP.URL,SP.identifier))
                elif SP.provider == 'lioncomputer':
                    result.append(lioncomputer.productParser(SP.URL,SP.identifier))
                elif SP.provider == 'meghdadit':
                    result.append(meghdadit.productParser(SP.URL,SP.identifier))
                elif SP.provider == 'shopmit':
                    result.append(shopmit.productParser(SP.URL,SP.identifier))
                elif SP.provider == 'toprayan':
                    result.append(toprayan.productParser(SP.URL,SP.identifier))

        return result




# def fetchProducts():
#     sourcesPath = sourceFiles()
#     for file in sourcesPath:
#         df = pd.read_csv(file)
#     result = []
#     for product_ in products:
#         result.append(baninopc.productParser(product_))
#         result.append(berozkala.productParser(product_))
#         result.append(digikala.productParser(product_))
#         result.append(exo.productParser(product_))
#         result.append(lioncomputer.productParser(product_))
#         result.append(meghdadit.productParser(product_))
#         result.append(shopmit.productParser(product_))
#         result.append(toprayan.productParser(product_))
#     return result

