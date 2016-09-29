import json
import os

class configFile():

    def __init__(self):
        configFilePath = os.path.join(os.getenv('APPDATA'),'amazon-backup','confg.json')
        print configFilePath
        if os.path.isfile(configFilePath):
            with open(configFilePath) as data_file:
                self.config = json.load(data_file)
        else:
            os.makedirs(os.path.join(os.getenv('APPDATA'),'amazon-backup'))
            with open(configFilePath, 'w') as outfile:
                json.dump([], outfile)
                self.config = []

