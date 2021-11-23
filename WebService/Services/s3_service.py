import boto3
import logging
from botocore.exceptions import ClientError

class S3Service:
    def __init__(self):
        self.session = boto3.Session(profile_name='capstone')
        self.s3 = self.session.client('s3')

    def download_file(self, key, bucket, filename):
        return self.s3.download_file(Bucket=bucket, Key=key, Filename=filename)

    def upload_file(self, bucket, filepath, key):
        try:
            response = self.s3.upload_file(filepath, bucket, key)
        except ClientError as e:
            logging.error(e)
            return False
        return True

