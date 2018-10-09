#!/usr/bin/env python

"""
Runs the s3santa CLI

Example usage:

    python santa.py --create-user
"""
import os
from s3santa.cli import SantaCli
from s3santa.santa import Santa
from s3santa.user_store import GoogleSpreadsheet

S3_BUCKET = os.environ.get('S3_BUCKET')
IAM_GROUP = os.environ.get('IAM_GROUP')
GOOGLE_KEYFILE = os.environ.get('GOOGLE_KEYFILE')
GOOGLE_SPREADSHEET_ID = os.environ.get('GOOGLE_SPREADSHEET_ID')

# define the user storage to use with santa
user_store = GoogleSpreadsheet(
    spreadsheet_id=GOOGLE_SPREADSHEET_ID,
    google_keyfile=GOOGLE_KEYFILE,
)

# create santa helper
santa = Santa(S3_BUCKET, IAM_GROUP, user_store)

# run santa cli
SantaCli(santa).run()
