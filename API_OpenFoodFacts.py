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
ingredients_txt,

The category is selected out of the config.py module and the url is built based on the url of the website.

Then the url for this product is rebuilt and recorded in the exchange file.
"""
import requests
import json
import config

def check_data_special_characters(value):
    if value is None:
        #print("Observation : ", value, "est vide")
        result = "NaN"
    elif '"' in value:
        #print ("Risque à la ligne : ", value)
        new_value = value
        result = new_value.replace('"', '')
    else:
        result = value
    return result

def download_category_products_OFF():
    r = requests.get(config.url, headers = config.headers, params = config.payload)

    #print(r)
    #print(r.url)
    #print(r.headers)
    data = r.json()

    #print(type(data))
    #print(type(data['products']))
    #print(data)
    #print(data['products'])
    id = 0
    with open('response_API.txt', 'w') as output_file:
        for product in data['products']:
            id+= 1
            brand = check_data_special_characters(product.get('brands'))
            name = check_data_special_characters(product.get('product_name'))
            categorie = config.category_choice +1
            code = product.get('code', 'NaN')
            nutrition_grade = product.get('nutrition_grade_fr', 'NaN')
            stores = check_data_special_characters(product.get('stores'))
            ingredients = check_data_special_characters(product.get('ingredients_text'))
            row = f" \"{brand}\";\"{name}\";\"{categorie}\";\"{code}\";\"{nutrition_grade}\";\"{stores}\";\"{ingredients}\";\"https://world.openfoodfacts.org/product/{code}\";\n"
            output_file.write(row)
            print(id," : ", row)
    print("Nombre d'items importés: {}".format(id))

if __name__ == "__main__":
    download_category_products_OFF()