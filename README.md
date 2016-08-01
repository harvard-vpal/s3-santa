# s3-santa
Data request user manager for s3

## Dependencies
* awscli
* gspread
* oauth2client

## Setup
* [Install](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) the AWS CLI
* [Configure](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) the AWS CLI
* Create an S3 bucket

## Usage
```
# create user
python santa.py create-user --user <USER>

# deliver file to user
python santa.py deliver --file <FILE> --user <USER>

# generate a user and deliver a file
python santa.py deliver --file <FILE>
```
