import os
import json


def run(cmd,parse=True):
    '''
    Run a system command and optionally return the result as a dictionary
    '''
    if parse:
        with os.popen(cmd) as f:
            try:
                cmd_result_parsed = json.load(f)
            except ValueError:
                raise ValueError(f.read()) 
        return cmd_result_parsed
    else:
        status = os.system(cmd)
        if status is not 0:
            # run again to print the error
            run(cmd,parse=True)
    

def list_users(group=None):
    '''
    Returns a list of usernames
    '''
    if not group:
        results = run("aws iam list-users")
    else:
        results = run("aws iam get-group")
    usernames = [user['UserName'] for user in results['Users']]
    return usernames

def create_user(username):
    '''
    Creates a new IAM user and returns the username
    '''
    results = run("aws iam create-user --user-name {}".format(username))
    # username = results['User']['UserName']
    print "Created IAM user: {}".format(username)
    return results
    

def create_access_key(username):
    '''
    Creates an access key pair for an IAM user
    '''
    results = run("aws iam create-access-key --user-name {}".format(username))
    access_key = {
        'AccessKeyId':results['AccessKey']['AccessKeyId'],
        'SecretAccessKey':results['AccessKey']['SecretAccessKey']
    }
    print "Created access key for user {}".format(username)
    return access_key


def get_user(username):
    '''
    Get info about an existing user
    '''
    results = run("aws iam get-user --user-name {}".format(username))
    return results

def user_exists(username):
    '''
    Returns True if the user exists
    '''
    usernames = list_users()
    return bool(username in usernames)

def add_user_to_group(username, group):
    '''
    attach user to group
    '''
    results = run(
        "aws iam add-user-to-group --user-name {} --group-name {}".format(
            username,
            group,
        ),
        parse=False
    )
    print "User {} added to group {}".format(username,group)

def upload_to_s3(file,bucket,username):
    '''
    upload a file to a user's folder
    '''
    if not os.path.exists(file):
        raise ValueError("Specified file or directory not found")

    results = run(
        "aws s3 cp {} s3://{}/{}/ {}".format(
            file,
            bucket,
            username,
            '--recursive' if os.path.isdir(file) else ''
        ),
        parse=False
    )

# def create_s3_folder(bucket,username):
#     '''
#     TODO Create a user folder on s3
#     '''
#     pass

if __name__=="__main__":
    pass

