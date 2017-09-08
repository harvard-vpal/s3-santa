"""
Module containing data request user class
"""

import aws
    

class User:
    """
    Represents a data request user
    Can handle setup
    """
    def __init__(self, name, description=''):
        """
        Arguments:
            name (str): username
        """
        self.name = name
        self.description = description


    def exists(self):
        """"
        indicates whether IAM user with username already exists
        """
        return aws.user_exists(self.name)

    def save(self):
        """
        Creates aws resources
        """
        if self.exists():
            raise Exception("AWS user already exists")
        aws.create_user(self.name)
        aws.create_access_key(self.name)
        aws.add_user_to_group(self.name, self.group)
        aws.create_user_folder(self.name)
