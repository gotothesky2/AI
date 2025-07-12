import fitz
from fastapi import UploadFile

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
        if isinstance(data,UploadFile):
            data.file.seek(0)
            return data.file.read()
        if isinstance(data, (bytes, bytearray)):
            return data
        if isinstance(data, str):
            with open(data, 'rb') as f:
                return f.read()
        raise ValueError("지원하지 않는 PDF 소스 타입")
    #페이지수 및 검사pdf맞는지 검사
    @classmethod
    def _validate_content(cls,pdf_bytes: bytes)->None:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            # 페이지 수 검증
            if doc.page_count < cls.MIN_PAGE:
                raise ValueError(f"PDF 페이지 수({doc.page_count})가 요구치({cls.MIN_PAGE})보다 적습니다.")
            #pdf 내용물 제목 검사
            txt="".join(page.get_text()for page in doc)
            if cls.REQUIRED_KEYWORD not in txt:
                raise ValueError(f"직업 흥미 검사 결과 PDF가 아닙니다.")
    #점수 추출 로직
    @classmethod
    def _extract_scores(cls,pdf_bytes: bytes)->dict:
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
                            result[teg[i]] = val
                            i += 1
                            if len(result) == len(cls.teg):
                                break
                        except ValueError:
                            continue
                if len(result) == len(cls.teg):
                    break
            if len(result)!=len(cls.teg):
                raise ValueError("점수를 추출 할 수 없습니다.")
        return result


