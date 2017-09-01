#!/usr/bin/env python

import argparse
import sys
from user import User
import aws
from config import config


class Santa:

    def __init__(self):
        pass

    def test(self, args):
        print "Ho ho ho"

    def create_user(self, args):
        """
        Creates a user. If the user already exists, will return the existing user
        """
        user = User(name=args.user)
        return user

    def deliver(self, args):
        """
        Delivers a file to a S3 user folder
        If name not specified, or name doesnt match existing user, creates a new AWS user
        """
        # get or create user
        user = User(name=args.user)
        aws.upload_to_s3(args.file, config.S3_BUCKET, user.name)
        return "Success: Delivered file {} to user {}".format(args.file, user.name)


    # TODO command: replace access key for user

    # TODO command: update description of user



def add_subparser(subparsers, name, arguments):
    subparser = subparsers.add_parser(name)
    for argument in arguments:
        subparser.add_argument(argument)
    subparser.set_defaults(func=getattr(Santa(),name.replace('-','_')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    # just testing
    add_subparser(subparsers, 'test', [])

    # define subcommand: create-user
    add_subparser(subparsers, 'create-user', ['--user'])

    # define subcommand: deliver
    add_subparser(subparsers, 'deliver', ['--user','--file'])

    # parse and execute
    args = parser.parse_args()
    print args.func(args)
    





