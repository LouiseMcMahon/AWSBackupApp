from unittest import TestCase
from source.file import File
from pprint import pprint

class TestFile(TestCase):
    def test_init(self):
        import os
        read_file_loc = File.normalise_path(os.path.join(os.getcwd(), "test_files", "init_config_1_test.json"))
        file = File(read_file_loc, os.path.join(os.getcwd(), 'test_files'), 'test-bucket', 'test/path/')

        self.assertEqual(file.path,read_file_loc,"path atribute not set correctly")
        self.assertEqual(file.name, "init_config_1_test.json", "name atribute not set correctly")
        self.assertEqual(file.path_parent, os.path.join(os.getcwd(), 'test_files'), "path_parent atribute not set correctly")
        self.assertEqual(file.path_relative, "init_config_1_test.json", "path_relative atribute not set correctly")
        self.assertEqual(file.bucket_name, "test-bucket", "bucket_name atribute not set correctly")
        self.assertEqual(file.s3_key, "test/path/init_config_1_test.json", "s3_key atribute not set correctly")

    def test_str(self):
        import os
        read_file_loc = os.path.join(os.getcwd(), "test_files", "init_config_1_test.json")
        file = File(read_file_loc,os.path.join(os.getcwd(),'test_files'),'test-bucket','')

        self.assertEqual(str(file),
                         File.normalise_path(read_file_loc),
                         'string method not passing path correctly')

    def test_contents(self):
        self.fail()

    def test_timestamp_created(self):
        self.fail()

    def test_timestamp_modified(self):
        self.fail()

    def test_upload(self):
        self.fail()

    def test_scan_folder(self):
        import os
        test_files_path = os.path.join(os.getcwd(), "test_files")
        expected_recursive_no_ignore = [
            File.normalise_path(os.path.join(os.getcwd(),'test_files','init_config_1_test.json')),
            File.normalise_path(os.path.join(os.getcwd(),'test_files','test.csv')),
            File.normalise_path(os.path.join(os.getcwd(),'test_files','test.php')),
            File.normalise_path(os.path.join(os.getcwd(),'test_files','dont_ignore','test.txt')),
            File.normalise_path(os.path.join(os.getcwd(),'test_files','ignore','test.json'))
        ]

        expected_no_recursive = [
            File.normalise_path(os.path.join(os.getcwd(), 'test_files', 'init_config_1_test.json')),
            File.normalise_path(os.path.join(os.getcwd(), 'test_files', 'test.csv')),
            File.normalise_path(os.path.join(os.getcwd(), 'test_files', 'test.php'))
        ]

        expected_recursive_ignore = [
            File.normalise_path(os.path.join(os.getcwd(), 'test_files', 'init_config_1_test.json')),
            File.normalise_path(os.path.join(os.getcwd(), 'test_files', 'test.csv')),
            File.normalise_path(os.path.join(os.getcwd(), 'test_files', 'test.php')),
            File.normalise_path(os.path.join(os.getcwd(), 'test_files', 'dont_ignore', 'test.txt'))
        ]

        self.assertItemsEqual(File.scan_folder(test_files_path),
                         expected_recursive_no_ignore,
                         "recursive with no ignored folders failed")

        self.assertItemsEqual(File.scan_folder(test_files_path,False),
                         expected_no_recursive,
                         "none recursive failed")

        self.assertItemsEqual(File.scan_folder(test_files_path,True,[os.path.join(test_files_path,'ignore')]),
                         expected_recursive_ignore,
                         "recursive with ignored folders failed")

    def test_normalise_path(self):
        import os
        self.assertEqual(File.normalise_path(os.getcwd()),os.path.normcase(os.path.normpath(os.getcwd())),"path not normalised")

    def test_path_leaf(self):
        import os
        read_file_loc = os.path.join(os.getcwd(), "test_files", "init_config_1_test.json")
        file_name = File.path_leaf(read_file_loc)
        self.assertEqual(file_name,"init_config_1_test.json","file name not extracted correctly")
