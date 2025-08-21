"""
AiTotalReport 클래스 테스트
북마크가 있을 때 GradeComparisonUtil을 활용한 분석 결과를 확인합니다.
"""

from app.gptApi.totalReport import AiTotalReport
from app.domain.User import User
from app.domain.reportModule.Report import Report
from app.domain.reportModule.ReportScore import ReportScore
from app.domain.MajorBookmark import MajorBookmark


def create_test_user_with_bookmarks():
    """
    테스트용 User 객체를 생성합니다 (북마크 포함).
    """
    user = User()
    user.uid = "test_user_123"
    user.name = "테스트 유저"
    user.email = "test@example.com"
    user.gradeNum = 3
    user.sex = "남"
    
    # 테스트용 Report 객체들 생성
    reports = []
    
    # 1학기 성적표
    report1 = Report()
    report1.id = 1
    report1.categoryName = 0  # KOREAN
    report1.categoryGrade = 2.5
    report1.uid = user.uid
    report1.term = 1
    report1.userGrade = 3
    
    # 1학기 세부 과목 점수들
    report1.reportScores = []
    score1 = ReportScore()
    score1.id = 1
    score1.subject = "국어"
    score1.grade = 2
    score1.credit = 3
    score1.rId = report1.id
    report1.reportScores.append(score1)
    
    score2 = ReportScore()
    score2.id = 2
    score2.subject = "문학"
    score2.grade = 3
    score2.credit = 2
    score2.rId = report1.id
    report1.reportScores.append(score2)
    
    reports.append(report1)
    
    # 2학기 성적표
    report2 = Report()
    report2.id = 2
    report2.categoryName = 1  # MATH
    report2.categoryGrade = 1.8
    report2.uid = user.uid
    report2.term = 2
    report2.userGrade = 3
    
    # 2학기 세부 과목 점수들
    report2.reportScores = []
    score3 = ReportScore()
    score3.id = 3
    score3.subject = "수학"
    score3.grade = 1
    score3.credit = 4
    score3.rId = report2.id
    report2.reportScores.append(score3)
    
    score4 = ReportScore()
    score4.id = 4
    score4.subject = "미적분"
    score4.grade = 2
    score4.credit = 3
    score4.rId = report2.id
    report2.reportScores.append(score4)
    
    reports.append(report2)
    
    # User 객체에 reports 설정
    user.reports = reports
    
    # 테스트용 MajorBookmark 객체들 생성
    bookmarks = []
    
    bookmark1 = MajorBookmark()
    bookmark1.id = 1
    bookmark1.major_id = 1
    bookmark1.univId = 1
    bookmark1.uid = user.uid
    # 간단한 Mock 객체 생성 (실제로는 더 복잡한 관계가 필요)
    bookmark1.major = type('MockMajor', (), {'name': '컴퓨터공학과'})()
    bookmark1.university = type('MockUniversity', (), {'name': '서울대학교'})()
    bookmarks.append(bookmark1)
    
    bookmark2 = MajorBookmark()
    bookmark2.id = 2
    bookmark2.major_id = 2
    bookmark2.univId = 2
    bookmark2.uid = user.uid
    bookmark2.major = type('MockMajor', (), {'name': '경영학과'})()
    bookmark2.university = type('MockUniversity', (), {'name': '연세대학교'})()
    bookmarks.append(bookmark2)
    
    user.majorBookmarks = bookmarks
    
    return user


def create_test_admission_cutoffs():
    """
    테스트용 합격 등급컷 데이터를 생성합니다.
    간단한 딕셔너리 형태로 생성합니다.
    """
    cutoffs = {}
    
    # (1, 1) 학과-학교의 합격 등급컷 (컴퓨터공학과, 서울대학교)
    key1 = (1, 1)
    cutoffs[key1] = {
        "교과성적우수자전형": {
            "cut_50": 1.5,
            "cut_70": 2.0,
            "cut_90": 2.5
        }
    }
    
    # (2, 2) 학과-학교의 합격 등급컷 (경영학과, 연세대학교)
    key2 = (2, 2)
    cutoffs[key2] = {
        "교과성적우수자전형": {
            "cut_50": 2.0,
            "cut_70": 2.5,
            "cut_90": 3.0
        }
    }
    
    return cutoffs


def test_bookmark_analysis():
    """
    북마크 분석 기능을 테스트합니다.
    """
    try:
        # 테스트용 데이터 생성
        user = create_test_user_with_bookmarks()
        admission_cutoffs = create_test_admission_cutoffs()
        
        print("=== 북마크 분석 테스트 ===")
        
        # 북마크가 있는 경우 분석
        print("1. 북마크가 있는 경우:")
        analysis_with_bookmark = AiTotalReport._generate_bookmark_analysis(user, True, admission_cutoffs)
        print(analysis_with_bookmark)
        
        print("\n" + "="*60 + "\n")
        
        # 북마크가 없는 경우 분석
        print("2. 북마크가 없는 경우:")
        analysis_without_bookmark = AiTotalReport._generate_bookmark_analysis(user, False, admission_cutoffs)
        print(analysis_without_bookmark)
        
        print("\n" + "="*60 + "\n")
        
        # 북마크는 있지만 합격 등급컷이 없는 경우
        print("3. 북마크는 있지만 합격 등급컷이 없는 경우:")
        analysis_no_cutoffs = AiTotalReport._generate_bookmark_analysis(user, True, {})
        print(analysis_no_cutoffs)
        
    except Exception as e:
        print(f"북마크 분석 테스트 중 오류 발생: {e}")


def test_user_prompt():
    """
    user_prompt 메서드를 테스트합니다.
    """
    try:
        # 테스트용 데이터 생성
        user = create_test_user_with_bookmarks()
        admission_cutoffs = create_test_admission_cutoffs()
        
        print("=== User Prompt 테스트 ===")
        
        # 테스트용 리포트 데이터
        test_report = "직업 흥미검사 결과: R형(실재형) 70%, I형(탐구형) 20%, A형(예술형) 10%"
        score_report = "교과 성적: 국어 2등급, 수학 1등급, 영어 2등급"
        
        # 북마크가 있는 경우
        print("1. 북마크가 있는 경우:")
        prompt_with_bookmark = AiTotalReport.user_prompt(test_report, score_report, user, True)
        print(prompt_with_bookmark)
        
        print("\n" + "="*60 + "\n")
        
        # 북마크가 없는 경우
        print("2. 북마크가 없는 경우:")
        prompt_without_bookmark = AiTotalReport.user_prompt(test_report, score_report, user, False)
        print(prompt_without_bookmark)
        
    except Exception as e:
        print(f"User Prompt 테스트 중 오류 발생: {e}")


def demonstrate_usage():
    """
    실제 사용법을 보여줍니다.
    """
    print("=== AiTotalReport 사용법 ===")
    print()
    
    print("1. 기본 사용법:")
    print("   user = get_user_with_bookmarks(uid)")
    print("   # 전역 DB 컨텍스트가 설정되어 있어야 함")
    print("   reportModule = AiTotalReport(test_report, score_report, user, True)")
    print()
    
    print("2. 북마크가 없는 경우:")
    print("   reportModule = AiTotalReport(test_report, score_report, user, False)")
    print()
    
    print("3. 생성되는 프롬프트 내용:")
    print("   - 직업 흥미검사/적성검사 분석")
    print("   - 교과/모의고사 성적 분석")
    print("   - 관심 학과-학교 분석 (북마크가 있는 경우)")
    print("     * 유저의 교과 평균등급")
    print("     * 북마크한 학과-학교 목록")
    print("     * 합격 등급컷 비교 결과 (전역 DB에서 자동 조회)")
    print("     * 진학 방향 (상향/적정/하향)")


if __name__ == "__main__":
    # 사용법 설명
    demonstrate_usage()
    
    print("\n" + "="*60 + "\n")
    
    # 북마크 분석 테스트
    test_bookmark_analysis()
    
    print("\n" + "="*60 + "\n")
    
    # User Prompt 테스트
    test_user_prompt()
