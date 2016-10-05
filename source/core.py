#!/usr/bin/env python
from config import Config
from file import File,scan_folder,delete_none_existing_files
from pprint import pprint
from aws import AWS
import sys
import logging
import os
import platform
import argparse

def upload(overwrite):
    logging.info('Uploading files to S3')
    for folder in config.config['folders']:
        aws = AWS()

        files = scan_folder(folder["path"],True,folder["ignore"])
        file_objects = []
        for file_path in files:
            file = File(file_path,folder["path"],folder["bucket_name"],folder['bucket_path'])
            file.upload(overwrite)
            file_objects.append(file)

    logging.info('Deleting files from S3')
    delete_none_existing_files(folder["bucket_name"],folder['bucket_path'],file_objects)

    logging.info('Finished')

#setup argument parsing
parser = argparse.ArgumentParser(description='S3 backup utility')
subparsers = parser.add_subparsers(help='sub-command help')

#upload specific arguments
parser_upload = subparsers.add_parser('upload', help='upload -h')
parser_upload.add_argument('upload', action="store_true",
                    help='Upload files as defined in the config file')
parser_upload.add_argument('-o','--overwrite', action="store_true",
                    help='All files on s3 will be overwritten even if local ones are older')

#restore specific arguments
parser_restore = subparsers.add_parser('restore', help='restore -h')
parser_restore.add_argument('restore', type=str,
                    help='Restore passed folder or file')
parser_restore.add_argument('--timestamp', type=int,
                    help='Restore file/s back to before passed timestamp if not set restore will use latest file version')
parser_restore.add_argument('-c','--clean', action="store_true",
                    help='Delete all existing file/s first')

#global argumenrs
parser.add_argument('--apikey',type=str, nargs = 1,
                    help='AWS API key will use aws configure if not passed')
parser.add_argument('--secretkey',type=str, nargs = 1,
                    help='AWS secret key will use aws configure if not passed')
parser.add_argument('--config',type=str, nargs = 1,
                    help='path to the config file')
parser.add_argument('--alllog', type=str, nargs = 1,
                    help='path to all log file')
parser.add_argument('--errorlog', type=str, nargs = 1,
                    help='path to error log file')
log_level_group = parser.add_mutually_exclusive_group()
log_level_group.add_argument("-v", "--verbose", action="store_true" , help="show verbose console output")
log_level_group.add_argument("-q", "--quiet", action="store_true" , help="show no console output")

args = parser.parse_args()

#setup logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
format_string = "[%(levelname)s] [%(name)s] [%(asctime)s] %(message)s"
if platform.system() == 'Windows':
    log_folder = os.path.join(os.getenv('APPDATA'), 'amazon-backup')
else:
    log_folder = os.path.join(os.path.expanduser("~"), ".local", "share", 'amazon-backup')


# create console handler and set level to info
if args.quiet != True:
    handler = logging.StreamHandler()
    if args.verbose:
        handler.setLevel(logging.INFO)
    else:
        handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# create error file handler and set level to error
handler = logging.FileHandler(os.path.join(log_folder, "error.log"), "w", encoding=None, delay="true")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter(format_string)
handler.setFormatter(formatter)
logger.addHandler(handler)

# create debug file handler and set level to debug
handler = logging.FileHandler(os.path.join(log_folder, "all.log"), "w")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(format_string)
handler.setFormatter(formatter)
logger.addHandler(handler)

#set boto to only log errors
logging.getLogger('botocore').setLevel(logging.ERROR)
logging.getLogger('boto3').setLevel(logging.ERROR)

#initialise config file
if args.config:
    config = Config(args.config)
else:
    config = Config()

if args.upload:
    upload(args.overwrite)