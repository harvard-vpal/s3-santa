"""
Module containing data request user class
"""

import aws
    

class User:
    """
    Represents a data request user
    Can handle setup
    """
    def __init__(self, name):
        """
        Arguments:
            name (str): username
        """
        self.name = name
        # indicates whether IAM user with username already exists
        self.exists = aws.user_exists()


    def save(self):
        """
        Creates aws resources
        """
        if self.exists():
            raise Exception("AWS user already exists")
        aws.create_user(self.name)
        self.exists = True
        aws.create_access_key(self.name)
        aws.add_user_to_group(self.name, self.group)
        aws.create_user_folder(self.name)
