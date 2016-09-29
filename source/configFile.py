import json
import os


class ConfigFile():

    '''
    self.config contains the whole config file as a json array
    self.config_file_path contains the path to the config file
    '''

    def __init__(self):
        self.config_file_path = os.path.join(os.getenv('APPDATA'), 'amazon-backup', 'confg.json')
        if os.path.isfile(self.config_file_path):
            with open(self.config_file_path) as data_file:
                self.config = json.load(data_file)
        else:
            os.makedirs(os.path.join(os.getenv('APPDATA'),'amazon-backup'))
            with open(self.config_file_path, 'w') as outfile:
                json.dump([], outfile)
                self.config = []

    #when called overwrites what ever is at self.config_file_path with self.config
    def update_config_file(self):
        with open(self.config_file_path, 'w') as config_file:
            config_file.truncate(0)
            json.dump(self.config, config_file)