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
import config_open_food_facts as coff

class ConnectToOFF:

    def check_special_characters(self, value):
        if value is None:
            result = "NaN"
        elif '"' in value:
            new_value = value
            result = new_value.replace('"', '')
        else:
            result = value
        return result


    def import_products(self, category):
        desired_category = {'tag_0': category}
        coff.PAYLOAD.update(desired_category)
        r = requests.get(coff.URL, headers = coff.HEADERS, params = coff.PAYLOAD)
        data = r.json()
        items_left_apart = 0
        nb_imported_items = 0
        row = ""
        with open('response_API.txt', 'w') as output_file:
            for product in data['products']:
                brand = self.check_special_characters(product.get('brands'))
                name = self.check_special_characters(product.get('product_name'))
                category = category
                code = product.get('code')
                nutrition_grade = product.get('nutrition_grade_fr')
                stores = self.check_special_characters(product.get('stores'))
                ingredients = self.check_special_characters(product.get('ingredients_text'))
                if brand != "NaN" and name != "NaN" and nutrition_grade in ["a","b","c","d","e"]:
                    nb_imported_items += 1
                    row = f" \"{brand}\";\"{name}\";\"{category}\";\"{code}\";\"{nutrition_grade}\";\"{stores}\";\"{ingredients}\"\n"
                else:
                    items_left_apart += 1
                output_file.write(row)
        return (nb_imported_items, items_left_apart)

    def import_static_data(self):
        """
            This method import static data and therefore doesn't include the parameters needed in an API.
            In the current application, it imports an excerpt of the Open Food Facts DB categories.
            Parameters are set as constants in the module "config_open_food_facts" module.

            Constants:
            URL_STATIC :  url of the target website and data to be downloaded.

            Attributes:
            self.OFF_category_dict : this is a dictionary containing the downloaded categories from OFF.
            the key is an index ranging from 1 to n, the value is the French name of the category.
            This dictionary is subsequently used in the Controller, get_better_diet, to be displayed and help select new category to be downloaded.

            Args:
            It takes no argument

            Returns:
            It doesn't return anything
        """
        self.OFF_category_dict = {}
        r = requests.get(coff.URL_STATIC)
        data = r.json()        
        counter = 1
        for tag in data[coff.STATIC_TAG]:
            name = tag.get(coff.STATIC_FIELD_0)
            # OFF categories contain mistakes, as a language code,\
            # followed by ':' & then the category. Therefore this rough filter.
            # choice has been made to limit the display of categories
            if ":" not in name and counter <= coff.STATIC_VOLUME:
                if name not in self.OFF_category_dict.values():
                    name = str(name)
                    counter = int(counter)
                    dict_k_v = {counter : name}
                    self.OFF_category_dict.update(dict_k_v)
            counter += 1

if __name__ == "__main__":
    connection = ConnectToOFF()
    connection.import_products()
    #connection.import_static_data()