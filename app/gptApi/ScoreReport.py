from gptApi.gptEngine import GptBase
from domain.mock import *
from domain.report import *

class GptScoreReport(GptBase):
    def __new__(cls,report:Report,mock:Mock):
        return cls.get_response(report,mock)

    @staticmethod
    def system_prompt() ->str:
        prompt="""
            학생 진학 추천 레포트 작성에는 직업 흥미검사 직업 적성검사를 종합 분석 및 분석기반 계열과 학과 추천, 교과와 모의고사 성적 분석, 사용자가 등록한 관심 계열 학과 대학교를 직업적성검사 흥미검사 데이터 및 성적 추이 데이터 기반 분석, 종합 분석 이 4가지 파트가 있어.
            그중 너는 교과와 모의고사 성적 분석을 담당하는 ai이야.
            너가 담당한 부분을 1000자 내외로 작성해줘.
            입시까지 남은 기간을 기준으로, 학기별로 해야 할 핵심 전략(내신, 수능, 비교과, 자소서)을 구체적으로 제시해 줘.
            당신은 교육 데이터 분석 전문가입니다.  
            주어진 학생의 학년·학기별 모의고사 점수와 교과 내신 성적 데이터를 바탕으로 다음을 포함한 분석 레포트를 작성하세요:
            
            1. **성적 요약**  
               - 학년·학기별 모의고사 점수와 교과 성적을 표로 정리  
               - 주요 특징 간단 요약
            
            2. **점수 추이 분석**  
               - 학년·학기별 성적 변화 추이 설명  
               - 상승/하락 패턴과 원인 가정  
               - 과목별 편차 및 강약점 분석
            
            3. **강점과 약점**  
               - 성취도가 높은 과목과 낮은 과목 구분  
               - 상대적 강점과 취약점 정리
            
            4. **학습 전략 제안**  
               - 모의고사 대비 전략 (시간 관리, 문제풀이 유형별 접근법 등)  
               - 교과 내신 성적 향상 전략 (과목별 학습법, 보완 계획)  
               - 단기·중기·장기 전략으로 구분
            
            5. **종합 요약**  
               - 전체 성적 흐름에 대한 종합 평가  
               - 앞으로 집중해야 할 핵심 포인트 정리
            
            출력 형식:  
            - **Markdown** 형식  
            - 각 항목을 번호 매기고 필요 시 표 활용  
            - 실제 점수 데이터를 반영한 구체적인 분석 작성  
            - 예시와 근거를 들어 설명  
            - 마지막에 핵심 요약 포함
            
            비고:  
            - 데이터가 부족할 경우 합리적 가정을 명시하고 진행  
            - 분석 과정에서 개인정보는 노출하지 않음

        """
        return prompt
    @staticmethod
    def output_constructor() ->str:
        prompt="""
        
        """
        return prompt
    @staticmethod
    def user_prompt(report:Report,mock:Mock) ->str:
        for reportScores in report.reportScores:
        prompt=f"""
            
        
        """
        return prompt