import boto3

class aws():
    def __init__(self,apiKey = None,secretKey = None):
        self.apiKey = apiKey
        self.secretKey = secretKey

    def getS3Client(self):

        if self.apiKey and self.secretKey:
            client =  boto3.client(
                's3',
                aws_access_key_id=self.apiKey,
                aws_secret_access_key=self.secretKey
            )
        else:
            client = boto3.client(
                's3'
            )

        return client

    def createBucket(self,bucketName):
        pass

    def addBucketFolder(self,folderName,lifecycle = None):
        pass

