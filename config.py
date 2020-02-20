"""
Purpose of this module is to set the constant datas used all along this program

payload, headers and url are used 
"""

categories = ["yaourts","pizzas", "beverages", "snacks", "dairies", "groceries","canned_foods","desserts"]

category_choice = 0
OFF_PAGE = 1


payload = {'search_terms': categories[category_choice],'json': 1, 'action' : "process", \
    'fields' : "brands,product_name,code,stores,nutrition_grade_fr,ingredients_text","page_size": 1000, "page": OFF_PAGE}

headers = {'User-Agent': 'python-requests/2.22.0'}

url = 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1'

db_connection_parameters = {'user' :'root', 'host' : 'localhost', 'database' : 'Project_5_OC'}

welcome_message = "WELCOME TO 'GET A BETTER DIET' PROGRAM"

registered_user_y_n = "Are you a registered user?"

reply_yes_no_quit = ["Yes","No","Quit"]