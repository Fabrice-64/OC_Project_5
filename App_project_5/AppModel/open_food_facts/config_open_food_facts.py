"""

    This module encompasses all the parameters needed for Open Food Facts API.

    Class:

    NIL

    # Exceptions:

    NIL

    Functions:

    NIL

    """

# Updload data from Open Food Facts
NUMBER_REJECTED_ITEMS = '{} food items have rejected because of bad data'
NUMBER_DOWNLOADED_ITEMS = '{} food items have been downloaded \
from Open Food Facts'

# Limit the import of data to 1 page & avoid to overload the local DB.
OFF_PAGE = 1

# Required to get access to the DB. They are defined by OFF administrators.
HEADERS = {'User-Agent': 'python-requests/2.22.0'}

# This payload is used in the API to get selected data.
PAYLOAD = {
          'tagtype_0': 'categories', 'tag_contains_0': 'contains',
          'tag_0': '', 'tag_types_1': 'countries',
          'tag_contains_1': 'contains', 'tag_1': 'fr',
          'json': 1, 'action': "process",
          'fields': "brands,product_name,code,stores,nutrition_grade_fr,categories",
          "page_size": 1000, 'page': OFF_PAGE}

# The OFF DB is to be found here. It is completed by other components,
# as the payload, the headers, categories, etc.
URL = 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1'

# Parameters used to import stores or categories, as static data from OFF.
URL_STATIC_STORES = 'https://fr.openfoodfacts.org/stores.json'
URL_STATIC_CAT = 'https://fr.openfoodfacts.org/categories.json'
STATIC_TAG = 'tags'
STATIC_FIELD_0 = 'name'
STATIC_VOLUME = 30000

# This is the address to be used to import a product.
# The product code is added right behind.
OFF_PRODUCT_ADDRESS = "https://world.openfoodfacts.org/product/"
