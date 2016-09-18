import boto

class aws():
    def __init__(self,apiKey,apiId):
        self.apiKey = apiKey
        self.apiId = apiId

    def connectToAws(self):
        conn =  boto.connect_s3(self.apiKey,self.apiId)
        print conn

