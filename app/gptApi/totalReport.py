from gptApi.gptEngine import GptBase

class TotalReport(GptBase):
    def __new__(cls):
        return cls.get_response()

    @staticmethod
    def system_prompt() ->str:
        prompt ="""
            학생 진학 추천 레포트 작성에는 직업 흥미검사 직업 적성검사를 종합 분석 및 분석기반 계열과 학과 추천, 교과와 모의고사 성적 분석, 사용자가 등록한 관심 계열 학과 대학교를 직업적성검사 흥미검사 데이터 및 성적 추이 데이터 기반 종합 분석 이 3가지 파트가 있어.
            학생 진학 추천 레포트 작성에는 [직업 흥미검사 직업 적성검사를 종합 분석 및 분석기반 계열과 학과 추천, [교과와 모의고사 성적 분석], [사용자가 등록한 관심 계열 학과 대학교를 직업적성검사 흥미검사 데이터 및 성적 추이 데이터 기반 분석] 출력결과를 바탕으로 종합분석 레포트를 담당하는 ai이야.
            너가 담당한 부분을 3000자 내외로 작성해줘.
            사용자를 지칭할 때에는 학생이라고 해줘.
            어투는 너무 딱딱하진 않게 조금 부드럽게 해줘.
        """
        return prompt

    @staticmethod
    def output_constructor() ->str:
        prompt = """
        """
        return prompt


    @staticmethod
    def user_prompt(testReport:str,scoreReport:str,user:User) ->str:
        prompt = f"""
        [직업 흥미검사 적성검사 종합분석 및 분석기반 계열 학과 추천]
        """
        return prompt
