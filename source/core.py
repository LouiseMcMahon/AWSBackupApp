#!/usr/bin/env python
from config import Config
from file import File,scan_folder
from pprint import pprint
from aws import AWS
import sys
import logging
import os

def main():
    config = Config()

    #setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    format_string = "[%(levelname)s] [%(name)s] [%(asctime)s] %(message)s"

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(os.getenv('APPDATA'), 'amazon-backup', "error.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(os.getenv('APPDATA'), 'amazon-backup', "all.log"), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #set boto to only log errors
    logging.getLogger('botocore').setLevel(logging.ERROR)
    logging.getLogger('boto3').setLevel(logging.ERROR)

    logging.info('Started')

    for folder in config.config['folders']:
        aws = AWS()

        files = scan_folder(folder["path"],True,folder["ignore"])
        for file_path in files:
            file = File(file_path,folder["path"],folder["bucket_name"],folder['bucket_path'])
            file.upload()

    logging.info('Finished')

if __name__ == '__main__':
    sys.exit(main())