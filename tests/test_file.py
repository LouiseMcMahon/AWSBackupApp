from unittest import TestCase
from source.file import File
from pprint import pprint

class TestFile(TestCase):
    def test_init(self):
        import os
        read_file_loc = File.path_normalise(os.path.join(os.getcwd(), "test_files", "init_config_1_test.json"))
        file = File(read_file_loc, os.path.join(os.getcwd(), 'test_files'), 'test-bucket', 'test/path/')

        self.assertEqual(file.path,read_file_loc,"path atribute not set correctly")
        self.assertEqual(file.name, "init_config_1_test.json", "name atribute not set correctly")
        print file.path_parent
        self.assertEqual(file.path_parent, File.path_normalise(os.path.join(os.getcwd(), 'test_files')), "path_parent atribute not set correctly")
        self.assertEqual(file.path_relative, "init_config_1_test.json", "path_relative atribute not set correctly")
        self.assertEqual(file.bucket_name, "test-bucket", "bucket_name atribute not set correctly")
        self.assertEqual(file.s3_key, "test/path/init_config_1_test.json", "s3_key atribute not set correctly")

    def test_str(self):
        import os
        read_file_loc = os.path.join(os.getcwd(), "test_files", "init_config_1_test.json")
        file = File(read_file_loc,os.path.join(os.getcwd(),'test_files'),'test-bucket','')

        self.assertEqual(str(file),
                         File.path_normalise(read_file_loc),
                         'string method not passing path correctly')

    def test_contents(self):
        import os
        read_file_loc = File.path_normalise(os.path.join(os.getcwd(), "test_files", "init_config_1_test.json"))
        file = File(read_file_loc, os.path.join(os.getcwd(), 'test_files'), 'test-bucket', 'test/path/')

        self.assertEqual(file.contents, "[\"this is a test file\"]", "contents not correct")

    def test_timestamp_created(self):
        self.fail()

    def test_timestamp_modified(self):
        import os

        read_file_loc = File.path_normalise(os.path.join(os.getcwd(), "test_files", "init_config_1_test.json"))
        file = File(read_file_loc, os.path.join(os.getcwd(), 'test_files'), 'test-bucket', 'test/path/')
        os.utime(read_file_loc, (1475664168, 1475664168))

        self.assertEqual(file.timestamp_modified,1475664168,"modified time not correct")

    def test_upload(self):
        self.fail()

    def test_scan_folder(self):
        import os
        test_files_path = os.path.join(os.getcwd(), "test_files")
        expected_recursive_no_ignore = [
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'init_config_1_test.json')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'test.csv')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'test.php')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'dont_ignore', 'test.txt')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'ignore', 'test.json'))
        ]

        expected_no_recursive = [
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'init_config_1_test.json')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'test.csv')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'test.php'))
        ]

        expected_recursive_ignore = [
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'init_config_1_test.json')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'test.csv')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'test.php')),
            File.path_normalise(os.path.join(os.getcwd(), 'test_files', 'dont_ignore', 'test.txt'))
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

    def test_path_normalise(self):
        import os
        self.assertEqual(File.path_normalise(os.getcwd()), os.path.normcase(os.path.normpath(os.getcwd())), "path not normalised")

    def test_path_leaf(self):
        import os
        read_file_loc = os.path.join(os.getcwd(), "test_files", "init_config_1_test.json")
        file_name = File.path_leaf(read_file_loc)
        self.assertEqual(file_name,"init_config_1_test.json","file name not extracted correctly")
