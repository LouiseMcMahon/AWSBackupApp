import json
import os
import errno


class Config(object):

    '''
    self.config contains the whole config file as a json array and will update the config file if changed
    self.config_file_path contains the path to the config file
    '''

    def __init__(self, file_path = None):
        import platform
        self.__config_cache = None

        if file_path:
            self.file_path = file_path
        else:
            if platform.system() == 'Windows':
                self.file_path = os.path.join(os.getenv('APPDATA'), 'amazon-backup', 'confg.json')
            else:
                self.file_path = os.path.join(os.path.expanduser("~") , ".local" , "share" , 'amazon-backup', 'confg.json')

    @property
    def config(self):
        #if cache return
        if self.__config_cache != None:
            return self.__config_cache

        #if not cached and file exists get it and set cache
        elif os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                self.__config_cache = json.load(data_file)
            return self.__config_cache
        #if file does not exist create it
        else:
            try:
                os.makedirs(os.path.dirname(self.file_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            with open(self.file_path, 'w') as outfile:
                json.dump([], outfile)
                self.__config_cache = []
                return self.__config_cache

    @config.setter
    def config(self,config):
        #set cache
        self.__config_cache = config

        #update file
        with open(self.file_path, 'w') as config_file:
            config_file.truncate(0)
            json.dump(config, config_file)