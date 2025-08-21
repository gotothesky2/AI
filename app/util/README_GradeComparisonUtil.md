# GradeComparisonUtil 사용 가이드

## 개요
`GradeComparisonUtil`은 유저의 교과 평균등급과 학과-학교 관심목록의 90퍼 합격 등급컷을 비교할 수 있는 유틸리티 클래스입니다.

**핵심 특징:**
- **객체지향적 설계**: User 객체의 관계(`user.reports`, `user.majorBookmarks`)를 통해 데이터 접근
- **전역 DB 지원**: 전역 데이터베이스 컨텍스트를 통한 자동 데이터베이스 접근
- **의존성 분리**: 비즈니스 로직과 데이터 접근 로직 분리

## 주요 기능

### 1. 교과 평균등급 계산
- **과목별 평균등급**: 각 과목의 등급과 학점을 고려한 가중 평균 등급
- **전체 평균등급**: 모든 과목의 등급과 학점을 고려한 전체 평균 등급

### 2. 학과-학교 관심목록 관리
- 유저가 북마크한 학과-학교 목록 조회
- 학과만 북마크한 경우와 학과-학교를 함께 북마크한 경우 구분

### 3. 합격 등급컷 비교
- 유저의 교과 평균등급과 관심 학과-학교의 90퍼 합격 등급컷 비교
- 합격 가능 여부 판단 및 등급 차이 계산

## 사용법

### 기본 사용법
```python
from app.util.GradeComparisonUtil import GradeComparisonUtil

# 전역 데이터베이스 사용
grade_util = GradeComparisonUtil()

# User 객체 조회 (서비스 레이어에서)
user = user_service.get_user_by_uid(uid)

# 객체지향적 데이터 접근
grade_summary = grade_util.get_user_grade_summary(user)
```

**참고**: 전역 데이터베이스를 사용하려면 `app.util.globalDB.db_context.set_db(session)`로 컨텍스트를 설정해야 합니다.

### 1. 유저의 교과 평균등급 계산
```python
# 과목별 평균등급
subject_averages = grade_util.calculate_user_subject_average_grade(user)
print(f"수학: {subject_averages.get('수학', 'N/A')}등급")
print(f"영어: {subject_averages.get('영어', 'N/A')}등급")

# 전체 평균등급
overall_average = grade_util.calculate_user_overall_average_grade(user)
print(f"전체 평균등급: {overall_average}등급")
```

### 2. 유저의 교과 성적 요약
```python
grade_summary = grade_util.get_user_grade_summary(user)
print(f"전체 평균등급: {grade_summary['overall_average_grade']}")
print(f"총 과목 수: {grade_summary['total_subjects']}")
print(f"과목별 평균등급: {grade_summary['subject_averages']}")
print(f"등급별 분포: {grade_summary['grade_distribution']}")
```

### 3. 북마크한 학과-학교 목록 조회
```python
bookmarks = grade_util.get_user_major_bookmarks_info(user)
for bookmark in bookmarks:
    print(f"학과: {bookmark['major_name']}")
    print(f"대학교: {bookmark['university_name']}")
```

### 4. 합격 등급컷 조회 및 비교
```python
# 전역 DB에서 자동 조회
comparison_results = grade_util.compare_user_grade_with_cutoffs(user)

for result in comparison_results:
    print(f"학과: {result['major_name']}")
    print(f"대학교: {result['university_name']}")
    print(f"전형: {result['admission_type']}")
    print(f"유저 등급: {result['user_grade']}등급")
    print(f"90% 합격 등급컷: {result['cutoff_90']}등급")
    print(f"진학 방향: {result['admission_direction']}")
    print(f"등급 차이: {result['grade_difference']}등급")
    print(f"상태: {result['status']}")
```

### 5. 북마크 합격 등급컷 요약
```python
# 전역 DB에서 자동 조회
bookmark_summary = grade_util.get_bookmark_cutoff_summary(user)

print(f"총 북마크 수: {bookmark_summary['total_bookmarks']}")
print(f"학과-학교 북마크: {bookmark_summary['university_major_bookmarks']}")
print(f"학과만 북마크: {bookmark_summary['major_only_bookmarks']}")
print(f"합격 등급컷 정보 있는 북마크: {bookmark_summary['bookmarks_with_cutoffs']}")
```

### 6. 유저 종합 분석
```python
# 전역 DB에서 자동 조회
comprehensive_analysis = grade_util.get_comprehensive_user_analysis(user)

print(f"유저 정보: {comprehensive_analysis['user_info']}")
print(f"교과 성적: {comprehensive_analysis['grade_analysis']}")
print(f"북마크 분석: {comprehensive_analysis['bookmark_analysis']}")

# 진학 방향별 분석
comparison_analysis = comprehensive_analysis['comparison_analysis']
print(f"하향 지원 가능: {comparison_analysis['down_count']}개")
print(f"적정 지원 가능: {comparison_analysis['appropriate_count']}개")
print(f"상향 지원 필요: {comparison_analysis['up_count']}개")
print(f"추천사항: {comprehensive_analysis['recommendations']}")
```

### 7. 학기별/학년별 성적표 조회
```python
# 특정 학기 성적표
term_reports = grade_util.get_user_reports_by_term(user, 1)  # 1학기

# 특정 학년 성적표
grade_reports = grade_util.get_user_reports_by_grade(user, 3)  # 3학년
```

### 8. 과목 카테고리별 등급
```python
category_grades = grade_util.get_user_category_grades(user)
for category, grade in category_grades.items():
    print(f"{category}: {grade}등급")
```

## 객체지향적 데이터 접근

### User 객체의 관계 구조
```python
user = User()
user.reports                    # List[Report] - 유저의 모든 성적표
user.majorBookmarks            # List[MajorBookmark] - 유저의 북마크

# Report 객체
report = user.reports[0]
report.categoryName            # 과목 카테고리 (KOREAN, MATH, ENGLISH 등)
report.categoryGrade           # 카테고리별 등급
report.term                    # 학기 (1, 2, 3)
report.userGrade               # 학년 (1, 2, 3)
report.reportScores            # List[ReportScore] - 세부 과목 점수들

# ReportScore 객체
score = report.reportScores[0]
score.subject                  # 과목명
score.grade                    # 등급
score.credit                   # 학점
```

## 반환 데이터 구조

### 교과 평균등급 계산 결과
```python
{
    '수학': 2.5,      # 수학 과목의 평균등급
    '영어': 1.8,      # 영어 과목의 평균등급
    '국어': 2.2       # 국어 과목의 평균등급
}
```

### 등급 비교 결과
```python
[
    {
        'bookmark_id': 1,
        'major_name': '컴퓨터공학과',
        'university_name': '서울대학교',
        'admission_type': '교과성적우수자전형',
        'user_grade': 2.1,
        'cutoff_90': 2.5,
        'admission_direction': '하향',
        'grade_difference': 0.4,
        'status': '하향 지원 가능',
        'is_eligible': True  # 기존 호환성을 위해 유지
    }
]
```

### 교과 성적 요약
```python
{
    'uid': 'user_123',
    'overall_average_grade': 2.1,
    'total_subjects': 3,
    'subject_averages': {'수학': 2.5, '영어': 1.8, '국어': 2.2},
    'grade_distribution': {'2등급': 2, '1등급': 1}
}
```

## 주의사항

1. **학점 정보**: 과목의 학점(`credit`)이 없는 경우 기본값 1로 설정됩니다.
2. **등급 비교**: 낮은 등급이 더 좋은 성적을 의미합니다 (1등급 > 2등급 > 3등급).
3. **진학 방향**: 등급 차이에 따라 상향/적정/하향으로 분류됩니다.
   - **하향**: 등급 차이 ≥ 0.5 (안정적인 합격 가능)
   - **적정**: 0 ≤ 등급 차이 < 0.5 (적절한 도전)
   - **상향**: 등급 차이 < 0 (성적 향상 필요)
4. **등급컷 유효성**: 0등급이나 None 값은 유효하지 않은 데이터로 처리됩니다.
5. **객체 관계**: User 객체에 `reports`와 `majorBookmarks` 관계가 로드되어 있어야 합니다.

## 에러 처리

모든 메서드는 예외 발생 시 빈 딕셔너리나 리스트를 반환하며, 콘솔에 오류 메시지를 출력합니다. 실제 운영 환경에서는 적절한 로깅 시스템을 사용하는 것을 권장합니다.

### 등급컷 데이터 유효성 검사
- **0등급 처리**: 0등급은 유효하지 않은 데이터로 간주하여 None으로 처리
- **None 값 처리**: 데이터베이스에 등급컷 정보가 없는 경우 None으로 처리
- **범위 검사**: 일반적으로 1~9등급 범위 내의 값만 유효한 것으로 처리
- **자동 필터링**: `get_valid_cutoffs_only()` 메서드로 유효한 등급컷만 자동 필터링

## 장점

### 1. **의존성 분리**
- 전역 데이터베이스 컨텍스트를 통한 자동 데이터 접근
- 비즈니스 로직과 데이터 접근 로직 분리

### 2. **객체지향적 설계**
- User 객체의 관계를 통한 자연스러운 데이터 접근
- 코드의 가독성과 유지보수성 향상

### 3. **테스트 용이성**
- Mock 객체를 사용한 단위 테스트 가능
- 데이터베이스 연결 없이 테스트 실행

### 4. **재사용성**
- 다양한 서비스 레이어에서 활용 가능
- 전역 DB 컨텍스트를 통한 일관된 데이터 접근
- 데이터 소스에 관계없이 동일한 로직 적용

## 테스트

`test_grade_comparison.py` 파일을 참조하여 각 기능을 테스트할 수 있습니다:

```bash
python -m app.util.test_grade_comparison
```

## 실제 사용 예시

### 서비스 레이어에서 사용
```python
class UserAnalysisService:
    def __init__(self):
        # 전역 DB 사용
        self.grade_util = GradeComparisonUtil()
    
    def analyze_user_performance(self, uid: str):
        # 1. User 객체 조회 (관계 포함)
        user = self.user_repository.get_user_with_relations(uid)
        
        # 2. 전역 DB에서 자동으로 합격 등급컷 조회
        analysis = self.grade_util.get_comprehensive_user_analysis(user)
        
        return analysis
```

이제 `GradeComparisonUtil`은 완전히 객체지향적으로 설계되어 User 객체의 관계를 통해 데이터를 처리하며, 전역 데이터베이스 컨텍스트를 통해 자동으로 데이터베이스에 접근합니다.
