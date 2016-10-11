#!/usr/bin/env python
from config import Config
from file import File,scan_folder,delete_none_existing_files,path_normalise,recursive_delete
from pprint import pprint
from aws import AWS
import sys
import logging
import os
import platform
import argparse

def num_to_ith(num):
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == "1":
            return str(num)+"th"
    lastDigit = num % 10
    if (lastDigit == 1):
        return str(num)+"st"
    elif (lastDigit == 2):
        return str(num)+"nd"
    elif (lastDigit == 3):
        return str(num)+"rd"
    else:
        return str(num)+"th"

def upload(overwrite,config,aws):
    from aws import AWS
    logging.info("Uploading files to S3")
    i = 0
    for folder in config.config["folders"]:
        i +=1
        aws_object = aws
        if "aws_credentials" in folder:
            if "api_key" in folder["aws_credentials"] and "secret_key" in folder["aws_credentials"]:
                aws_object = AWS(folder["aws_credentials"]["api_key"],folder["aws_credentials"]["secret_key"])

        if "path" not in folder:
            logging.error("path not set in config for "+num_to_ith(i)+" folder")
            continue

        if "bucket_name" not in folder:
            logging.error("bucket_name not set in config for "+num_to_ith(i)+" folder")
            continue

        if "bucket_path" not in folder:
            logging.error("bucket_path not set in config for "+num_to_ith(i)+" folder" )
            continue

        if "ignore" not in folder:
            folder["ignore"] = []

        files = scan_folder(folder["path"],True,folder["ignore"])
        file_objects = []
        for file_path in files:
            file = File(file_path,folder["path"],folder["bucket_name"],folder["bucket_path"])
            file.upload(aws_object,overwrite)
            file_objects.append(file)

        logging.info("Removing old files from S3")
        delete_none_existing_files(folder["bucket_name"],folder["bucket_path"],file_objects,aws_object)

    logging.info("Finished")

def restore(restore_path, timestamp, config, aws, clean = False):
    import os
    import botocore
    import time
    restore_path = path_normalise(restore_path)
    logging.info("Starting restore")
    if config.config:
        for folder_config in config.config["folders"]:
            #get config for restore path
            if "path" in folder_config:
                if path_normalise(folder_config["path"]) in restore_path:
                    logging.info("Config found")
                    #delte old files if requested
                    if clean:
                        logging.info("Cleaning away old files")
                        if "ignore" in folder_config:
                            if len(folder_config["ignore"]) > 0:
                                logging.error("Cannot do clean while there are ignored folders, clean manually first")
                                return
                        if os.path.isfile(restore_path):
                            os.unlink(restore_path)
                        elif os.path.isdir(restore_path):
                            recursive_delete(restore_path+os.path.sep)

                    if "bucket_name" in folder_config:
                        aws_object = aws
                        if "aws_credentials" in folder_config:
                            if "api_key" in folder_config["aws_credentials"] and "secret_key" in folder_config["aws_credentials"]:
                                aws_object = AWS(folder_config["aws_credentials"]["api_key"],
                                                 folder_config["aws_credentials"]["secret_key"])
                        try:
                            prefix = folder_config["bucket_path"]+restore_path.replace(path_normalise(folder_config["path"]),'').strip(os.path.sep)
                            bucket = aws_object.s3_bucket(folder_config["bucket_name"])

                            if timestamp and timestamp > 0:
                                objects = {}
                                for object in bucket.object_versions.filter(Prefix=prefix):
                                    if object.object_key not in objects:
                                        objects[object.object_key] = []
                                    objects[object.object_key].append(object)

                                for list in objects:
                                    objects[list] = sorted(objects[list], key=lambda object: object.last_modified, reverse=True)
                                    for object in objects[list]:
                                        if time.mktime(object.last_modified.timetuple()) < timestamp:
                                            if object.size != None:
                                                path = object.key.replace(folder_config["bucket_path"], '')
                                                path = os.path.join(restore_path, path.replace('/', os.path.sep))
                                                file = File(path,
                                                            folder_config["path"],
                                                            folder_config["bucket_name"],
                                                            folder_config["bucket_path"])
                                                logging.info("Restoring " + path + " to " + object.last_modified.strftime("%I:%M%p on %B %d, %Y"))
                                                file.restore(aws_object,object.version_id)
                                            break
                            else:

                                objects = bucket.objects.filter(Prefix=prefix)
                                for object in objects:
                                    path = object.key.replace(folder_config["bucket_path"],'')
                                    path = os.path.join(restore_path,path.replace('/',os.path.sep))
                                    logging.info("Restoring " + path)
                                    file = File(path,folder_config["path"],folder_config["bucket_name"],folder_config["bucket_path"])
                                    file.restore(aws_object)

                        except botocore.exceptions.ClientError as e:
                            logging.error(": AWS Error " + e.response['Error']['Message'])

                    else:
                        logging.error("bucket_name not found in config file")

                    #return when complete or the not found in config file error will be passed
                    logging.info("Finished")
                    return

            else:
                continue
        else:
            logging.error(restore_path + " not found in config file")

def logger():
    # setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    format_string = "[%(levelname)s] [%(name)s] [%(asctime)s] %(message)s"
    if platform.system() == "Windows":
        log_folder = os.path.join(os.getenv("APPDATA"), "amazon-backup")
    else:
        log_folder = os.path.join(os.path.expanduser("~"), ".local", "share", "amazon-backup")

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
    if args.errorlog:
        error_log_path = args.errorlog
    else:
        error_log_path = os.path.join(log_folder, "error.log")
    handler = logging.FileHandler(error_log_path, "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    if args.alllog:
        all_log_path = args.alllog
    else:
        all_log_path = os.path.join(log_folder, "all.log")
    handler = logging.FileHandler(all_log_path, "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # set boto to only log errors
    logging.getLogger("botocore").setLevel(logging.ERROR)
    logging.getLogger("boto3").setLevel(logging.ERROR)

def parser():
    #setup argument parsing
    parser = argparse.ArgumentParser(description="S3 backup utility")
    subparsers = parser.add_subparsers(help="sub-command help")

    #upload specific arguments
    parser_upload = subparsers.add_parser("upload", help="upload -h")
    parser_upload.add_argument("upload", action="store_true",
                        help="Upload files as defined in the config file")
    parser_upload.add_argument("-o","--overwrite", action="store_true",
                        help="All files on s3 will be overwritten even if local ones are older")

    #restore specific arguments
    parser_restore = subparsers.add_parser("restore", help="restore -h")
    parser_restore.add_argument("restore", type=str,
                        help="Restore passed folder or file")
    parser_restore.add_argument("--timestamp", type=int,
                        help="Restore file/s back to before passed timestamp if not set restore will use latest file version")
    parser_restore.add_argument("-c","--clean", action="store_true",
                        help="Delete all existing file/s first")

    #restore specific arguments
    parser_config = subparsers.add_parser("config", help="config -h")
    parser_config.add_argument("config", action="store_true",
                        help="Configure what folders are to be backed up and to where")

    #global argumenrs
    parser.add_argument("--apikey",type=str, nargs = 1,
                        help="AWS API key will use aws configure if not passed and settings in your confg file will overwrite")
    parser.add_argument("--secretkey",type=str, nargs = 1,
                        help="AWS secret key will use aws configure if not passed and settings in your confg file will overwrite")
    parser.add_argument("--config",type=str, nargs = 1,
                        help="path to the config file")
    parser.add_argument("--alllog", type=str, nargs = 1,
                        help="path to all log file")
    parser.add_argument("--errorlog", type=str, nargs = 1,
                        help="path to error log file")
    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument("-v", "--verbose", action="store_true" , help="show verbose console output")
    log_level_group.add_argument("-q", "--quiet", action="store_true" , help="show no console output")

    return parser.parse_args()

#initialise parser
args = parser()

#initialise logger
logger()

#initialise config file
if args.config:
    config = Config(args.config)
else:
    config = Config()

#initialise aws
aws = AWS()
if args.apikey and args.secretkey:
    aws = AWS(args.apikey,args.secretkey)

# run commands
if hasattr(args, 'upload'):
    upload(args.overwrite,config,aws)
elif hasattr(args, 'restore'):
    timestamp = False
    if "timestamp" in args:
        timestamp = args.timestamp

    restore(args.restore,timestamp,config,aws,args.clean)