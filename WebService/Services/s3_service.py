import boto3

class S3Service:
    def __init__(self):
        self.session = boto3.Session(profile_name='capstone')
        self.s3 = self.session.client('s3')

    def download_file(self, key, bucket, filename):
        return self.s3.download_file(Bucket=bucket, Key=key, Filename=filename)
