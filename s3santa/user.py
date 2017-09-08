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

    def save(self, s3_bucket, iam_group, user_store):
        """
        Creates aws resources for user and saves to user store
        """
        if self.exists():
            raise Exception("AWS user already exists")
        # create iam user
        aws.create_user(self.name)
        # create keypair
        self.access_key_id, self.secret_access_key = aws.create_access_key(self.name)
        # add user to data requests IAM group
        aws.add_user_to_group(self.name, iam_group)
        # create user folder (labeled by username) in s3 bucket
        aws.create_s3_folder(s3_bucket, self.name)
        # updates spreadsheet/db with user info and credentials
        user_store.add_user(self)
