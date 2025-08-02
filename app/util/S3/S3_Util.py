import boto3
import os
from fastapi import UploadFile
from botocore.exceptions import BotoCoreError,ClientError
from flask.cli import load_dotenv


class S3Util:
    def __init__(self):
        load_dotenv()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID","")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY","")
        buket=os.getenv("AWS_S3_BUCKET_NAME","")
        if not aws_access_key_id or not aws_secret_access_key or not buket:
            raise Exception("S3 환경 변수가 설정 되지 않았습니다.")
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    def upload_file(self,file:UploadFile,key:str)->str:
        try:
            self.s3_client.upload_fileobj(file.file,self.bucket,key)
            return key
        except (BotoCoreError,ClientError) as e:
            raise Exception(f"S3 업로드 실패:{str(e)}")

    def get_presigned_url(self,key:str,expires_in: int =3600)->str:
        try:
            url=self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": buket, "Key": key},
                ExpiresIn=expires_in
            )
            return url
        except (BotoCoreError,ClientError) as e:
            raise Exception(f"S3 prisigned_url 생성 실패:{str(e)}")

    def delete_file(self,key:str)->bool:
        try:
            self.s3_client.delete_object(Bucket=buket, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise Exception(f"S3 파일 확인 실패:{str(e)}")

