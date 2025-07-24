from app.domain.Cst import Cst
from app.domain.Hmt import Hmt
from app.gptApi.testReportEng.testReport import testReport

# 테스트용 Cst 객체 생성 및 점수 할당
cst = Cst()
cst.physicalScore = 80
cst.handScore = 75
cst.spaceScore = 90
cst.musicScore = 60
cst.creativeScore = 85
cst.langScore = 70
cst.mathScore = 95
cst.selfScore = 88
cst.relationScore = 77
cst.natureScore = 66
cst.artScore = 82

# 테스트용 Hmt 객체 생성 및 점수 할당
hmt = Hmt()
hmt.rScore = 65
hmt.iScore = 78
hmt.aScore = 88
hmt.sScore = 72
hmt.eScore = 69
hmt.cScore = 80

print(testReport(hmt,cst))
# testReport의 system_prompt, user_prompt 결과 출력
