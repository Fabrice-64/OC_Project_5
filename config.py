"""
Purpose of this module is to set the constant datas used all along this program

payload, headers and url are used fetch data from the Open Food Facts DB

"""
db_connection_parameters = {'user' :'root', 'host' : 'localhost', 'database' : 'get_better_diet'}

#Message displayed when launching the programm. Used by the method display_message()
WELCOME_MESSAGE = "WELCOME TO 'GET A BETTER DIET' APP \n"
TITLE_0 = "Initial Window"

# The following lines deals with the successive comments, questions, window titles to be used at each step of the program
# These are the dialog strings related to the step dealing with the Terms and Conditions
TITLE_1 = "Open Food Facts Terms and Conditions"
T_C_LINE_1 = "Please first scroll down the Terms and Conditions!\n"
T_C_LINE_2 = "You can press any key...\n"
T_C_QUESTION_ACCEPT_T_C = "Do you accept the Terms and Conditions?\n"
T_C_IF_REFUSAL = "If you do not accept the Terms and Conditions, you'll quit automatically\n"

# These are the dialog strings related to the step dealing with the actions to be conducted
TITLE_2 = "Working with the Databases"
S_A_INFO_LINE_1 = "Please select in the list below the action you are interested in\n"
S_A_OPERATE_ON_DB = ["Search for substitution food", "Find a previous search", "Upload a new category", "Quit"]

S_A_NUMBER_DOWNLOADED_ITEMS = '{} food items have been downloaded from Open Food Facts'

S_A_PROCESSING_RECORD = "Your selection is about to be recorded"

# These are the dialog strings to select a substition food item
TITLE_3 = "Looking for a substitution food item"
S_A_SELECT_CATEGORY = "Please type the number of the selected category if you wish to:\n"
S_A_NAME_FOOD_ITEM = "Please name the food item for which you are looking for a substitution:\n"
S_A_NAME_ITEM_BRAND = "Please name the brand of this food item:\n"
S_A_NAME_ITEM_CODE = "Please type the id code of the product:\n"


# These are the dialog strings to download and upload an excerpt of Open Food Facts DB
S_A_INFO_ADD_NEW_CATEGORY = "You ought to look into Open Food Facts which category you want to add to your local DB"

# These are the keyboard information lines to deal with the textpad
KEYBOARD_INFO_00 = "User's Guide:"
KEYBOARD_INFO_0 = "THE NUMERIC KEYPAD IS NOT ACTIVATED" 
KEYBOARD_INFO_1 = "Press Ctrl+B to have the cursor go left"
KEYBOARD_INFO_2 = "Press Ctrl+D to delete the character under the cursor"
KEYBOARD_INFO_3 = "Press Ctrl+H to delete a character backwards"
KEYBOARD_INFO_4 = "Press Ctrl+E to go to the end of line"
KEYBOARD_INFO_5 = "Press Ctrl+G or ENTER to terminate the operation"

#These are the instructions displayed when using the keypad
KEYPAD_INSTRUCTION_1 = "Please input your selection in the box below\n"


SELECT_ANSWER = "Please select the appropriate answer and press ENTER\n"
REPLY_YES_NO = ["Yes","No"]

WARNING_MESSAGE_0 = """PLEASE ENTER A CORRECT VALUE"""

# Miscellaneous messages.
BACK_MAIN_MENU = "You are going back to the main menu.\n"