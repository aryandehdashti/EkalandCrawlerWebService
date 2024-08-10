import pandas as pd
from . import baninopc, berozkala, digikala, exo, lioncomputer, meghdadit, shopmit, toprayan, torob, emalls, karmait, teccaf
from crewlerApp.models import SourceProduct
import os
import logging


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
            emallsURL = df.iloc[i-1]['emallsURL']
            torobURL = df.iloc[i-1]['torobURL']
            karmaitURL = df.iloc[i-1]['karmaitURL']
            teccafURL = df.iloc[i-1]['teccafURL']
            createProductSource(productTitle,productID,baninopcURL,'baninopc')
            createProductSource(productTitle,productID,berozkalaURL,'berozkala')
            createProductSource(productTitle,productID,digikalaURL,'digikala')
            createProductSource(productTitle,productID,exoURL,'exo')
            createProductSource(productTitle,productID,lioncomputerURL,'lioncomputer')
            createProductSource(productTitle,productID,meghdaditURL,'meghdadit')
            createProductSource(productTitle,productID,shopmitURL,'shopmit')
            createProductSource(productTitle,productID,toprayanURL,'toprayan')
            createProductSource(productTitle,productID,emallsURL,'emalls')
            createProductSource(productTitle,productID,torobURL,'torob')
            createProductSource(productTitle,productID,karmaitURL,'karmait')
            createProductSource(productTitle,productID,teccafURL,'teccaf')
        os.remove(file)

def fetchProducts():
    """
    Parses product information from a given URL.

    Args:
        productUrl (str): The URL of the product page.
        identifier (str): An identifier for the product.

    Returns:
        list: A list of dictionaries containing product information,
              or an empty list if parsing fails.

    Logs:
        - INFO: Successful product parsing with details.
        - ERROR: Any exceptions encountered during parsing.
        - DEBUG: Detailed information about the parsing process (optional).

    Saves logs to a file named 'product_parser.log' in the current working directory.
    """

    log_file = os.path.join(os.getcwd(), 'product_parser.log')  
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)  

    allSourceProducts = SourceProduct.objects.all()
    result = []
    for SP in allSourceProducts:
        if SP.is_active:
            if SP.provider == 'baninopc':
                try: 
                    result.append(baninopc.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'berozkala':
                try: 
                    result.append(berozkala.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'digikala':
                try:
                    result.append(digikala.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'exo':
                try: 
                    result.append(exo.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'lioncomputer':
                try: 
                    result.append(lioncomputer.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'meghdadit':
                try: 
                    result.append(meghdadit.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")  
            # elif SP.provider == 'shopmit':
            #     try:
            #         result.append(shopmit.productParser(SP.URL,SP.identifier))
            #     except Exception as e:  # Catch all exceptions for cleaner logging
            #         logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            # elif SP.provider == 'toprayan':
            #     try:
            #         result.append(toprayan.productParser(SP.URL,SP.identifier))
            #     except Exception as e:  # Catch all exceptions for cleaner logging
            #         logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'emalls':
                try:
                    result.append(emalls.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'torob':
                try:
                    result.append(torob.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            elif SP.provider == 'teccaf':
                try:
                    result.append(teccaf.productParser(SP.URL,SP.identifier))
                except Exception as e:  # Catch all exceptions for cleaner logging
                    logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")
            # elif SP.provider == 'karmait':
            #     try:
            #         result.append(karmait.productParser(SP.URL,SP.identifier))
            #     except Exception as e:  # Catch all exceptions for cleaner logging
            #         logger.error(f"Error fetching products from {SP.provider} ({SP.URL}): {e}")

                
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

