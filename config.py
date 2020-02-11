categories = ["yaourts","pizzas", "beverages", "snacks", "dairies", "groceries","canned_foods","desserts"]

category_choice = 0
OFF_PAGE = 1

payload = {'search_terms': categories[category_choice],'json': 1, 'action' : "process", \
    'fields' : "brands,product_name,code,stores,nutrition_grade_fr,ingredients_text","page_size": 1000, "page": OFF_PAGE}

headers = {'User-Agent': 'python-requests/2.22.0'}

url = 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1'

connection_to_database = {'user' :'root', 'host' : 'localhost', 'database' : 'Project_5_OC'}

welcome_message = "WELCOME TO 'GET A BETTER DIET' PROGRAM"