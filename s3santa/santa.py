from .user import User
from .aws import upload_to_s3
from .generate_name import generate_name


class Santa:
    """
    Class providing main functionality for creating data request users

    TODO command to replace access key for user
    TODO command to update description of user
    """

    def __init__(self, s3_bucket, iam_group, user_store):
        self.s3_bucket = s3_bucket
        self.user_store = user_store
        self.iam_group = iam_group

    def generate_user(self):
        """
        Get a username to use, that isn't taken yet
        """
        # Generate random username if one not provided as input
        user = User(name=generate_name())
        while user.exists():
            # try another username if name already taken
            user = User(name=generate_name())
        return user

    def create_user(self, username=None):
        """
        Creates new user. 
        If specified username corresponds to an existing user, an error is raised.
        If not username is specified, a random one is generated.
        Arguments:
            username (str): username of new user to create
        """
        # Create user using provided input
        if username:
            user = User(name=username)
            if user.exists():
                raise Exception("User already exists, try another username")
        # Generate random username if one not provided as input
        else:
            user = self.generate_user()

        # setup aws resources and generate/save credentials
        user.save(self.s3_bucket, self.iam_group, self.user_store)

        return user


    def deliver(self, file, username, **kwargs):
        """
        Delivers a file to a S3 user folder
        If name not specified, or name doesnt match existing user, creates a new AWS user
        """
        # get or create user
        user = User(name=username)
        # if user doesn't yet exist, we can create one
        if not user.exists():
            raise Exception("User {} doesn't exist yet!")
        # upload to bucket under user folder
        upload_to_s3(file, self.s3_bucket, user.name)
        return "Success: Delivered file {} to user {}".format(file, user.name)

