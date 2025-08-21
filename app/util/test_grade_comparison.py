"""
GradeComparisonUtil 클래스 사용 예시
객체지향적으로 User 객체의 관계를 통해 데이터를 처리합니다.
"""

from app.util.GradeComparisonUtil import GradeComparisonUtil
from app.domain.User import User
from app.domain.reportModule.Report import Report
from app.domain.reportModule.ReportScore import ReportScore
from app.domain.AdmissionScore import AdmissionScore


def test_grade_comparison_with_user_object():
    """
    User 객체를 사용한 GradeComparisonUtil 테스트
    """
    
    try:
        # Util 클래스 인스턴스 생성 (DB 세션 불필요)
        grade_util = GradeComparisonUtil()
        
        # 테스트용 User 객체 생성 (실제 사용시에는 DB에서 조회한 객체 사용)
        test_user = create_test_user()
        
        print("=== User 객체를 사용한 교과 성적 분석 ===")
        
        # 1. 교과 성적 요약
        grade_summary = grade_util.get_user_grade_summary(test_user)
        print(f"전체 평균등급: {grade_summary.get('overall_average_grade', 'N/A')}")
        print(f"총 과목 수: {grade_summary.get('total_subjects', 0)}")
        print(f"과목별 평균등급: {grade_summary.get('subject_averages', {})}")
        print(f"등급별 분포: {grade_summary.get('grade_distribution', {})}")
        print()
        
        # 2. 과목별 평균등급
        subject_averages = grade_util.calculate_user_subject_average_grade(test_user)
        print("=== 과목별 평균등급 ===")
        for subject, grade in subject_averages.items():
            print(f"{subject}: {grade}등급")
        print()
        
        # 3. 전체 평균등급
        overall_grade = grade_util.calculate_user_overall_average_grade(test_user)
        print(f"=== 전체 평균등급: {overall_grade}등급 ===")
        print()
        
        # 4. 북마크 정보
        bookmarks = grade_util.get_user_major_bookmarks_info(test_user)
        print("=== 북마크 정보 ===")
        for bookmark in bookmarks:
            print(f"ID: {bookmark['id']}, 학과: {bookmark['major_name']}, 대학교: {bookmark['university_name']}")
        print()
        
        # 5. 과목 카테고리별 등급
        category_grades = grade_util.get_user_category_grades(test_user)
        print("=== 과목 카테고리별 등급 ===")
        for category, grade in category_grades.items():
            print(f"{category}: {grade}등급")
        print()
        
        # 6. 학기별 성적표
        for term in [1, 2, 3]:
            term_reports = grade_util.get_user_reports_by_term(test_user, term)
            print(f"=== {term}학기 성적표 ({len(term_reports)}개) ===")
            for report in term_reports:
                print(f"  카테고리: {report.categoryName}, 등급: {report.categoryGrade}, 학년: {report.userGrade}")
        print()
        
        # 7. 학년별 성적표
        for grade in [1, 2, 3]:
            grade_reports = grade_util.get_user_reports_by_grade(test_user, grade)
            print(f"=== {grade}학년 성적표 ({len(grade_reports)}개) ===")
            for report in grade_reports:
                print(f"  카테고리: {report.categoryName}, 등급: {report.categoryGrade}, 학기: {report.term}")
        print()
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")


def test_with_admission_cutoffs():
    """
    합격 등급컷과 함께 테스트
    """
    try:
        grade_util = GradeComparisonUtil()
        
        # 테스트용 User 객체 생성
        test_user = create_test_user()
        
        # 테스트용 합격 등급컷 데이터 생성
        admission_cutoffs = create_test_admission_cutoffs()
        
        print("=== 합격 등급컷과 함께 테스트 ===")
        
        # 1. 북마크 합격 등급컷 요약
        bookmark_summary = grade_util.get_bookmark_cutoff_summary(test_user, admission_cutoffs)
        print(f"총 북마크 수: {bookmark_summary.get('total_bookmarks', 0)}")
        print(f"학과-학교 북마크: {bookmark_summary.get('university_major_bookmarks', 0)}")
        print(f"학과만 북마크: {bookmark_summary.get('major_only_bookmarks', 0)}")
        print(f"합격 등급컷 정보 있는 북마크: {bookmark_summary.get('bookmarks_with_cutoffs', 0)}")
        print()
        
        # 2. 등급 비교 결과
        comparison_results = grade_util.compare_user_grade_with_cutoffs(test_user, admission_cutoffs)
        print("=== 등급 비교 결과 ===")
        
        if comparison_results:
            for result in comparison_results:
                print(f"학과: {result.get('major_name', 'N/A')}")
                print(f"대학교: {result.get('university_name', 'N/A')}")
                print(f"전형: {result.get('admission_type', 'N/A')}")
                print(f"유저 등급: {result.get('user_grade', 'N/A')}")
                print(f"90% 합격 등급컷: {result.get('cutoff_90', 'N/A')}")
                print(f"진학 방향: {result.get('admission_direction', 'N/A')}")
                print(f"등급 차이: {result.get('grade_difference', 'N/A')}")
                print(f"상태: {result.get('status', 'N/A')}")
                print("-" * 40)
        else:
            print("비교할 북마크가 없거나 오류가 발생했습니다.")
        print()
        
        # 3. 종합 분석
        comprehensive_analysis = grade_util.get_comprehensive_user_analysis(test_user, admission_cutoffs)
        print("=== 종합 분석 결과 ===")
        print(f"유저 정보: {comprehensive_analysis.get('user_info', {})}")
        comparison_analysis = comprehensive_analysis.get('comparison_analysis', {})
        print(f"하향 지원 가능: {comparison_analysis.get('down_count', 0)}개")
        print(f"적정 지원 가능: {comparison_analysis.get('appropriate_count', 0)}개")
        print(f"상향 지원 필요: {comparison_analysis.get('up_count', 0)}개")
        print(f"추천사항: {comprehensive_analysis.get('recommendations', [])}")
        
    except Exception as e:
        print(f"합격 등급컷 테스트 중 오류 발생: {e}")


def create_test_user():
    """
    테스트용 User 객체를 생성합니다.
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
    
    # 3학기 성적표
    report3 = Report()
    report3.id = 3
    report3.categoryName = 2  # ENGLISH
    report3.categoryGrade = 2.2
    report3.uid = user.uid
    report3.term = 3
    report3.userGrade = 3
    
    # 3학기 세부 과목 점수들
    report3.reportScores = []
    score5 = ReportScore()
    score5.id = 5
    score5.subject = "영어"
    score5.grade = 2
    score5.credit = 3
    score5.rId = report3.id
    report3.reportScores.append(score5)
    
    score6 = ReportScore()
    score6.id = 6
    score6.subject = "영어독해"
    score6.grade = 3
    score6.credit = 2
    score6.rId = report3.id
    report3.reportScores.append(score6)
    
    reports.append(report3)
    
    # User 객체에 reports 설정
    user.reports = reports
    
    # 테스트용 MajorBookmark 객체들 생성 (실제로는 더 복잡한 관계가 필요)
    # 여기서는 간단하게 생성
    user.majorBookmarks = []
    
    return user


def create_test_admission_cutoffs():
    """
    테스트용 합격 등급컷 데이터를 생성합니다.
    """
    cutoffs = {}
    
    # (1, 1) 학과-학교의 합격 등급컷
    key1 = (1, 1)
    cutoffs[key1] = {
        "교과성적우수자전형": {
            "cut_50": 1.5,
            "cut_70": 2.0,
            "cut_90": 2.5
        }
    }
    
    # (2, 1) 학과-학교의 합격 등급컷
    key2 = (2, 1)
    cutoffs[key2] = {
        "교과성적우수자전형": {
            "cut_50": 2.0,
            "cut_70": 2.5,
            "cut_90": 3.0
        }
    }
    
    return cutoffs


def demonstrate_usage():
    """
    실제 사용법을 보여주는 함수
    """
    print("=== GradeComparisonUtil 사용법 ===")
    print()
    
    print("1. 기본 사용법:")
    print("   grade_util = GradeComparisonUtil()  # DB 세션 불필요")
    print("   user = get_user_from_db(uid)        # DB에서 User 객체 조회")
    print("   grade_summary = grade_util.get_user_grade_summary(user)")
    print()
    
    print("2. 객체지향적 데이터 접근:")
    print("   user.reports                    # 유저의 모든 성적표")
    print("   user.majorBookmarks            # 유저의 북마크")
    print("   reportModule.reportScores            # 성적표의 세부 점수들")
    print()
    
    print("3. 주요 메서드:")
    print("   - calculate_user_subject_average_grade(user)")
    print("   - calculate_user_overall_average_grade(user)")
    print("   - get_user_grade_summary(user)")
    print("   - compare_user_grade_with_cutoffs(user, admission_cutoffs)")
    print("   - get_comprehensive_user_analysis(user, admission_cutoffs)")
    print()
    
    print("4. 장점:")
    print("   - DB 세션 불필요")
    print("   - 객체지향적 데이터 처리")
    print("   - User 객체의 관계를 통한 자연스러운 데이터 접근")
    print("   - 테스트하기 쉬움")
    print("   - 의존성 분리")


if __name__ == "__main__":
    # 사용법 설명
    demonstrate_usage()
    
    print("\n" + "="*60 + "\n")
    
    # 기본 테스트
    test_grade_comparison_with_user_object()
    
    print("\n" + "="*60 + "\n")
    
    # 합격 등급컷과 함께 테스트
    test_with_admission_cutoffs()
