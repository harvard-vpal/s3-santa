import argparse
from distutils.util import strtobool

class SantaCli(object):
    """
    Class for running a CLI interface to a santa instance
    """
    def __init__(self, santa):
        self.santa = santa
        self.setup_parser()
        

    def setup_parser(self, **kwargs):
        """
        Provides a command line interface to santa methods
        """
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='sub-command help')

        # define subcommand: create-user
        subparser = subparsers.add_parser('create-user')
        subparser.set_defaults(func=getattr(self,'create_user'))
        subparser.add_argument('--user', dest='username', help="Username of user to create (Leave unspecified to generate a random username)")

        # define subcommand: deliver
        subparser = subparsers.add_parser('deliver')
        subparser.set_defaults(func=getattr(self.santa,'deliver'))
        subparser.add_argument('--user', dest='username', help="Username of user to deliver file to. (If username does not exist yet, the user will be created)")
        subparser.add_argument('--file', help="File to upload to user data folder")
        

    def run(self):
        # parse and execute
        args = self.parser.parse_args()
        args.func(**vars(args))


    def generate_user(self):
        user = self.santa.generate_user()
        print("Generated user: {}".format(user.name))


    def create_user(self, username=None, save=True):
        """
        2-step process for creating users if name not specified (adds confirmation step)
        """
        if username:
            user = self.santa.create_user(username)
        else:
            user = self.santa.generate_user()
            confirm_create = strtobool(input('Create user "{}"? [y/n] '.format(user.name)))
            if not confirm_create:
                print("User creation cancelled")
                return
            user = self.santa.create_user(user.name)
        print("Successfully created new data request user {}".format(user.name))
