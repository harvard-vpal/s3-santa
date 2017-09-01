from generate_name import generate_name
import aws
from google_spreadsheet import GoogleSpreadsheet
from local_csv import LocalCSV
from config import config


class User:
    def __init__(self,name=None,description=None):
        """
        Get or create user with specified username
        On creation, attach to group
        """
        self.usernames = aws.list_users()

        # create new user
        if not name or name not in self.usernames:
            self.create_user(name)
            self.create_access_key()
            # add to group
            self.add_user_to_group()
            self.description = description
            # create user folder
            self.create_user_folder()

            # update google
            spreadsheet = GoogleSpreadsheet()
            spreadsheet.add_user(self)

            # update csv
            csvfile = LocalCSV()
            csvfile.add_user(self)

        # get existing user
        else:
            user = aws.get_user(name)
            self.name = user['User']['UserName']
            # TODO get access keys from spreadsheet
            print "Identified existing user: {}".format(self.name)

    def create_user(self,name=None):
        """
        Generate a new IAM user on the AWS account
        If name not specified, uses generate_name to generate one
        """
        while name in self.usernames or not name:
            name = generate_name()
        
        self.name = aws.create_user(name)['User']['UserName']


    def create_access_key(self):
        """
        Generate access key for user
        """
        access_key = aws.create_access_key(self.name)
        self.access_key_id = access_key['AccessKeyId']
        self.secret_access_key = access_key['SecretAccessKey']
        # print 'Created access key {}... for user: {}'.format(
        #     self.access_key_id[:8],
        #     self.name
        # )

    def add_user_to_group(self):
        """
        Add user to group
        """
        aws.add_user_to_group(self.name,config.IAM_GROUP)

    def create_user_folder(self):
        """
        Create s3 folder for user named using username
        """
        aws.create_s3_folder(config.S3_BUCKET,self.name)

    def delete_user(self,name):
        """
        TODO Delete user
        """
        # delete from aws
        # delete from google / local databases
        pass

    def update_description(self,name):
        """
        TODO Set user description on csv/gspread
        """
        pass

    def update_google_spreadsheet(self):
        spreadsheet = GoogleSpreadsheet()
        spreadsheet.add_record(self)
