import fitz
from fastapi import UploadFile
from pathlib import Path
from app.util.exceptions import ErrorCode, raise_business_exception, raise_file_exception


class CstExtracter:
    REQUIRED_KEYWORD = "직업적성검사 주요 결과"
    MIN_PAGE = 1
    teg_name = [
        "수리·논리력", "예술시각능력", "손재능", "공간지각력", "음악능력",
        "대인관계능력", "창의력", "언어능력", "신체·운동능력", "자연친화력", "자기성찰능력"
    ]
    
    def __new__(cls, pdf_sorce):
        pdf_bytes = cls._load_bytes(pdf_sorce)
        cls._validate_content(pdf_bytes)
        return cls._extract_scores(pdf_bytes)
    
    #파일 유효성 검사 및 파일 형식 일관화
    @staticmethod
    def _load_bytes(data):
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
        raise_file_exception(ErrorCode.FILE_TYPE_NOT_SUPPORTED, "지원하지 않는 PDF 소스 타입")
    
    #페이지수 및 검사pdf맞는지 검사
    @classmethod
    def _validate_content(cls,pdf_bytes: bytes)->None:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            # 페이지 수 검증
            if doc.page_count < cls.MIN_PAGE:
                raise_file_exception(ErrorCode.PDF_PROCESSING_ERROR, f"PDF 페이지 수({doc.page_count})가 요구치({cls.MIN_PAGE})보다 적습니다.")
            #pdf 내용물 제목 검사
            txt="".join(page.get_text()for page in doc)
            if cls.REQUIRED_KEYWORD not in txt:
                # 흥미검사 PDF인지 확인
                if "직업흥미검사(H) 주요 결과" in txt:
                    raise_file_exception(ErrorCode.PDF_PROCESSING_ERROR, f"흥미검사 PDF입니다. 직업적성검사 API가 아닌 흥미검사 API를 사용해주세요.")
                else:
                    raise_file_exception(ErrorCode.PDF_PROCESSING_ERROR, f"직업 적성 검사 결과 PDF가 아닙니다.")
    
    #점수 추출 로직
    @classmethod
    def _extract_scores(cls,pdf_bytes: bytes)->dict:
        result = {}
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text = page.get_text()
                lines = text.strip().split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line in cls.teg_name:
                        if i + 1 < len(lines):
                            try:
                                score = float(lines[i + 1].strip())
                                result[line] = score
                                i += 2  # 라벨+숫자 처리시 두줄 스킵
                                continue
                            except ValueError:
                                pass
                    i += 1
                    if len(result) == len(cls.teg_name):
                        break
            if len(result)!=len(cls.teg_name):
                raise_business_exception(ErrorCode.CST_PROCESSING_ERROR, "점수를 추출 할 수 없습니다.")
        return result


