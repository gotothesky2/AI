from fastapi import UploadFile

from repository.userRepository import UserRepository
from util.PdfExtracter.HmtExtracter import HmtExtracter
from util.Transactional import Transactional
from repository.hmtRepository import hmtRepository, HmtRepository
from repository.userRepository import userRepository,UserRepository
from domain.Hmt import Hmt
import uuid
from domain.User import User
from datetime import datetime
from DTO.HmtDTO import HmtResponse
from globals import (
    ErrorCode, 
    raise_business_exception, 
    raise_database_exception, 
    raise_file_exception,
    BusinessException,
    FileException,
    DatabaseException
)

# Mock S3 클라이언트 (개발/테스트용)
class MockS3Client:
    def upload_bytes(self, pdf_bytes: bytes, key: str) -> str:
        """Mock S3 업로드 - 실제 업로드 없이 가짜 URL 반환"""
        return f"https://mock-s3-bucket.s3.amazonaws.com/{key}"

class HmtService:
    def __init__(self,hmtRepository: HmtRepository,userRepository: UserRepository):
        self._hmtRepository= hmtRepository
        self._userRepository = userRepository
        # Mock S3 클라이언트로 초기화 (추후 실제 S3 클라이언트로 교체 가능)
        self._s3 = MockS3Client()

    #흥미검사 첨부 기능
    @Transactional
    def createHmt(self, user_id:str ,file:UploadFile):
        try:
            # 1. 사용자 검증
            user:User = self._userRepository.getById(user_id)
            if user is None:
                raise_business_exception(
                    ErrorCode.USER_NOT_FOUND, 
                    f"흥미검사 생성 - 사용자 ID '{user_id}'를 찾을 수 없습니다."
                )
            
            # 2. 파일 바이트 읽기
            file.file.seek(0)
            pdf_bytes = file.file.read()
            
            if not pdf_bytes:
                raise_file_exception(
                    ErrorCode.FILE_UPLOAD_ERROR,
                    "흥미검사 생성 - 업로드된 파일이 비어있거나 읽을 수 없습니다."
                )
            
            # 3. PDF 추출 및 점수 분석 (유틸단 에러를 서비스 컨텍스트로 전파)
            try:
                scores = HmtExtracter(pdf_bytes)
            except FileException as e:
                # 유틸단에서 올라온 파일 관련 예외를 서비스 컨텍스트로 재발생
                raise_file_exception(
                    e.error_code,
                    f"흥미검사 PDF 처리 실패 - {e.detail}"
                )
            except BusinessException as e:
                # 유틸단에서 올라온 비즈니스 예외를 서비스 컨텍스트로 재발생
                raise_business_exception(
                    e.error_code,
                    f"흥미검사 점수 분석 실패 - {e.detail}"
                )
            
            # 4. S3 업로드
            try:
                key = f"hmt/{user.uid}/{uuid.uuid4().hex}.pdf"
                pdf_url = self._s3.upload_bytes(pdf_bytes, key)
            except Exception as e:
                raise_business_exception(
                    ErrorCode.S3_UPLOAD_ERROR,
                    f"흥미검사 파일 업로드 실패 - {str(e)}"
                )
            
            # 5. 흥미검사 엔티티 생성
            try:
                newHmt = Hmt(
                    user=user,
                    hmtGradeNum=user.gradeNum,
                    pdfLink=pdf_url,
                    rScore=scores.get("R", -1),
                    iScore=scores.get("I", -1),
                    aScore=scores.get("A", -1),
                    sScore=scores.get("S", -1),
                    eScore=scores.get("E", -1),
                    cScore=scores.get("C", -1)
                )
                self._hmtRepository.save(newHmt)
            except Exception as e:
                raise_database_exception(
                    ErrorCode.DATABASE_ERROR,
                    f"흥미검사 저장 실패 - {str(e)}"
                )
            
            # 6. DTO 변환 및 반환
            try:
                return HmtResponse.model_validate(newHmt, from_attributes=True)
            except Exception as e:
                raise_business_exception(
                    ErrorCode.VALIDATION_ERROR,
                    f"흥미검사 응답 생성 실패 - {str(e)}"
                )
                
        except (BusinessException, DatabaseException, FileException):
            # 이미 정의된 커스텀 예외는 그대로 재발생 (라우트단에서 처리)
            raise
        except Exception as e:
            # 예상치 못한 모든 예외
            raise_business_exception(
                ErrorCode.UNKNOWN_ERROR,
                f"흥미검사 생성 중 예상치 못한 서비스 오류 - {str(e)}"
            )

    @Transactional
    def deleteHmt(self, hmtId: int):
        try:
            removeObj = self._hmtRepository.getById(hmtId)
            if removeObj is None:
                raise_business_exception(
                    ErrorCode.HMT_NOT_FOUND,
                    f"삭제할 흥미검사 ID '{hmtId}'를 찾을 수 없습니다."
                )
            
            self._hmtRepository.remove(removeObj)
            
        except BusinessException:
            raise
        except Exception as e:
            raise_database_exception(
                ErrorCode.DATABASE_ERROR,
                f"흥미검사 삭제 중 데이터베이스 오류: {str(e)}"
            )
    
    @Transactional
    def getHmtById(self, hmtId: int):
        try:
            getObj = self._hmtRepository.getById(hmtId)
            if getObj is None:
                raise_business_exception(
                    ErrorCode.HMT_NOT_FOUND,
                    f"조회할 흥미검사 ID '{hmtId}'를 찾을 수 없습니다."
                )
            return getObj
            
        except BusinessException:
            raise
        except Exception as e:
            raise_database_exception(
                ErrorCode.DATABASE_ERROR,
                f"흥미검사 조회 중 데이터베이스 오류: {str(e)}"
            )

    @Transactional
    def allHmtByUserId(self, user_id: str):
        try:
            user: User = self._userRepository.getById(user_id)
            if user is None:
                raise_business_exception(
                    ErrorCode.USER_NOT_FOUND,
                    f"사용자 ID '{user_id}'를 찾을 수 없습니다."
                )
            
            allHmt = user.hmts
            
            # 빈 리스트도 정상적인 결과로 처리
            return [HmtResponse.model_validate(c, from_attributes=True) for c in allHmt]
            
        except BusinessException:
            raise
        except Exception as e:
            raise_database_exception(
                ErrorCode.DATABASE_ERROR,
                f"사용자별 흥미검사 목록 조회 중 오류: {str(e)}"
            )

hmtService = HmtService(hmtRepository,userRepository)

