"""
This module encompasses all the parameters needed for Open Food Facts API
"""
# Updload data from Open Food Facts
categories = ["yaourts","pizzas", "beverages", "snacks", "dairies", "groceries","canned_foods","desserts"]

category_choice = 1
OFF_PAGE = 1
# The headers are required to get access to the DB. They are defined by OFF administrators.
HEADERS = {'User-Agent': 'python-requests/2.22.0'}
# The payload is used in the API to get selected data.
PAYLOAD = {'search_terms': categories[category_choice],'json': 1, 'action' : "process", \
    'fields' : "brands,product_name,code,stores,nutrition_grade_fr,ingredients_text","page_size": 1000, "page": OFF_PAGE}
# This url is where the OFF DB is to be found. It is completed by other components, as the payload, the headers, categories, etc.
URL = 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1'