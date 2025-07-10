
import fitz
path="./testPDF/KARSA 직업흥미검사 결과지.pdf"
doc = fitz.open(path)

start_teg="<참조> 흥미 유형 육각형 모양 해석"
result = {}
teg=["R","I","A","S","E","C"]
i=0
for page in doc:
    text = page.get_text()
    lines = text.strip().split('\n')
    start_extract=False
    for line in lines:
        line = line.strip()
        if start_teg in line:
            start_extract = True
            continue
        if start_extract:
            try:
                val=float(line)
                result[teg[i]] = val
                i+=1
                if len(result)==len(teg):
                    break
            except ValueError:
                continue
    if len(result)==len(teg):
        break
print(result)


