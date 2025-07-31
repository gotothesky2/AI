import boto3
import os
from fastapi import UploadFile
from botocore.exceptions import BotoCoreError,ClientError


class S3Upload:
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_s3_buket_name=os.environ.get("AWS_S3_BUKET_NAME")
    def __
    def upload_file(self, file:UploadFile, key:str)->str:
        try:
            self.s3.upload_fileobj(file, key, self.bucket,key)
            return self.
