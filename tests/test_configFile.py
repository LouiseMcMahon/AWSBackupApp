from unittest import TestCase
from source.configFile import ConfigFile
import os
import json
from pprint import pprint

class TestConfigFile(TestCase):

    def setUp(self):
        self.files_to_remove = []

    def tearDown(self):
        if len(self.files_to_remove) > 0:
            for file in self.files_to_remove:
                os.remove(file)

    def test___init__(self):
        read_file_loc = os.path.join(os.getcwd(), "init_config_1_test.json")
        create_file_loc = os.path.join(os.getcwd(),"init_config_2_test.json")
        self.files_to_remove.append(create_file_loc)

        #create a config file from scratch
        config_file = ConfigFile(create_file_loc)
        self.assertEqual(config_file.config_file_path,
                         create_file_loc,
                         "config file location not set correctly when input as a variable")

        config_file.config
        self.assertTrue (os.path.isfile(config_file.config_file_path),
                         "config file not created")

        config_file = ConfigFile()
        self.assertEqual(config_file.config_file_path,
                         os.path.join(os.getenv('APPDATA'), 'amazon-backup', 'confg.json'),
                         "config file location not set correctly left blank")

        config_file = ConfigFile(read_file_loc)
        self.assertEqual(config_file.config,
                         ["this is a test file"],
                         "config not retrived corectly")

    def test_update_config_file(self):
        create_file_loc = os.path.join(os.getcwd(), "init_config_2_test.json")
        self.files_to_remove.append(create_file_loc)

        config_file = ConfigFile(create_file_loc)
        config_file.config = ["updated test file"]

        with open(create_file_loc) as data_file:
            config_file_contents = json.load(data_file)

        self.assertEqual(config_file_contents,
                         ["updated test file"],
                         "config not not writen to file")

