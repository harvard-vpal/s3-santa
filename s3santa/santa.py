from user import User
import aws
from config import config
from generate_name import generate_name
from user_store import get_user_store


class Santa:
    """
    Class providing main functionality for creating data request users

    TODO command to replace access key for user
    TODO command to update description of user
    """

    def __init__(self, user_store_type, **kwargs):
        self.user_store = get_user_store(user_store_type, **kwargs)

    def create_user(self, username=None, save=True):
        """
        Creates a user. If the user already exists, will return the existing user
        Arguments:
            save (boolean): if true, creates aws resources. if false, only generates a username and checks validity
        """
        # Create user using provided input
        if name:
            user = User(name=username)
            if user.exists:
                return Exception("User already exists, try another username")
        # Generate random username if one not provided as input
        else:
            user = User(name=generate_name())
            while user.exists:
                # try another username if name already taken
                user = User(name=generate_name())
        # create the 
        if save:
            # setup aws resources and generate/save credentials
            user.save()
            # updates spreadsheet/db with user info and credentials
            self.user_store.add_user(user)


    def deliver(self, file, s3_bucket, username, create_user=True):
        """
        Delivers a file to a S3 user folder
        If name not specified, or name doesnt match existing user, creates a new AWS user
        """
        # get or create user
        user = User(name=username)
        # if user doesn't yet exist, we can create one
        if not user.exists:
            if create_user:
                user.save()
                self.user_store.add_user(user)
            else:
                raise Exception("User doesn't exist yet - specify whether user should be created")
        aws.upload_to_s3(args.file, s3_bucket, user.name)
        return "Success: Delivered file {} to user {}".format(file, user.name)


    def cli(self, **kwargs):
        """
        Provides a command line interface to santa methods
        """

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='sub-command help')

        # define subcommand: create-user
        subparser = subparsers.add_parser('create-user')
        subparser.set_defaults(func=getattr(self,'create_user'))
        subparser.add_argument('--user', help="Username of user to create (Leave unspecified to generate a random username)")

        # define subcommand: deliver
        subparser = subparsers.add_parser('deliver')
        subparser.set_defaults(func=getattr(self,'deliver'))
        subparser.add_argument('--user', help="Username of user to deliver file to. (If username does not exist yet, the user will be created)")
        subparser.add_argument('--file', help="File to upload to user data folder")
        
        # parse and execute
        args = parser.parse_args()
        print args.func(args)
