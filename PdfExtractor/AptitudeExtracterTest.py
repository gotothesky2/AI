import fitz

# 파일 경로
path = "./testPDF/진로심리검사 _ 중∙고등학생용 _ 직업적성검사 _ 진로정보망 커리ᄋ.pdf"
doc = fitz.open(path)

# 관심 태그 목록
teg_name = [
    "수리·논리력", "예술시각능력", "손재능", "공간지각력", "음악능력",
    "대인관계능력", "창의력", "언어능력", "신체·운동능력", "자연친화력", "자기성찰능력"
]

# 결과 저장용
result = {}

for page in doc:
    text = page.get_text()
    lines = text.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line in teg_name:
            if i + 1 < len(lines):
                try:
                    score = float(lines[i + 1].strip())
                    result[line] = score
                    i += 2  # 라벨+숫자 처리시 두줄 스킵
                    continue
                except ValueError:
                    pass
        i += 1
        if len(result)==11:
            break
if len(result)!=11 :
    print("error")
print(result)