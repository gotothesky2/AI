import fitz
from fastapi import UploadFile
from pathlib import Path
from util.exceptions import ErrorCode, raise_business_exception, raise_file_exception

class HmtExtracter:
    REQUIRED_KEYWORD="직업흥미검사(H) 주요 결과"
    MIN_PAGE=1
    start_teg = "<참조> 흥미 유형 육각형 모양 해석"
    teg = ["R", "I", "A", "S", "E", "C"]
    def __new__(cls, pdf_sorce):
        pdf_bytes = cls._load_bytes(pdf_sorce)
        cls._validate_content(pdf_bytes)
        return cls._extract_scores(pdf_bytes)
    #파일 유효성 검사 및 파일 형식 일관화
    @staticmethod
    def _load_bytes(data):
        try:
            if isinstance(data,UploadFile):
                data.file.seek(0)
                return data.file.read()
            if isinstance(data, (bytes, bytearray)):
                return data
            if isinstance(data, str):
                with open(data, 'rb') as f:
                    return f.read()
            if isinstance(data, (str, Path)):
                path_str = str(data)
                with open(path_str, 'rb') as f:
                    return f.read()
            
            # 커스텀 예외로 변경
            raise_file_exception(
                ErrorCode.FILE_TYPE_NOT_SUPPORTED,
                f"지원하지 않는 PDF 소스 타입: {type(data)}"
            )
        except Exception as e:
            if hasattr(e, 'error_code'):  # 이미 커스텀 예외인 경우
                raise
            raise_file_exception(
                ErrorCode.FILE_UPLOAD_ERROR,
                f"파일 읽기 중 오류: {str(e)}"
            )
    
    #페이지수 및 검사pdf맞는지 검사
    @classmethod
    def _validate_content(cls,pdf_bytes: bytes)->None:
        try:
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                # 페이지 수 검증
                if doc.page_count < cls.MIN_PAGE:
                    raise_file_exception(
                        ErrorCode.PDF_PROCESSING_ERROR,
                        f"PDF 페이지 수({doc.page_count})가 요구치({cls.MIN_PAGE})보다 적습니다."
                    )
                
                #pdf 내용물 제목 검사
                txt="".join(page.get_text()for page in doc)
                if cls.REQUIRED_KEYWORD not in txt:
                    # 직업적성검사 PDF인지 확인
                    if "직업적성검사 주요 결과" in txt:
                        raise_file_exception(
                            ErrorCode.PDF_PROCESSING_ERROR,
                            f"직업적성검사 PDF입니다. 흥미검사 API가 아닌 직업적성검사 API를 사용해주세요."
                        )
                    else:
                        raise_file_exception(
                            ErrorCode.PDF_PROCESSING_ERROR,
                            f"흥미검사 PDF가 아닙니다. 필수 키워드 '{cls.REQUIRED_KEYWORD}'를 찾을 수 없습니다."
                        )
        except Exception as e:
            if hasattr(e, 'error_code'):  # 이미 커스텀 예외인 경우
                raise
            raise_file_exception(
                ErrorCode.PDF_PROCESSING_ERROR,
                f"PDF 유효성 검증 중 오류: {str(e)}"
            )
    
    #점수 추출 로직
    @classmethod
    def _extract_scores(cls,pdf_bytes: bytes)->dict:
        try:
            result = {}
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                i = 0
                for page in doc:
                    text = page.get_text()
                    lines = text.strip().split('\n')
                    start_extract = False
                    for line in lines:
                        line = line.strip()
                        if cls.start_teg in line:
                            start_extract = True
                            continue
                        if start_extract:
                            try:
                                val = float(line)
                                result[cls.teg[i]] = val
                                i += 1
                                if len(result) == len(cls.teg):
                                    break
                            except ValueError:
                                continue
                    if len(result) == len(cls.teg):
                        break
                
                if len(result)!=len(cls.teg):
                    raise_business_exception(
                        ErrorCode.HMT_PROCESSING_ERROR,
                        f"흥미검사 점수 추출 실패. 추출된 점수: {len(result)}/{len(cls.teg)}개"
                    )
            return result
        except Exception as e:
            if hasattr(e, 'error_code'):  # 이미 커스텀 예외인 경우
                raise
            raise_business_exception(
                ErrorCode.HMT_PROCESSING_ERROR,
                f"점수 추출 중 예상치 못한 오류: {str(e)}"
            )


