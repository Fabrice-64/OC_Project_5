"""
Purpose of this module is to manage user functionalities

It encompasses:
Downloading of selected categories from Open Food Facts Database
Fill the database subsequently to the download
Partly or totally empty the database whenever deemed necessary

"""

class User:
    def __init__(self):
        pass

    def confirm_user_in_db(self):
        pass

    def create_user(self):
        pass

class SuperUser(User):
    def fetch_category_from_OFF_website(self):
        """ Method initiating the download of a selected category from OFF using an API. 
        This method cleans the data as well"""
        pass
    def upload_data_to_DB(self):
    # Function to upload the data into mySQL
        pass

    def reset_DB(self):
    # Function to partly or totally reset the database
        pass

class Customer(User):
    pass
