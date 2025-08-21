from typing import List, Dict, Optional, Tuple, Union
from sqlalchemy.orm import Session
from domain.User import User
from domain.reportModule.Report import Report
from domain.reportModule.ReportScore import ReportScore
from domain.MajorBookmark import MajorBookmark
from domain.AdmissionScore import AdmissionScore
from util.globalDB.global_db import get_global_db


class GradeComparisonUtil:
    """
    유저의 교과 평균등급과 학과-학교 관심목록의 90퍼 합격 등급컷을 비교하는 유틸리티 클래스
    User 객체의 관계를 통해 객체지향적으로 데이터를 처리합니다.
    """
    
    def __init__(self):
        pass
    
    def calculate_user_subject_average_grade(self, user: User) -> Dict[str, float]:
        """
        유저의 교과 평균등급을 계산합니다.
        
        Args:
            user: User 객체
            
        Returns:
            Dict[str, float]: 과목별 평균등급 (과목명: 평균등급)
        """
        try:
            if not user.reports:
                return {}
            
            # 모든 ReportScore 데이터 수집
            all_report_scores = []
            for report in user.reports:
                if report.reportScores:
                    all_report_scores.extend(report.reportScores)
            
            if not all_report_scores:
                return {}
            
            # 과목별로 등급과 학점을 그룹화
            subject_grades = {}
            for score in all_report_scores:
                subject_name = score.subject
                grade = score.grade
                credit = score.credit or 1  # 학점이 없으면 기본값 1
                
                if subject_name not in subject_grades:
                    subject_grades[subject_name] = {
                        'total_grade_weighted': 0,
                        'total_credit': 0
                    }
                
                subject_grades[subject_name]['total_grade_weighted'] += grade * credit
                subject_grades[subject_name]['total_credit'] += credit
            
            # 과목별 평균등급 계산
            subject_averages = {}
            for subject, data in subject_grades.items():
                if data['total_credit'] > 0:
                    average_grade = data['total_grade_weighted'] / data['total_credit']
                    subject_averages[subject] = round(average_grade, 2)
            
            return subject_averages
            
        except Exception as e:
            print(f"교과 평균등급 계산 중 오류 발생: {e}")
            return {}
    
    def calculate_user_overall_average_grade(self, user: User) -> float:
        """
        유저의 전체 교과 평균등급을 계산합니다.
        
        Args:
            user: User 객체
            
        Returns:
            float: 전체 평균등급
        """
        try:
            if not user.reports:
                return 0.0
            
            # 모든 ReportScore 데이터 수집
            all_report_scores = []
            for report in user.reports:
                if report.reportScores:
                    all_report_scores.extend(report.reportScores)
            
            if not all_report_scores:
                return 0.0
            
            total_grade_weighted = 0
            total_credit = 0
            
            for score in all_report_scores:
                grade = score.grade
                credit = score.credit or 1
                
                total_grade_weighted += grade * credit
                total_credit += credit
            
            if total_credit > 0:
                overall_average = total_grade_weighted / total_credit
                return round(overall_average, 2)
            
            return 0.0
            
        except Exception as e:
            print(f"전체 교과 평균등급 계산 중 오류 발생: {e}")
            return 0.0
    
    def get_user_major_bookmarks_info(self, user: User) -> List[Dict]:
        """
        유저가 등록한 학과-학교 관심목록 정보를 가공합니다.
        
        Args:
            user: User 객체
            
        Returns:
            List[Dict]: 학과-학교 관심목록 리스트
        """
        try:
            if not user.majorBookmarks:
                return []
            
            bookmark_list = []
            for bookmark in user.majorBookmarks:
                bookmark_info = {
                    'id': bookmark.id,
                    'major_id': bookmark.major_id,
                    'univ_id': bookmark.univId,
                    'major_name': bookmark.major.name if bookmark.major else None,
                    'university_name': bookmark.university.name if bookmark.university else None
                }
                bookmark_list.append(bookmark_info)
            
            return bookmark_list
            
        except Exception as e:
            print(f"북마크 정보 가공 중 오류 발생: {e}")
            return []
    
    def get_admission_score_cutoffs_from_db(self, univ_ids: List[int] = None, major_ids: List[int] = None) -> Dict[Tuple[int, int], Dict]:
        """
        데이터베이스에서 직접 합격 등급컷 정보를 조회합니다.
        
        Args:
            univ_ids: 조회할 대학교 ID 리스트 (None이면 전체)
            major_ids: 조회할 학과 ID 리스트 (None이면 전체)
            
        Returns:
            Dict[Tuple[int, int], Dict]: 합격 등급컷 정보 (key: (univ_id, major_id))
        """
        try:
            # 전역 데이터베이스 사용
            db_session = get_global_db()
            if not db_session:
                raise Exception("전역 데이터베이스 세션을 찾을 수 없습니다. set_db()로 설정해주세요.")
            
            query = db_session.query(AdmissionScore)
            
            # 특정 대학교나 학과로 필터링
            if univ_ids:
                query = query.filter(AdmissionScore.univId.in_(univ_ids))
            if major_ids:
                query = query.filter(AdmissionScore.majorId.in_(major_ids))
            
            admission_scores = query.all()
            
            cutoffs = {}
            for score in admission_scores:
                admission_type = score.admissionType
                key = (score.univId, score.majorId)
                
                if key not in cutoffs:
                    cutoffs[key] = {}
                
                # 유효성 검사를 통해 등급컷 값 처리
                cut_50 = score.cutFifty if self.validate_grade_cutoff(score.cutFifty) else None
                cut_70 = score.cutSeventy if self.validate_grade_cutoff(score.cutSeventy) else None
                cut_90 = score.cutNinety if self.validate_grade_cutoff(score.cutNinety) else None
                
                cutoffs[key][admission_type] = {
                    'cut_50': cut_50,
                    'cut_70': cut_70,
                    'cut_90': cut_90
                }
            
            return cutoffs
            
        except Exception as e:
            print(f"합격 등급컷 데이터베이스 조회 중 오류 발생: {e}")
            return {}
    
    def compare_user_grade_with_cutoffs(self, user: User) -> List[Dict]:
        """
        유저의 교과 평균등급과 관심 학과-학교의 90퍼 합격 등급컷을 비교합니다.
        
        Args:
            user: User 객체
            admission_cutoffs: 학과-학교별 합격 등급컷 정보 (key: (univ_id, major_id))
            
        Returns:
            List[Dict]: 비교 결과 리스트
        """
        try:
            # 유저의 전체 평균등급 계산
            user_overall_grade = self.calculate_user_overall_average_grade(user)
            
            # 유저의 북마크 정보 가공
            bookmarks = self.get_user_major_bookmarks_info(user)
            
            # 전역 데이터베이스에서 직접 조회
            univ_ids = [b['univ_id'] for b in bookmarks if b['univ_id']]
            major_ids = [b['major_id'] for b in bookmarks if b['major_id']]
            admission_cutoffs = self.get_admission_score_cutoffs_from_db(univ_ids, major_ids)
            
            comparison_results = []
            
            for bookmark in bookmarks:
                univ_id = bookmark['univ_id']
                major_id = bookmark['major_id']
                
                if univ_id and major_id:
                    # 해당 학과-학교의 합격 등급컷 조회
                    cutoff_key = (univ_id, major_id)
                    cutoffs = admission_cutoffs.get(cutoff_key, {})
                    
                    for admission_type, cutoff_data in cutoffs.items():
                        cut_90 = cutoff_data.get('cut_90')
                        
                        if cut_90 is not None and cut_90 > 0:
                            # 등급 비교 (낮은 등급이 더 좋음)
                            grade_difference = cut_90 - user_overall_grade
                            
                            # 진학 방향 결정
                            if grade_difference >= 0.5:
                                admission_direction = '하향'
                                status = '하향 지원 가능'
                            elif grade_difference >= 0:
                                admission_direction = '적정'
                                status = '적정 지원'
                            else:
                                admission_direction = '상향'
                                status = '상향 지원'
                            
                            result = {
                                'bookmark_id': bookmark['id'],
                                'major_name': bookmark['major_name'],
                                'university_name': bookmark['university_name'],
                                'admission_type': admission_type,
                                'user_grade': user_overall_grade,
                                'cutoff_90': cut_90,
                                'admission_direction': admission_direction,
                                'grade_difference': round(grade_difference, 2),
                                'status': status,
                                'is_eligible': grade_difference >= 0  # 기존 호환성을 위해 유지
                            }
                            
                            comparison_results.append(result)
                        elif cut_90 == 0:
                            # 0등급인 경우 (유효하지 않은 데이터)
                            result = {
                                'bookmark_id': bookmark['id'],
                                'major_name': bookmark['major_name'],
                                'university_name': bookmark['university_name'],
                                'admission_type': admission_type,
                                'user_grade': user_overall_grade,
                                'cutoff_90': cut_90,
                                'is_eligible': None,
                                'grade_difference': None,
                                'status': '등급컷 데이터 오류 (0등급)'
                            }
                            
                            comparison_results.append(result)
                
                else:
                    # 학과만 북마크한 경우 (학교 정보 없음)
                    result = {
                        'bookmark_id': bookmark['id'],
                        'major_name': bookmark['major_name'],
                        'university_name': None,
                        'admission_type': None,
                        'user_grade': user_overall_grade,
                        'cutoff_90': None,
                        'is_eligible': None,
                        'grade_difference': None,
                        'status': '학교 정보 없음'
                    }
                    
                    comparison_results.append(result)
            
            return comparison_results
            
        except Exception as e:
            print(f"등급 비교 중 오류 발생: {e}")
            return []
    
    def get_user_grade_summary(self, user: User) -> Dict:
        """
        유저의 교과 성적 요약 정보를 제공합니다.
        
        Args:
            user: User 객체
            
        Returns:
            Dict: 교과 성적 요약 정보
        """
        try:
            # 과목별 평균등급
            subject_averages = self.calculate_user_subject_average_grade(user)
            
            # 전체 평균등급
            overall_average = self.calculate_user_overall_average_grade(user)
            
            # 전체 과목 수
            total_subjects = len(subject_averages)
            
            # 등급별 분포 계산
            grade_distribution = {}
            for subject, grade in subject_averages.items():
                grade_key = f"{int(grade)}등급"
                grade_distribution[grade_key] = grade_distribution.get(grade_key, 0) + 1
            
            summary = {
                'uid': user.uid,
                'overall_average_grade': overall_average,
                'total_subjects': total_subjects,
                'subject_averages': subject_averages,
                'grade_distribution': grade_distribution
            }
            
            return summary
            
        except Exception as e:
            print(f"교과 성적 요약 생성 중 오류 발생: {e}")
            return {}
    
    def get_bookmark_cutoff_summary(self, user: User) -> Dict:
        """
        유저의 관심 학과-학교별 합격 등급컷 요약을 제공합니다.
        
        Args:
            user: User 객체
            admission_cutoffs: 학과-학교별 합격 등급컷 정보
            
        Returns:
            Dict: 합격 등급컷 요약 정보
        """
        try:
            bookmarks = self.get_user_major_bookmarks_info(user)
            
            # 전역 데이터베이스에서 직접 조회
            univ_ids = [b['univ_id'] for b in bookmarks if b['univ_id']]
            major_ids = [b['major_id'] for b in bookmarks if b['major_id']]
            admission_cutoffs = self.get_admission_score_cutoffs_from_db(univ_ids, major_ids)
            
            cutoff_summary = {
                'total_bookmarks': len(bookmarks),
                'university_major_bookmarks': 0,
                'major_only_bookmarks': 0,
                'bookmarks_with_cutoffs': 0,
                'bookmark_details': []
            }
            
            for bookmark in bookmarks:
                bookmark_detail = {
                    'id': bookmark['id'],
                    'major_name': bookmark['major_name'],
                    'university_name': bookmark['university_name'],
                    'has_university': bookmark['univ_id'] is not None
                }
                
                if bookmark['univ_id']:
                    cutoff_summary['university_major_bookmarks'] += 1
                    
                    # 합격 등급컷 조회
                    cutoff_key = (bookmark['univ_id'], bookmark['major_id'])
                    cutoffs = admission_cutoffs.get(cutoff_key, {})
                    if cutoffs:
                        # 유효한 등급컷만 필터링
                        valid_cutoffs = self.get_valid_cutoffs_only(cutoffs)
                        
                        if valid_cutoffs:
                            cutoff_summary['bookmarks_with_cutoffs'] += 1
                            bookmark_detail['cutoffs'] = valid_cutoffs
                        else:
                            bookmark_detail['cutoffs'] = {}
                    else:
                        bookmark_detail['cutoffs'] = {}
                else:
                    cutoff_summary['major_only_bookmarks'] += 1
                    bookmark_detail['cutoffs'] = {}
                
                cutoff_summary['bookmark_details'].append(bookmark_detail)
            
            return cutoff_summary
            
        except Exception as e:
            print(f"북마크 합격 등급컷 요약 생성 중 오류 발생: {e}")
            return {}
    
    def validate_grade_cutoff(self, cutoff_value: float) -> bool:
        """
        등급컷 값이 유효한지 검증합니다.
        
        Args:
            cutoff_value: 검증할 등급컷 값
            
        Returns:
            bool: 유효한 등급컷이면 True, 아니면 False
        """
        if cutoff_value is None:
            return False
        
        # 0등급은 유효하지 않음 (실제로는 1등급부터 시작)
        if cutoff_value <= 0:
            return False
        
        # 일반적으로 9등급까지 존재 (실제로는 더 높을 수 있음)
        if cutoff_value > 9:
            return False
        
        return True
    
    def get_valid_cutoffs_only(self, cutoffs: Dict) -> Dict:
        """
        등급컷 데이터에서 유효한 값만 필터링합니다.
        
        Args:
            cutoffs: 원본 등급컷 데이터
            
        Returns:
            Dict: 유효한 등급컷만 포함된 데이터
        """
        valid_cutoffs = {}
        
        for admission_type, cutoff_data in cutoffs.items():
            valid_cutoff_data = {}
            
            for key, value in cutoff_data.items():
                if self.validate_grade_cutoff(value):
                    valid_cutoff_data[key] = value
            
            if valid_cutoff_data:  # 유효한 등급컷이 하나라도 있으면
                valid_cutoffs[admission_type] = valid_cutoff_data
        
        return valid_cutoffs
    
    def get_user_info(self, user: User) -> Dict:
        """
        유저의 기본 정보를 조회합니다.
        
        Args:
            user: User 객체
            
        Returns:
            Dict: 유저 기본 정보
        """
        try:
            return {
                'uid': user.uid,
                'name': getattr(user, 'name', None),
                'email': getattr(user, 'email', None),
                'grade_num': getattr(user, 'gradeNum', None),
                'sex': getattr(user, 'sex', None)
            }
                    
        except Exception as e:
            print(f"유저 정보 조회 중 오류 발생: {e}")
            return {}
    
    def get_comprehensive_user_analysis(self, user: User) -> Dict:
        """
        유저의 종합적인 분석 정보를 제공합니다.
        
        Args:
            user: User 객체
            admission_cutoffs: 학과-학교별 합격 등급컷 정보
            
        Returns:
            Dict: 유저 종합 분석 정보
        """
        try:
            # 유저 기본 정보
            user_info = self.get_user_info(user)
            
            # 교과 성적 요약
            grade_summary = self.get_user_grade_summary(user)
            
            # 북마크 합격 등급컷 요약
            bookmark_summary = self.get_bookmark_cutoff_summary(user)
            
            # 등급 비교 결과
            comparison_results = self.compare_user_grade_with_cutoffs(user)
            
            # 진학 방향별 학과-학교 수 계산
            down_count = sum(1 for result in comparison_results 
                           if result.get('admission_direction') == '하향')
            appropriate_count = sum(1 for result in comparison_results 
                                  if result.get('admission_direction') == '적정')
            up_count = sum(1 for result in comparison_results 
                          if result.get('admission_direction') == '상향')
            error_count = sum(1 for result in comparison_results 
                            if result.get('admission_direction') is None)
            
            comprehensive_analysis = {
                'user_info': user_info,
                'grade_analysis': grade_summary,
                'bookmark_analysis': bookmark_summary,
                'comparison_analysis': {
                    'total_comparisons': len(comparison_results),
                    'down_count': down_count,
                    'appropriate_count': appropriate_count,
                    'up_count': up_count,
                    'error_count': error_count,
                    'comparison_results': comparison_results
                },
                'recommendations': self._generate_recommendations(grade_summary, comparison_results)
            }
            
            return comprehensive_analysis
            
        except Exception as e:
            print(f"유저 종합 분석 중 오류 발생: {e}")
            return {}
    
    def _generate_recommendations(self, grade_summary: Dict, comparison_results: List[Dict]) -> List[str]:
        """
        유저의 성적과 비교 결과를 바탕으로 추천사항을 생성합니다.
        
        Args:
            grade_summary: 교과 성적 요약
            comparison_results: 등급 비교 결과
            
        Returns:
            List[str]: 추천사항 리스트
        """
        recommendations = []
        
        try:
            overall_grade = grade_summary.get('overall_average_grade', 0)
            
            # 전체 성적 기반 추천
            if overall_grade <= 2.0:
                recommendations.append("전체적으로 우수한 성적입니다. 상위권 대학 지원을 고려해보세요.")
            elif overall_grade <= 3.0:
                recommendations.append("양호한 성적입니다. 목표 대학의 합격 가능성을 높이기 위해 추가 학습이 필요합니다.")
            elif overall_grade <= 4.0:
                recommendations.append("보통 성적입니다. 더 높은 등급을 목표로 학습 계획을 세워보세요.")
            else:
                recommendations.append("성적 향상이 필요합니다. 기초 과목부터 차근차근 학습해보세요.")
            
            # 진학 방향 기반 추천
            down_count = sum(1 for result in comparison_results 
                           if result.get('admission_direction') == '하향')
            appropriate_count = sum(1 for result in comparison_results 
                                  if result.get('admission_direction') == '적정')
            up_count = sum(1 for result in comparison_results 
                          if result.get('admission_direction') == '상향')
            
            if down_count > 0:
                recommendations.append(f"{down_count}개의 학과-학교에 하향 지원이 가능합니다. 안정적인 합격을 노려보세요.")
            
            if appropriate_count > 0:
                recommendations.append(f"{appropriate_count}개의 학과-학교에 적정 지원이 가능합니다. 적절한 도전을 해보세요.")
            
            if up_count > 0:
                recommendations.append(f"{up_count}개의 학과-학교에 상향 지원이 필요합니다. 성적 향상을 통해 합격 가능성을 높여보세요.")
            
            if down_count == 0 and appropriate_count == 0:
                recommendations.append("현재 성적으로는 합격 가능한 학과-학교가 없습니다. 성적 향상이 필요합니다.")
            
            # 과목별 성적 기반 추천
            subject_averages = grade_summary.get('subject_averages', {})
            weak_subjects = [subject for subject, grade in subject_averages.items() if grade > 3.0]
            
            if weak_subjects:
                recommendations.append(f"다음 과목들의 성적 향상이 필요합니다: {', '.join(weak_subjects)}")
            
            return recommendations
            
        except Exception as e:
            print(f"추천사항 생성 중 오류 발생: {e}")
            return ["추천사항을 생성할 수 없습니다."]
    
    def get_user_reports_by_term(self, user: User, term: int) -> List[Report]:
        """
        특정 학기의 유저 성적표를 조회합니다.
        
        Args:
            user: User 객체
            term: 학기 (1, 2, 3)
            
        Returns:
            List[Report]: 해당 학기의 성적표 리스트
        """
        try:
            return [report for report in user.reports if report.term == term]
        except Exception as e:
            print(f"학기별 성적표 조회 중 오류 발생: {e}")
            return []
    
    def get_user_reports_by_grade(self, user: User, grade: int) -> List[Report]:
        """
        특정 학년의 유저 성적표를 조회합니다.
        
        Args:
            user: User 객체
            grade: 학년 (1, 2, 3)
            
        Returns:
            List[Report]: 해당 학년의 성적표 리스트
        """
        try:
            return [report for report in user.reports if report.userGrade == grade]
        except Exception as e:
            print(f"학년별 성적표 조회 중 오류 발생: {e}")
            return []
    
    def get_user_category_grades(self, user: User) -> Dict[str, float]:
        """
        유저의 과목 카테고리별 평균 등급을 계산합니다.
        
        Args:
            user: User 객체
            
        Returns:
            Dict[str, float]: 과목 카테고리별 평균 등급
        """
        try:
            if not user.reports:
                return {}
            
            category_grades = {}
            category_counts = {}
            
            for report in user.reports:
                if report.categoryGrade is not None:
                    category_name = report.categoryName.name if hasattr(report.categoryName, 'name') else str(report.categoryName)
                    
                    if category_name not in category_grades:
                        category_grades[category_name] = 0
                        category_counts[category_name] = 0
                    
                    category_grades[category_name] += float(report.categoryGrade)
                    category_counts[category_name] += 1
            
            # 평균 계산
            category_averages = {}
            for category, total in category_grades.items():
                if category_counts[category] > 0:
                    category_averages[category] = round(total / category_counts[category], 2)
            
            return category_averages
            
        except Exception as e:
            print(f"과목 카테고리별 등급 계산 중 오류 발생: {e}")
            return {}
