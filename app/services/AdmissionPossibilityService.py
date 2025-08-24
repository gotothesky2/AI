from typing import List, Dict, Optional
from domain.User import User
from domain.MajorBookmark import MajorBookmark
from domain.AdmissionScore import AdmissionScore
from repository.majorBookmarkRepository import majorBookmarkRepository
from repository.userRepository import userRepository
from util.Transactional import Transactional
from util.globalDB.global_db import get_global_db

class AdmissionPossibilityService:
    """
    사용자의 대학 학과 북마크에 대한 합격가능성을 분석하는 서비스
    """
    
    def __init__(self):
        pass
    
    @Transactional
    def getUserAdmissionPossibility(self, uid: str) -> Dict:
        """
        사용자의 북마크된 학과-학교에 대한 합격가능성을 분석합니다.
        
        Args:
            uid: 사용자 ID
            
        Returns:
            Dict: 합격가능성 분석 결과
        """
        try:
            # 사용자 정보 조회
            user = userRepository.getById(uid)
            if not user:
                return {"error": "사용자를 찾을 수 없습니다."}
            
            # 대학교와 학과 정보가 모두 있는 북마크만 조회
            bookmarks = majorBookmarkRepository.getByUserIdWithUniversityAndMajor(uid)
            if not bookmarks:
                return {
                    "message": "등록된 대학-학과 북마크가 없습니다.",
                    "uid": uid,
                    "bookmarks": [],
                    "analysis": None
                }
            
            # 합격가능성 분석
            analysis_result = self._analyzeAdmissionPossibility(user, bookmarks)
            
            bookmark_results = []
            for bookmark in bookmarks:
                analysis = self._analyzeSingleBookmark(user, bookmark)
                
                bookmark_results.append({
                    "name": f"{bookmark.major.name}-{bookmark.university.name}",
                    "percent": -1 if analysis.get("level") == "unknown" else (100 if analysis.get("level") == "high" else (70 if analysis.get("level") == "medium" else 30)),
                    "grade_diff": analysis.get("diff"),
                    "user_grade": analysis.get("user_grade", 0),
                    "cutoff_grade": analysis.get("cutoff_90")
                })
            
            return {
                "user_grade": analysis_result.get("user_overall_grade"),
                "bookmarks": len(bookmarks),
                "bookmark_results": bookmark_results
            }
            
        except Exception as e:
            return {"error": f"합격가능성 분석 중 오류가 발생했습니다: {str(e)}"}
    
    @Transactional
    def getSpecificBookmarkPossibility(self, uid: str, bookmark_id: int) -> Dict:
        """
        특정 북마크에 대한 합격가능성을 분석합니다.
        
        Args:
            uid: 사용자 ID
            bookmark_id: 북마크 ID
            
        Returns:
            Dict: 특정 북마크의 합격가능성 분석 결과
        """
        try:
            # 사용자 정보 조회
            user = userRepository.getById(uid)
            if not user:
                return {"error": "사용자를 찾을 수 없습니다."}
            
            # 특정 북마크 조회
            bookmark = majorBookmarkRepository.getById(bookmark_id)
            if not bookmark or bookmark.uid != uid:
                return {"error": "북마크를 찾을 수 없거나 접근 권한이 없습니다."}
            
            if not bookmark.univId or not bookmark.major_id:
                return {"error": "대학교 또는 학과 정보가 없는 북마크입니다."}
            
            # 해당 북마크만 분석
            analysis_result = self._analyzeSingleBookmark(user, bookmark)
            
            return {
                "uid": uid,
                "bookmark_id": bookmark_id,
                "bookmark": self._formatSingleBookmark(bookmark),
                "analysis": analysis_result
            }
            
        except Exception as e:
            return {"error": f"북마크 분석 중 오류가 발생했습니다: {str(e)}"}
    
    def _analyzeAdmissionPossibility(self, user: User, bookmarks: List[MajorBookmark]) -> Dict:
        """북마크 목록에 대한 합격가능성을 종합 분석합니다."""
        try:
            # 사용자 전체 평균 등급 (임시로 고정값 사용)
            user_overall_grade = 3.0  # 실제로는 성적 데이터에서 계산해야 함
            
            # 각 북마크별 분석 결과
            bookmark_analyses = []
            total_possibility = {
                "high": 0,      # 높음 (하향 지원)
                "medium": 0,    # 보통 (적정 지원)
                "low": 0,       # 낮음 (상향 지원)
                "unknown": 0    # 알 수 없음
            }
            
            for bookmark in bookmarks:
                analysis = self._analyzeSingleBookmark(user, bookmark)
                bookmark_analyses.append(analysis)
                
                            # 합격가능성 분류
            if analysis.get("level") == "high":
                total_possibility["high"] += 1
            elif analysis.get("level") == "medium":
                total_possibility["medium"] += 1
            elif analysis.get("level") == "low":
                total_possibility["low"] += 1
            else:
                total_possibility["unknown"] += 1
            
            return {
                "user_overall_grade": user_overall_grade,
                "total_bookmarks": len(bookmarks),
                "total_possibility": total_possibility,
                "bookmark_analyses": bookmark_analyses,
                "summary": self._generateSummary(total_possibility, user_overall_grade)
            }
            
        except Exception as e:
            return {"error": f"종합 분석 중 오류 발생: {str(e)}"}
    
    def _analyzeSingleBookmark(self, user: User, bookmark: MajorBookmark) -> Dict:
        """단일 북마크에 대한 합격가능성을 분석합니다."""
        try:
            # 사용자 전체 평균 등급 (임시로 고정값 사용)
            user_overall_grade = 3.0  # 실제로는 성적 데이터에서 계산해야 함
            
            # 합격 등급컷 조회
            admission_scores = self._getAdmissionScores(bookmark.univId, bookmark.major_id)
            
            if not admission_scores:
                return {
                    "possibility_level": "unknown",
                    "reason": "합격 등급컷 데이터가 없습니다.",
                    "user_grade": user_overall_grade,
                    "cutoff_data": None
                }
            
            # 가장 낮은 90% 합격 등급컷 찾기 (가장 엄격한 기준)
            best_cutoff = None
            best_admission_type = None
            
            for score in admission_scores:
                if score.cutNinety and score.cutNinety > 0:
                    if best_cutoff is None or score.cutNinety < best_cutoff:
                        best_cutoff = score.cutNinety
                        best_admission_type = score.admissionType
            
            if best_cutoff is None:
                return {
                    "possibility_level": "unknown",
                    "reason": "유효한 90% 합격 등급컷이 없습니다.",
                    "user_grade": user_overall_grade,
                    "cutoff_data": None
                }
            
            # 등급 비교 및 합격가능성 판단
            grade_difference = best_cutoff - user_overall_grade
            
            if grade_difference >= 0.5:
                possibility_level = "high"
                reason = "하향 지원 가능 - 안정적인 합격"
            elif grade_difference >= 0:
                possibility_level = "medium"
                reason = "적정 지원 - 적절한 도전"
            else:
                possibility_level = "low"
                reason = "상향 지원 - 성적 향상 필요"
            
            return {
                "level": possibility_level,  # high/medium/low
                "diff": round(grade_difference, 2),  # 등급 차이
                "user_grade": user_overall_grade,
                "cutoff_90": best_cutoff
            }
            
        except Exception as e:
            return {"error": f"북마크 분석 중 오류 발생: {str(e)}"}
    
    def _getAdmissionScores(self, univ_id: int, major_id: int) -> List[AdmissionScore]:
        """특정 대학교-학과의 합격 등급컷을 조회합니다."""
        try:
            db_session = get_global_db()
            if not db_session:
                return []
            
            return (db_session.query(AdmissionScore)
                    .filter(AdmissionScore.univId == univ_id)
                    .filter(AdmissionScore.majorId == major_id)
                    .all())
                    
        except Exception as e:
            print(f"합격 등급컷 조회 중 오류: {e}")
            return []
    
    def _formatAdmissionScores(self, scores: List[AdmissionScore]) -> List[Dict]:
        """합격 등급컷 데이터를 포맷팅합니다."""
        formatted = []
        for score in scores:
            formatted.append({
                "admission_type": score.admissionType,
                "cut_50": score.cutFifty,
                "cut_70": score.cutSeventy,
                "cut_90": score.cutNinety
            })
        return formatted
    
    def _formatBookmarks(self, bookmarks: List[MajorBookmark]) -> List[Dict]:
        """북마크 목록을 포맷팅합니다."""
        formatted = []
        for bookmark in bookmarks:
            formatted.append({
                "id": bookmark.id,
                "major_id": bookmark.major_id,
                "univ_id": bookmark.univId,
                "major_name": bookmark.major.name if bookmark.major else None,
                "university_name": bookmark.university.name if bookmark.university else None
            })
        return formatted
    
    def _formatSingleBookmark(self, bookmark: MajorBookmark) -> Dict:
        """단일 북마크를 포맷팅합니다."""
        return {
            "id": bookmark.id,
            "major_id": bookmark.major_id,
            "univ_id": bookmark.univId,
            "major_name": bookmark.major.name if bookmark.major else None,
            "university_name": bookmark.university.name if bookmark.university else None
        }
    
    def _getUserBasicInfo(self, user: User) -> Dict:
        """사용자 기본 정보를 추출합니다."""
        return {
            "uid": user.uid,
            "name": getattr(user, 'name', None),
            "email": getattr(user, 'email', None),
            "grade_num": getattr(user, 'gradeNum', None)
        }
    
    def _generateSummary(self, total_possibility: Dict, user_grade: float) -> Dict:
        """합격가능성 요약을 생성합니다."""
        total = sum(total_possibility.values())
        
        if total == 0:
            return {"message": "분석할 북마크가 없습니다."}
        
        # 합격가능성 비율 계산
        high_ratio = round((total_possibility["high"] / total) * 100, 1)
        medium_ratio = round((total_possibility["medium"] / total) * 100, 1)
        low_ratio = round((total_possibility["low"] / total) * 100, 1)
        
        # 전체적인 평가
        if high_ratio >= 50:
            overall_assessment = "전체적으로 합격 가능성이 높습니다."
        elif medium_ratio >= 50:
            overall_assessment = "전체적으로 적정한 수준의 합격 가능성을 보입니다."
        elif low_ratio >= 50:
            overall_assessment = "전체적으로 합격 가능성이 낮습니다. 성적 향상이 필요합니다."
        else:
            overall_assessment = "다양한 수준의 합격 가능성을 보입니다."
        
        return {
            "total_bookmarks": total,
            "high_possibility": {
                "count": total_possibility["high"],
                "ratio": high_ratio
            },
            "medium_possibility": {
                "count": total_possibility["medium"],
                "ratio": medium_ratio
            },
            "low_possibility": {
                "count": total_possibility["low"],
                "ratio": low_ratio
            },
            "unknown": total_possibility["unknown"],
            "overall_assessment": overall_assessment,
            "user_grade": user_grade
        }

admissionPossibilityService = AdmissionPossibilityService()
