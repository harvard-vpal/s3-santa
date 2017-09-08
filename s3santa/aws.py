"""
Utility module for calling aws endpoints and parsing results
"""

import boto3


iam = boto3.client('iam')
s3 = boto3.client('s3')
    

# def list_users(group=None):
#     """
#     Returns a list of usernames that exist in the aws account
#     Arguments:
#         group (str): if included, 
#     """
#     if not group:
#         results = iam.list_users()
#     else:
#         results = iam.get_group()
#     usernames = [user['UserName'] for user in results['Users']]
#     return usernames


def create_user(username):
    """
    Creates a new IAM user and returns the username
    """
    results = iam.create_user(UserName=username)
    username = results['User']['UserName']
    print "[AWS] Created IAM user: {}".format(username)
    return username
    

def create_access_key(username):
    """
    Creates an access key pair for an IAM user
    """
    results = iam.create_access_key(UserName=username)
    keypair = (
        results['AccessKey']['AccessKeyId'],
        results['AccessKey']['SecretAccessKey']
    )
    print "[AWS] Created access key for user {}".format(username)
    return keypair


def get_user(username):
    """
    Get info about an existing user
    Arguments:
        username (str): username to look up
    """
    results = iam.get_user(UserName=username)
    return results


def user_exists(username):
    """
    Returns True if the user exists, False if they do not exist
    """
    try: 
        get_user(username)
        return True
    except iam.exceptions.NoSuchEntityException:
        return False


def add_user_to_group(username, group):
    """
    Attach user to IAM group
    """
    results = iam.add_user_to_group(UserName=username, GroupName=group)
    print "[AWS] User {} added to group {}".format(username,group)


def upload_to_s3(file, bucket, username, key_suffix=None):
    """
    Upload a file to a user's folder.
    Key format is:
        s3://<bucket_name>/<username>/<key_suffix>
    """
    # check if local file exists
    if not os.path.exists(file):
        raise ValueError("Specified file or directory not found")

    if key_suffix:
        key = "{}/{}".format(username, key_suffix)
    else:
        key = username

    s3.upload_file(file, bucket, key)
    print "[AWS] Uploaded file {} to s3://{}/{}".format(file, bucket, key)


def create_s3_folder(bucket,foldername):
    """
    Create a folder on s3
    """
    results = s3.put_object(
        Bucket=bucket,
        Key="{}/".format(foldername)
    )
    print "[AWS] Created folder s3://{}/{}".format(bucket,foldername)


if __name__=="__main__":
    pass
