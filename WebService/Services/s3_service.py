import boto3
import logging

import botocore
from botocore.config import Config
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

    def generate_url(self, bucket, key, expiration=360):
        try:
            response = self.s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=3600)
        except ClientError as e:
            logging.error(e)
            return None
        return response

