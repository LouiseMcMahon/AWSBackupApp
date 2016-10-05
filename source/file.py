import platform
from pprint import pprint

class File(object):

    def __init__(self,path,path_parent,bucket_name,bucket_path):
        import os
        self.path = path_normalise(path)
        self.name = path_leaf(self.path)
        self.path_parent = path_normalise(path_parent)
        self.path_relative = os.path.relpath(self.path,self.path_parent)
        self.bucket_name = bucket_name
        self.s3_key = bucket_path+ self.path_relative.replace('\\', '/')

    def __str__(self):
        return self.path

    @property
    def contents(self):
        with open(self.path) as file:
            contents = file.read()
        return contents

    @property
    def timestamp_created(self):
        import os
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            return os.path.getctime(self.path)
        else:
            stat = os.stat(self.path)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime

    @property
    def timestamp_modified(self):
        import os
        modified_time = os.path.getmtime(self.path)
        if modified_time != None:
            return modified_time
        else:
            return self.timestamp_created

    def upload(self,overwrite_if_older = False):
        from aws import AWS
        from datetime import datetime
        import time
        import botocore
        import logging

        aws = AWS()
        object = aws.s3_object(self.bucket_name,self.s3_key)
        s3_last_modified = False

        try:
            s3_last_modified = object.last_modified
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                logging.info(str(self) + ": new uploading")
                object.upload_file(self.path)
        else:
            if time.mktime(s3_last_modified.timetuple()) < self.timestamp_modified and overwrite_if_older == False:
                logging.info(str(self)+ ": backup out of date uploading")
                object.upload_file(self.path)
            elif overwrite_if_older == True:
                if time.mktime(s3_last_modified.timetuple()) < self.timestamp_modified:
                    logging.info(str(self) + ": backup out of date uploading")
                else:
                    logging.info(str(self) + ": older than backup uploading anyway")
                object.upload_file(self.path)
            else:
                logging.info(str(self) + ": older than backup skipping")


def scan_folder(folder_path,recursive = True,ignore_paths = []):
    import os

    folder_path = path_normalise(folder_path)
    files_to_return = []

    if recursive:
        for current_dir, sub_dirs, sub_files in os.walk(folder_path):
            for path in ignore_paths:
                path = path_normalise(path)
                if path in current_dir:
                    break

            #if path not in ingnore the else will run
            else:
                for filename in sub_files:
                    files_to_return.append(os.path.join(current_dir, filename))

    else:
        files_in_folder = os.listdir(folder_path)
        for file in files_in_folder:
            if os.path.isfile(os.path.join(folder_path,file)):
                files_to_return.append(os.path.join(folder_path,file))

    return files_to_return


def path_normalise(path):
    """
    function to lowercase and normalise paths removing extraneous ../ etc
    :param path string: path to be normalised
    :return string: normalised path
    """
    import os
    return os.path.normcase(os.path.normpath(path))


def path_leaf(path):
    """
    function that relibly gets the a files filename
    :param path: path to file
    :return string: file name
    """
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
        
def delete_none_existing_files(bucket_name,s3_path,existsing_files):
    from aws import AWS
    import logging
    aws = AWS()
    bucket = aws.s3_bucket(bucket_name)

    all_objects = bucket.objects.all()
    for object in all_objects:
        if s3_path in object.key:
            for existsing_file in existsing_files:
                if object.key == existsing_file.s3_key:
                    logging.info(str(object.key) + ": exists on local leaving on s3")
                    break
            else:
                logging.info(str(object.key) + ": does not exist on local deleting from s3")
                object.delete()