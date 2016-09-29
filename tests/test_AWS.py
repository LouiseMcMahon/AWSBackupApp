from unittest import TestCase
from source.aws import AWS
from botocore.client import BaseClient

class TestAWS(TestCase):
    def test_s3_client(self):
        aws = AWS()
        s3_client = aws.s3_client
        self.assertIsInstance(s3_client,
                              BaseClient,
                              "S3 client not being set correctly")

    def test_createBucket(self):
        self.fail()

    def test_addBucketFolder(self):
        self.fail()
