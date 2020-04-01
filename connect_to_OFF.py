"""

Downloads the requested data from Open Food Facts DB using an API.

To be noticed: dowloaded data are filtered by downloading. If some fields deemed \
    as absolutely necessary are not field, the row is discarded.

Classes:
ConnectToOFF: manage the connection settings through the API an the data download.

Exceptions:
NIL.
    
Functions:
NIL.


"""
import requests
import json
import config_open_food_facts as coff
import webbrowser


class ConnectToOFF:
    """

    Manage the relations with the Open Food Facts Database through an API.

    Methods:
    check_special_characters(): remove the quotation marks of any type to prepare \
        the data for the upload to mysql DB.

    import_products_list():  downloads a list of items from OFF.

    import_static_data():   import data which are not subject to change, like categories, etc.

    open_product_file_OFF(): opens from OFF, in a web browser the file of a specific product.

    Instance variables:
    self.list_items (list): encompasses all the items downloaded from OFF.

    self.OFF_category_list (list): contains the names of the categories imported as static data.

    """

    def __init__(self):
        """

            Initialize the class

            Arguments:
                NIL.

            Returns:
                NIL.

        """
        self.list_items = []

    def check_special_characters(self, value):
        """

            Cleans the fields of the downloaded rows in order to avoid conflicts with mySQL syntax.

            Arguments:
                value: is a string to be checked.

            Returns:
                result: value cleaned from the various quotation marks or identified as empty.

        """
        if value is None:
            result = "NaN"
        elif '"' in value:
            new_value = value
            result = new_value.replace('"', '')
        elif "'" in value:
            new_value = value
            result = new_value.replace("'", "\'")
        else:
            result = value
        return result

    def import_products_list(self, category):
        """

        Imports a large list of food items, based on a selected category.

        Arguments:
        category: selected from a predefined list of possible categories.

        Returns:
        nb_imported_items: out of a selected range, number of food items considered \
            as valid for import.

        items_left_apart: out of the initial range, number of food items discarded \
            because of poor quality of the data.

        """
        desired_category = {'tag_0': category}
        coff.PAYLOAD.update(desired_category)
        r = requests.get(coff.URL, headers=coff.HEADERS, params=coff.PAYLOAD)
        data = r.json()
        items_left_apart = 0
        nb_imported_items = 0
        for product in data['products']:
            brand = self.check_special_characters(product.get('brands'))
            name = self.check_special_characters(product.get('product_name'))
            category = self.check_special_characters(category)
            code = product.get('code')
            nutrition_grade = product.get('nutrition_grade_fr')
            stores = self.check_special_characters(product.get('stores'))
            ingredients = self.check_special_characters(
                product.get('ingredients_text'))
            if brand != "NaN" and name != "NaN" and nutrition_grade in ["a", "b", "c", "d", "e"]:
                nb_imported_items += 1
                self.list_items.append(
                    (brand, name, category, code, nutrition_grade, stores, ingredients))
            else:
                items_left_apart += 1
        return (nb_imported_items, items_left_apart, self.list_items)

    def import_static_data(self):
        """

        This method import categories, which are static data and therefore doesn't \
            include the parameters needed in an API.
        On Open Food Facts DB, the categories are sorted out by number of entries. \
            Therefore, this method picks some of the most popular categories in OFF DB.

        Arguments:
        NIL.

        Returns:
        self.OFF_category_list : list of categories selected for later download. 

        """
        self.OFF_category_list = []
        r = requests.get(coff.URL_STATIC)
        data = r.json()
        counter = 1
        for tag in data[coff.STATIC_TAG]:
            name = tag.get(coff.STATIC_FIELD_0)
            # Some inconsistant fields have been remarked. This is an ad hoc way to remove those rows.
            if ":" not in name and counter <= coff.STATIC_VOLUME:
                if name not in self.OFF_category_list:
                    name = str(name)
                    self.OFF_category_list.append(name)
                    counter += 1
        return self.OFF_category_list

    def open_product_file_OFF(self, code_product):
        """

        Opens the page of a selected product in the default browser.

        Arguments:
        code_product: completes the address where to find this very food item.

        Returns:
        NIL.

        """
        product_location = str(coff.OFF_PRODUCT_ADDRESS + code_product)
        webbrowser.open(product_location, new=1)


if __name__ == "__main__":
    connection = ConnectToOFF()
