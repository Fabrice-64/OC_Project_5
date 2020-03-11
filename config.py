"""
Purpose of this module is to set the constant datas used all along this program

payload, headers and url are used fetch data from the Open Food Facts DB

"""

# Updload data from Open Food Facts
categories = ["yaourts","pizzas", "beverages", "snacks", "dairies", "groceries","canned_foods","desserts"]

category_choice = 0
OFF_PAGE = 1
# The headers are required to get access to the DB. They are defined by OFF administrators.
headers = {'User-Agent': 'python-requests/2.22.0'}
# The payload is used in the API to get selected data.
payload = {'search_terms': categories[category_choice],'json': 1, 'action' : "process", \
    'fields' : "brands,product_name,code,stores,nutrition_grade_fr,ingredients_text","page_size": 1000, "page": OFF_PAGE}
# This url is where the OFF DB is to be found. It is completed by other components, as the payload, the headers, categories, etc.
url = 'https://fr.openfoodfacts.org/cgi/search.pl?search_simple=1'



db_connection_parameters = {'user' :'root', 'host' : 'localhost', 'database' : 'get_better_diet'}

#Message displayed when launching the programm. Used by the method display_message()
WELCOME_MESSAGE = "WELCOME TO 'GET A BETTER DIET' APP \n"
TITLE_0 = "Initial Window"

# The following lines deals with the successive comments, questions, window titles to be used at each step of the program
# These are the dialog strings related to the step dealing with the Terms and Conditions
TITLE_1 = "Open Food Facts Terms and Conditions"
T_C_LINE_1 = "Please first scroll down the Terms and Conditions!"
T_C_LINE_2 = "You can press any key..."
T_C_QUESTION_ACCEPT_T_C = "Do you accept the Terms and Conditions?"
T_C_IF_REFUSAL = "If you do not accept the Terms and Conditions, you'll quit automatically\n"

# These are the dialog strings related to the step dealing with the actions to be conducted
TITLE_2 = "Working with the Databases"
S_A_INFO_LINE_1 = "Please select in the list below the action you are interested in\n"
S_A_OPERATE_ON_DB = ["Search for substitution food", "Find a previous search", "Upload a new category", "Quit"]

# These are the dialog string to select a substition food item
S_A_SELECT_CATEGORY = "Please type the number of the selected category:"

# These are the keyboard information lines to deal with the textpad
KEYBOARD_INFO_0 = "User's Guide:"
KEYBOARD_INFO_1 = "Press Ctrl+B to have the cursor go left"
KEYBOARD_INFO_2 = "Press Ctrl+D to delete the character under the cursor"
KEYBOARD_INFO_3 = "Press Ctrl+H to delete a character backwards"
KEYBOARD_INFO_4 = "Press Ctrl+E to go to the end of line"
KEYBOARD_INFO_5 = "Press Ctrl+G or ENTER to terminate the operation"

#These are the instructions displayed when using the keypad
KEYPAD_INSTRUCTION_1 = "Please input your selection in the box below"


SELECT_ANSWER = "Please select the appropriate answer and press ENTER"
REPLY_YES_NO = ["Yes","No"]