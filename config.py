"""
    
Purpose of this module is to gather the various constants used all along this program

Classes:
NIL.
    
Exceptions:
NIL.
    
Functions:
NIL.

"""
DB_CONNECTION_PARAMETERS = {'user': 'root',
                            'host': 'localhost', 'database': 'get_better_diet'}

# Message displayed when launching the programm. Used by the method display_message()
WELCOME_MESSAGE = "WELCOME TO 'GET A BETTER DIET' APP \n"
TITLE_0 = "Initial Window"

# The following lines deals with the successive comments, questions, window titles to be used at each step of the program
# These are the dialog strings related to the step dealing with the Terms and Conditions
TITLE_1 = "Open Food Facts Terms and Conditions"
T_C_FILE = "Documentation/texte_T&C.txt"
T_C_LINE_1 = "Please first scroll down the Terms and Conditions!\n"
T_C_LINE_2 = "You can press any key...\n"
T_C_QUESTION_ACCEPT_T_C = "Do you accept the Terms and Conditions?\n"
T_C_IF_REFUSAL = "If you do not accept the Terms and Conditions, you'll quit automatically\n"
T_C_APPROVAL = "You have decided to go on with this App\n"

# These are the dialog strings related to the step dealing with the actions to be conducted
TITLE_2 = "Working with the Databases"
S_A_INFO_LINE_1 = "Please select in the list below the action you are interested in\n"
S_A_INFO_LOC_DISPLAY_RESULTS = "The results will be displayed in this window\n"
S_A_OPERATE_ON_DB = ["Look for a substitution food item",
                     "Get to the previous searches", "Upload a new category", "Quit"]

S_A_SIZE_LOCAL_DB = 'Your local database currently counts : {} food items'

S_A_PROCESSING_RECORD = "Your selection is being recorded."

# These are the dialog strings to select a substition food item
TITLE_3 = "Looking for a substitution food item"
S_A_SELECT_CATEGORY = "Please type the number of the selected category if you wish to:\n"
S_A_ITEM_NAME = "Please name the food item for which you are looking for a substitution:\n"
S_A_ITEM_BRAND = "Please name the brand of this food item:\n"
S_A_ITEM_CODE = "Please type the id code of the product:\n"
S_A_INFO_ITEM_SEARCH_OUTCOME = "Here is a selection of food items we have found:\n"
S_A_COMPARE_FOOD_ITEMS = "Please Enter the Food Item you wish to compare with:\n"
S_A_ADD_KEYWORDS = "Please enter one or two keywords in order to have a larger choice:\n"

S_A_INDEX_NAME = "{}:  {}\n"
S_A_DISPLAY_BRAND_NUTRISCORE = "Brand: {}, Nutrition grade: {}\n"
S_A_DISPLAY_STORES = "Stores: {}\n"
S_A_DISPLAY_INITIAL_PRODUCT = "Initial product was: {}\n"
S_A_COMPARRISON_DATE = "Comparrison was on: {: %d %B %y %H:%M}.\n"
S_A_SINGLE_RETURN = "\n"

# These are the dialog strings dealing with the DB consultation.
S_A_ASK_CHECK_DETAILED_RESULT = "Do you want to check the result on the Web (Y/N)?\n"
S_A_USE_BROWSER = "Please select the item you want to check on the official website:\n"
S_A_ASK_RECORD_SELECTED_ITEM = "Do you want to record this research for further use (Y/N)\n?"

# These are the dialog strings to download and upload an excerpt of Open Food Facts DB
S_A_INFO_ADD_NEW_CATEGORY = "You ought to select a category to import to your local DB.\n"
S_A_INFO_NAME_IMPORTED_CATEGORY = "You will import : "

# These are the dialog strings displayed when retrieving recorded previous searches
S_A_INFO_LAST_RECORDS = "Here are your last records\n"
S_A_USE_BROWSER = "Please select the item you want to check on the official website:\n"
S_A_GO_ON_CHECK_FOOD_ITEMS_Y_N = "Do you want to select another food item (Y/N?\n"


# These are the keyboard information lines to deal with the textpad
USER_GUIDE = ["User's Guide:",
              "THE NUMERIC KEYPAD IS NOT ACTIVATED",
              "Press Ctrl+B to have the cursor go left.",
              "Press Ctrl+D to delete the character under the cursor.",
              "Press Ctrl+H to delete a character backwards.",
              "Press Ctrl+E to go to the end of line.",
              "Press Ctrl+G or ENTER to terminate the operation."]

# These are the instructions displayed when using the keypad
KEYPAD_INSTRUCTION_1 = "Please input your selection in the box below.\n"


SELECT_ANSWER = "Please select the appropriate answer and press ENTER\n"
SELECT_Y_N = "Press Y to continue, N to interrupt.\n"
REPLY_YES_NO = ["Yes", "No"]

WARNING_MESSAGE_0 = "PLEASE ENTER A CORRECT VALUE"
WARNING_MESSAGE_1 = "YOUR SEARCH IS TO RESTRICTIVE, BE LESS SPECIFIC"
WARNING_MESSAGE_2 = "NO FOOD ITEM MATCHES YOUR REQUEST, NEW CRITERION ARE NEEDED"

# Miscellaneous messages.
BACK_MAIN_MENU = "You are going back to the main menu."
QUIT_MESSAGE = "The program will quit in a few seconds\n"
