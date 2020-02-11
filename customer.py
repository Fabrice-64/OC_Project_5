""""
This module deals with interactions between the user and the interface of this programm.

They can be described as follows:
-Get a list of items responding to the selected criteria
-Input a new item into the DB
-Amend an already existing item

"""
def input_selected_category():
#Function to choose the category
    pass

def compare_item():
#Function to select the item based on category, name and nutrition grade
    pass

def ask_launch_search():
# Once the required fields are filled, gives the order to look into the DB.
# This function is directly linked to the module named 'connect_to_my_sql.py"
    pass

def input_new_item():
# Function to add an item to the database and record it 
    pass

def amend_existing_item_in_db():
# Amend an item should occur after a realizing that an item is not full.
# Therefore, the item is first called
    pass

def find_archived_search():
# Request to get archived queries
    pass

def select_user_interaction_with_db():
# First step for the user iot select the desired functionality
    pass

if __name__ == "__main__":
    select_interaction_with_db()