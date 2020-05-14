"""
    
    Purpose of this module is to gather the various constants used all along this program

    Classes:

    NIL.
        
    Exceptions:

    NIL.
        
    Functions:
    
    NIL.

    """
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = '/get_better_diet'
DB_CONNEXION_STRING = "mysql+mysqlconnector://{}:{}@localhost{}"

# Message displayed when launching the programm. Used by the method display_message()
WELCOME_MESSAGE = "WELCOME TO 'GET A BETTER DIET' APP \n"
TITLE_0 = "Initial Window"

# The following lines deals with the successive comments, questions, window titles to be used at each step of the program
# These are the dialog strings related to the step dealing with the Terms and Conditions
TITLE_1 = "Open Food Facts Terms and Conditions"
T_C_FILE = "texte_T&C.txt"
T_C_LINE_1 = "Please first scroll down the Terms and Conditions!\n"
T_C_LINE_2 = "You can press any key...\n"
ACCEPT_T_C = "Do you accept the Terms and Conditions?\n"
IF_REFUSAL = "If you do not accept the Terms and Conditions, you'll quit automatically\n"
T_C_APPROVAL = "You have decided to go on with this App\n"

# These are the dialog strings related to the creation of the DB
DB_CREATE_LOCAL_DB = "A new DB will be created\n"
DB_CATEGORIES_FETCHED = "The names of the french categories have been uploaded\n"
DB_STORES_FETCHED = "The names of the stores have been uploaded\n"
DB_INITIAL_INFO = "Please follow the instructions to create a new DB\n"
DB_USER_INVITE = "Please enter the user if you have defined one ('root' by default)\n"
DB_PASSWORD_INVITE = "Please enter the password to your DB (None by default)\n"

# These are the dialog strings related to the step dealing with the actions to be conducted
TITLE_2 = "Working with the Databases"
INFO_LINE_1 = "Please select in the list below the action you are interested in\n"
INFO_DISPLAY_RESULTS = "The results will be displayed in this window\n"
OPERATE_ON_DB = ["Look for a substitution food item",
                     "Get to the previous searches", "Upload a new category",
                     "Quit"]
CAT_RANK_NAME = "{} : {}\n"
EMPTY_DB = "DON'T FORGET TO FIRST LOAD SOME ITEMS IN YOUR LOCAL DB !"
ROWS_LOCAL_DB = 'Your local database currently counts : {} food items'

PROCESSING_RECORD = "Your selection is being recorded."
BE_PATIENT = "Be patient, Work in Progress"

# These are the dialog strings to select a substition food item
TITLE_3 = "Looking for a substitution food item"
SELECT_CATEGORY = "Please type the number of the selected category (REQUIRED):\n"
ITEM_NAME = "Please name the food item for which you are looking for a substitution:\n"
ITEM_BRAND = "Please name the brand of this food item:\n"
ITEM_SEARCH_OUTCOME = "Here is a selection of food items we have found:\n"
COMPARE_FOOD_ITEMS = "Please Enter the Food Item you wish to compare with:\n"
ADD_KEYWORDS = "Please enter one or two keywords in order to have a larger choice:\n"

RANK_NAME_QTY = "{}:  {} ({} items)\n"

PRODUCT_RANK_NAME = "{}:  {}\n"
PRODUCT_BRAND_NUTR_GR = "Brand: {}, Nutrition grade: {}\n"
DISPLAY_STORES = "Stores: {}\n"
INITIAL_PRODUCT = "Initial product was: {}\n"
COMPARRISON_DATE = "Comparrison was on: {}\n \n"
EMPTY_LINE = "\n"

# These are the dialog strings dealing with the DB consultation on the web.
CHECK_DETAILED_RESULT = "Do you want to check the result on the Web (Y/N)?\n"
USE_BROWSER = "Please select the item you want to check on the official website:\n"
RECORD_SELECTED_ITEM = "This result will be automatically recorded. \n"

# These are the dialog strings to download and upload an excerpt of Open Food Facts DB
ADD_CATEGORY = "You ought to select a category to import to your local DB.\n"
NAME_IMPORTED_CATEGORY = "You will import : "

# These are the dialog strings displayed when retrieving recorded previous searches
INFO_LAST_RECORDS = "Here are your last records\n"
CHECK_AGAIN_ITEMS_Y_N = "Do you want to select a food item (Y/N)?\n"


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
WARNING_MESSAGE_3 = "NO BEST PRODUCT RECORDED IN THE DB (WAS MAY BE UPDATED)"
WARNING_MESSAGE_4 = "THE APP COULD NOT FIND THE DB, PLEASE CREATE ONE FIRST"

# Miscellaneous messages.
BACK_MAIN_MENU = "You are going back to the main menu."
QUIT_MESSAGE = "The program will quit in a few seconds\n"
