import platform
from pprint import pprint

class File(object):

    def __init__(self,file_path):
        self.path = File.normalise_path(file_path)
        self.name = File.path_leaf(self.path)

    def __str__(self):
        return self.path

    @property
    def contents(self):
        with file(self.path) as file:
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

    @staticmethod
    def scan_folder(folder_path,recursive = True,ignore_paths = []):
        import os

        folder_path = File.normalise_path(folder_path)
        files_to_return = []

        if recursive:
            for current_dir, sub_dirs, sub_files in os.walk(folder_path):
                for path in ignore_paths:
                    path = File.normalise_path(path)
                    if path in current_dir:
                        break

                #if path not in ingnore the else will run
                else:
                    for filename in sub_files:
                        files_to_return.append(File(os.path.join(current_dir, filename)))

        else:
            files_in_folder = os.listdir(folder_path)
            for file in files_in_folder:
                if os.path.isfile(os.path.join(folder_path,file)):
                    files_to_return.append(File(os.path.join(folder_path,file)))

        return files_to_return

    @staticmethod
    def normalise_path(path):
        """
        function to lowercase and normalise paths removing extraneous ../ etc
        :param path string: path to be normalised
        :return string: normalised path
        """
        import os
        return os.path.normcase(os.path.normpath(path))

    @staticmethod
    def path_leaf(path):
        """
        function that relibly gets the a files filename
        :param path: path to file
        :return string: file name
        """
        import ntpath
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)
        
