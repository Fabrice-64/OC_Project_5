"""
The module API_OpenFoodFacts aims at downloading products from Open Food Facts database.

In order to download a list of products large enough to provide the consumer with a large enough dataset, several parameters are set by default. A list of preselected categories has been made available in the module named config.py
This module follows the following steps:
1. the category to be downloaded has been previously selected
2. the API is initiated and gets the data from OFF website. By default, they are downloaded in JSON format
3. the downloaded data are converted in JSON readable by Python
4. the data are converted into a CSV format, ready to be exported to the database.

The fields selected from the products database are the following ones:
brands,
product_name,
code,
stores,
nutrition_score_fr,

Then the url for this product is rebuilt and recorded in the exchange file.
"""
import requests
import json
import config


def download_category_products_OFF():
    OFF_page = 1
    payload = {'search_terms': config.categories[0],'json': 1, 'action' : "process", \
    'fields' : "brands,product_name,code,stores,nutrition_grade_fr","page_size": 1000, "page": OFF_page}
    headers = {'User-Agent': 'python-requests/2.22.0'}
    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1', headers = headers, params = payload)

    print(r)
    print(r.url)
    print(r.headers)
    data = r.json()


    print(type(data))
    print(type(data['products']))
    print(data)
    print(data['products'])
    id = 0
    with open('response_API.txt', 'w') as output_file:
        for product in data['products']:
            id+= 1
            brand = product.get('brands', 'NaN')
            name = product.get('product_name', 'NaN')
            code = product.get('code', 'NaN')
            nutrition_grade = product.get('nutrition_grade_fr', 'NaN')
            stores = product.get('stores', 'NaN')
            row = f"\"{brand}\";\"{name}\";\"{code}\";\"{nutrition_grade}\";\"{stores}\";\"https://world.openfoodfacts.org/product/{code}\";\n"
            print(row)
            output_file.write(row)
    print("Nombre d'items importés: {}".format(id))

if __name__ == "__main__":
    download_category_products_OFF()