import boto3

class AWS(object):
    def __init__(self, api_key = None, secret_key = None):
        self.api_key = api_key
        self.secret_key = secret_key

    @property
    def s3_client(self):

        if self.api_key and self.secret_key:
            client =  boto3.client(
                's3',
                aws_access_key_id=self.api_key,
                aws_secret_access_key=self.secret_key
            )
        else:
            client = boto3.client(
                's3'
            )

        return client

    def s3_object(self,bucket_name,key):
        if self.api_key and self.secret_key:
            s3 =  boto3.resource(
                's3',
                aws_access_key_id=self.api_key,
                aws_secret_access_key=self.secret_key
            )
        else:
            s3 = boto3.resource('s3')

        return s3.Object(bucket_name, key)

    def createBucket(self,bucket_name):
        pass

    def addBucketFolder(self,folder_name,lifecycle = None):
        pass

