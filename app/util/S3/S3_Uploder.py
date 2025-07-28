import boto3
import os
from typing import Optional, Dict
from datetime import datetime
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from dataclasses import dataclass
from fastapi import UploadFile

logger = logging.getLogger(__name__)

@dataclass
class PdfUploadConfig:
    """PDF 업로드 설정 클래스"""
    public_read: bool = False  # 공개 읽기 권한 여부
    cache_control: str = "max-age=3600"  # 캐시 제어 (기본값: 1시간)
    metadata: Dict[str, str] = None  # 추가 메타데이터
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class S3Uploader:
    """AWS S3에 파일을 업로드하는 간단한 클래스 (PDF 추출기 스타일)"""
    
    def __new__(cls, file_source, user_id: str, upload_type: str = 'auto', pdf_upload_config=None):
        """
        PDF 추출기 스타일로 바로 업로드 처리하고 결과 반환
        
        Args:
            file_source: 업로드할 파일 (경로, bytes, UploadFile 등)
            user_id: 사용자 ID
            upload_type: 업로드 타입 ('auto', 'pdf', 'report', 'file')
            pdf_upload_config: PDF 업로드 설정 (선택사항)
        
        Returns:
            업로드 성공 시 S3 URL, 실패 시 None
        """
        uploader = cls._create_uploader(pdf_upload_config)
        return cls._process_upload(uploader, file_source, user_id, upload_type)
    
    @classmethod
    def _create_uploader(cls, pdf_upload_config=None):
        """S3 업로더 인스턴스 생성"""
        instance = super(S3Uploader, cls).__new__(cls)
        instance._initialize(pdf_upload_config)
        return instance
    
    def _initialize(self, pdf_upload_config=None):
        """업로더 초기화"""
        # PDF 업로드 설정
        self.pdf_upload_config = pdf_upload_config
            
        # 환경변수에서 AWS 설정 읽기
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.getenv('AWS_REGION', 'ap-northeast-2')
        
        if not all([self.bucket_name, self.aws_access_key_id, self.aws_secret_access_key]):
            logger.warning("S3 설정이 완전하지 않습니다. 일부 기능이 제한될 수 있습니다.")
            self.s3_client = None
        else:
            # S3 클라이언트 초기화
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
    
    @classmethod
    def _process_upload(cls, uploader, file_source, user_id: str, upload_type: str):
        """업로드 처리 로직"""
        try:
            if upload_type == 'auto':
                # 자동 타입 감지
                upload_type = cls._detect_type(file_source)
            
            if upload_type == 'pdf':
                return uploader._upload_pdf_internal(file_source, user_id)
            elif upload_type == 'report':
                return uploader._upload_report_internal(file_source, user_id)
            else:
                return uploader._upload_file_internal(file_source, user_id, upload_type)
                
        except Exception as e:
            logger.error(f"업로드 처리 중 오류 발생: {e}")
            return None
    
    @staticmethod
    def _detect_type(file_source):
        """파일 타입 자동 감지"""
        if isinstance(file_source, UploadFile):
            if file_source.filename and file_source.filename.lower().endswith('.pdf'):
                return 'pdf'
        elif isinstance(file_source, str):
            if file_source.lower().endswith('.pdf'):
                return 'pdf'
            elif file_source.lower().endswith(('.txt', '.md')):
                return 'report'
        return 'file'
    
    def _upload_pdf_internal(self, pdf_source, user_id: str):
        """PDF 파일 업로드 내부 처리"""
        if not self.s3_client:
            logger.error("S3 클라이언트가 초기화되지 않았습니다.")
            return None
        
        try:
            # 파일을 바이트로 변환
            pdf_bytes = self._load_bytes(pdf_source)
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pdf_{user_id}_{timestamp}.pdf"
            
            # PDF 업로드 설정
            extra_args = {'ContentType': 'application/pdf'}
            if self.pdf_upload_config:
                if hasattr(self.pdf_upload_config, 'public_read') and self.pdf_upload_config.public_read:
                    extra_args['ACL'] = 'public-read'
                if hasattr(self.pdf_upload_config, 'cache_control'):
                    extra_args['CacheControl'] = self.pdf_upload_config.cache_control
                if hasattr(self.pdf_upload_config, 'metadata') and self.pdf_upload_config.metadata:
                    extra_args['Metadata'] = self.pdf_upload_config.metadata
            
            # S3에 업로드
            object_name = f"pdfs/{filename}"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=pdf_bytes,
                **extra_args
            )
            
            # S3 URL 생성
            s3_url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{object_name}"
            logger.info(f"PDF 업로드 성공: {s3_url}")
            return s3_url
            
        except Exception as e:
            logger.error(f"PDF 업로드 중 오류 발생: {e}")
            return None
    
    def _upload_report_internal(self, report_source, user_id: str):
        """보고서 업로드 내부 처리"""
        if not self.s3_client:
            logger.error("S3 클라이언트가 초기화되지 않았습니다.")
            return None
        
        try:
            # 내용을 문자열로 변환
            if isinstance(report_source, str) and not report_source.endswith(('.txt', '.md')):
                # 문자열 내용 그대로 사용
                content = report_source
            else:
                # 파일에서 읽기
                content_bytes = self._load_bytes(report_source)
                content = content_bytes.decode('utf-8')
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{user_id}_{timestamp}.txt"
            
            # S3에 업로드
            object_name = f"reports/{filename}"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=content.encode('utf-8'),
                ContentType='text/plain; charset=utf-8'
            )
            
            # S3 URL 생성
            s3_url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{object_name}"
            logger.info(f"보고서 업로드 성공: {s3_url}")
            return s3_url
            
        except Exception as e:
            logger.error(f"보고서 업로드 중 오류 발생: {e}")
            return None
    
    def _upload_file_internal(self, file_source, user_id: str, file_type: str):
        """일반 파일 업로드 내부 처리"""
        if not self.s3_client:
            logger.error("S3 클라이언트가 초기화되지 않았습니다.")
            return None
        
        try:
            # 파일을 바이트로 변환
            file_bytes = self._load_bytes(file_source)
            
            # 파일 확장자 추출
            if isinstance(file_source, UploadFile):
                extension = file_source.filename.split('.')[-1] if file_source.filename and '.' in file_source.filename else 'bin'
            elif isinstance(file_source, str):
                extension = file_source.split('.')[-1] if '.' in file_source else 'bin'
            else:
                extension = 'bin'
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{file_type}_{user_id}_{timestamp}.{extension}"
            
            # S3에 업로드
            object_name = f"files/{filename}"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_bytes
            )
            
            # S3 URL 생성
            s3_url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{object_name}"
            logger.info(f"파일 업로드 성공: {s3_url}")
            return s3_url
            
        except Exception as e:
            logger.error(f"파일 업로드 중 오류 발생: {e}")
            return None
    
    @staticmethod
    def _load_bytes(data):
        """파일 소스를 바이트로 변환 (CstExtracter 스타일)"""
        if isinstance(data, UploadFile):
            data.file.seek(0)
            return data.file.read()
        if isinstance(data, (bytes, bytearray)):
            return data
        if isinstance(data, str):
            # 파일 경로인 경우
            with open(data, 'rb') as f:
                return f.read()
        if hasattr(data, 'read'):  # 파일 객체
            return data.read()
        
        raise ValueError("지원하지 않는 파일 소스 타입")


# 간단한 사용을 위한 헬퍼 함수들
def upload_pdf(pdf_source, user_id: str, pdf_config=None) -> Optional[str]:
    """PDF 파일을 S3에 간단하게 업로드"""
    return S3Uploader(pdf_source, user_id, 'pdf', pdf_config)

def upload_pdf_validated(pdf_source, user_id: str, pdf_config=None) -> Optional[str]:
    """이미 검증된 PDF 파일을 S3에 바로 업로드 (유효성 검사 스킵)"""
    uploader = S3Uploader._create_uploader(pdf_config)
    return uploader._upload_pdf_internal(pdf_source, user_id)

def upload_report(report_content: str, user_id: str, pdf_config=None) -> Optional[str]:
    """보고서를 S3에 간단하게 업로드"""
    return S3Uploader(report_content, user_id, 'report', pdf_config)

def upload_file(file_source, user_id: str, pdf_config=None) -> Optional[str]:
    """일반 파일을 S3에 간단하게 업로드"""
    return S3Uploader(file_source, user_id, 'auto', pdf_config)
