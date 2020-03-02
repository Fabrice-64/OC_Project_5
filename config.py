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

#Message displayed when launching the programm. Used by the method display_message()
WELCOME_MESSAGE = "WELCOME TO 'GET A BETTER DIET' APP \n"

TITLE_0 = "Initial Window"

# These are the dialog strings related to the step dealing with the Terms and Conditions
TITLE_1 = "Open Food Facts Terms and Conditions"
T_C_LINE_1 = "Please first scroll down the Terms and Conditions!"
T_C_LINE_2 = "You can press any key..."
T_C_QUESTION_ACCEPT_T_C = "Do you accept the Terms and Conditions?"
T_C_IF_REFUSAL = "If you do not accept the Terms and Conditions, you'll quit automatically\n"

registered_user_y_n = "Are you a registered user?"

SELECT_ANSWER = "Please select the appropriate answer and press ENTER"
REPLY_YES_NO = ["Yes","No"]