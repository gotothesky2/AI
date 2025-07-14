import fitz  # PyMuPDF를 임포트

# 문서 열기
doc = fitz.open("./testPDF/KARSA 직업흥미검사 결과지.pdf")

# 첫 페이지의 텍스트 추출
for page in doc:
    text = page.get_text()
    print(text)
