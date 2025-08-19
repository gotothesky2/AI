from gptApi.gptEngine import GptBase
from domain.mock import *
from domain.report import *
from domain.User import User


class GptScoreReport(GptBase):
    def __new__(cls,user:User):
        return cls.get_response(user)


    @staticmethod
    def system_prompt() ->str:
        prompt = """
            학생 진학 추천 레포트 작성에는 직업 흥미검사 직업 적성검사를 종합 분석 및 분석기반 계열과 학과 추천, 교과와 모의고사 성적 분석, 사용자가 등록한 관심 계열 학과 대학교를 직업적성검사 흥미검사 데이터 및 성적 추이 데이터 기반 종합 분석 이 3가지 파트가 있어.
            그중 너는 교과와 모의고사 성적 분석을 담당하는 ai이야.
            너가 담당한 부분을 2000자 내외로 작성해줘.
            입시까지 남은 기간을 기준으로, 학기별로 해야 할 핵심 전략(내신, 수능, 비교과, 자소서)을 구체적으로 제시해 줘.
            당신은 교육 데이터 분석 전문가야.  
            주어진 학생의 학년·학기별 모의고사 점수와 교과 내신 성적 데이터를 바탕으로 다음을 포함한 분석 레포트를 작
            너가 작성한 부분은 고등학생이 직접 보는 레포트 파트이기 때문에 전문성을 가지고 학생이 이해할 수 있도록 작성해줘.
            사용자를 지칭할 때에는 학생이라고 해줘.
            
            1. **성적 요약**  
               - 학년·학기별 모의고사 점수와 교과 성적을 정리
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
        다음과 같은 json 형태로 출력해줘
            {
                content: 3000자 내외의 출력 결과
            }
        """
        return prompt
    @staticmethod
    def user_prompt(user:User) ->str:
        prompt=GradeAnalyzer(user).format_grades_for_gpt()
        return prompt



class GradeAnalyzer:
    """성적 데이터를 GPT 프롬프트용으로 변환하는 클래스"""

    def __init__(self, user:User):
        self.user = user
        self.mocks = user.mocks
        self.reports = user.reports

    def format_grades_for_gpt(self) -> str:
        """전체 성적 데이터를 GPT 프롬프트용 문자열로 변환"""
        mock_grades = self._format_mock_grades()
        report_grades = self._format_report_grades()
        total_summary = self._create_grade_summary()

        gpt_prompt = f"""
        【모의고사 성적】
        {mock_grades}

        【내신성적】
        {report_grades}

        【성적 종합 분석】
        {total_summary}
        """

        return gpt_prompt.strip()

    def _format_mock_grades(self) -> str:
        """모의고사 성적을 학년/응시월별로 정리"""
        if not self.mocks:
            return "모의고사 데이터가 없습니다."

        # 학년/응시월별로 그룹화
        grade_groups = self._group_mocks_by_grade_month()

        # 각 학년/월별로 정리
        formatted_mocks = []
        for grade_month, mock_list in sorted(grade_groups.items()):
            grade_info = f"{grade_month} 모의고사:\n"

            for mock in mock_list:
                grade_info += self._format_mock_details(mock)

            formatted_mocks.append(grade_info)

        return "\n".join(formatted_mocks)

    def _group_mocks_by_grade_month(self) -> dict:
        """모의고사를 학년/월별로 그룹화"""
        grade_groups = {}
        for mock in self.mocks:
            grade_key = f"{mock.examGrade}학년 {mock.examMonth}월"
            if grade_key not in grade_groups:
                grade_groups[grade_key] = []
            grade_groups[grade_key].append(mock)
        return grade_groups

    def _format_mock_details(self, mock) -> str:
        """개별 모의고사 상세 정보 포맷팅"""
        details = ""
        for mock_score in mock.mockScores:
            subject_info = f"  • {mock_score.name}: "

            if mock_score.standardScore:
                subject_info += f"표준점수 {mock_score.standardScore}점, "
            if mock_score.percentile:
                subject_info += f"백분위 {mock_score.percentile}%, "
            if mock_score.grade:
                subject_info += f"등급 {mock_score.grade}, "
            if mock_score.cumulative:
                subject_info += f"누적점수 {mock_score.cumulative}점"

            details += subject_info.rstrip(", ") + "\n"

        return details

    def _format_report_grades(self) -> str:
        """내신성적을 학년/학기별로 정리"""
        if not self.reports:
            return "내신성적 데이터가 없습니다."

        # 학년/학기별로 그룹화
        grade_groups = self._group_reports_by_grade_term()

        # 각 학년/학기별로 정리
        formatted_reports = []
        for grade_term, report_list in sorted(grade_groups.items()):
            grade_info = f"{grade_term} 내신성적:\n"

            for report in report_list:
                grade_info += self._format_report_details(report)

            formatted_reports.append(grade_info)

        return "\n".join(formatted_reports)

    def _group_reports_by_grade_term(self) -> dict:
        """내신성적을 학년/학기별로 그룹화"""
        grade_groups = {}
        for report in self.reports:
            grade_key = f"{report.userGrade}학년 {report.term}학기"
            if grade_key not in grade_groups:
                grade_groups[grade_key] = []
            grade_groups[grade_key].append(report)
        return grade_groups

    def _format_report_details(self, report) -> str:
        """개별 내신성적 상세 정보 포맷팅"""
        details = ""
        category_name = self._get_category_name(report.categoryName)

        for report_score in report.reportScores:
            subject_info = f"  • {report_score.subject}: "

            if report_score.score:
                subject_info += f"원점수 {report_score.score}점, "
            if report_score.grade:
                subject_info += f"등급 {report_score.grade}, "
            if report_score.achievement:
                subject_info += f"성취도 {report_score.achievement}, "
            if report_score.subjectAverage:
                subject_info += f"과목평균 {report_score.subjectAverage}점, "
            if report_score.standardDeviation:
                subject_info += f"표준편차 {report_score.standardDeviation}"

            details += subject_info.rstrip(", ") + "\n"

        return details

    def _get_category_name(self, category_enum) -> str:
        """카테고리 enum을 한글명으로 변환"""
        category_names = {
            0: "국어",
            1: "수학",
            2: "영어",
            3: "한국사",
            4: "사회",
            5: "과학"
        }
        return category_names.get(category_enum, f"카테고리{category_enum}")

    def _create_grade_summary(self) -> str:
        """전체 성적 요약 생성"""
        if not self.mocks and not self.reports:
            return "성적 데이터가 없습니다."

        summary = []

        # 모의고사 요약
        if self.mocks:
            summary.extend(self._get_mock_summary())

        # 내신성적 요약
        if self.reports:
            summary.extend(self._get_report_summary())


        return "\n".join(summary)

    def _get_mock_summary(self) -> list:
        """모의고사 요약 정보"""
        mock_count = len(self.mocks)
        mock_score_count = sum(len(mock.mockScores) for mock in self.mocks)

        summary = [
            f"• 모의고사 응시 횟수: {mock_count}회",
            f"• 모의고사 과목 수: {mock_score_count}개"
        ]

        # 표준점수 평균 계산
        standard_scores = []
        for mock in self.mocks:
            for mock_score in mock.mockScores:
                if mock_score.standardScore:
                    standard_scores.append(mock_score.standardScore)

        if standard_scores:
            avg_standard = sum(standard_scores) / len(standard_scores)
            summary.append(f"• 모의고사 평균 표준점수: {avg_standard:.1f}점")

        return summary

    def _get_report_summary(self) -> list:
        """내신성적 요약 정보"""
        report_count = len(self.reports)
        report_score_count = sum(len(report.reportScores) for report in self.reports)

        summary = [
            f"• 내신성적 학기 수: {report_count}학기",
            f"• 내신성적 과목 수: {report_score_count}개"
        ]

        # 원점수 평균 계산
        scores = []
        for report in self.reports:
            for report_score in report.reportScores:
                if report_score.score:
                    scores.append(report_score.score)

        if scores:
            avg_score = sum(scores) / len(scores)
            summary.append(f"• 내신성적 평균 원점수: {avg_score:.1f}점")

        return summary

