from difflib import SequenceMatcher
import re
from typing import List, Tuple, Optional

class SimilarityChecker:
    def __init__(self):
        # 대학교명 매칭을 위한 별칭 사전
        self.university_aliases = {
            "고려대학교": ["고려대", "고대"],
            "고려대학교 세종캠퍼스": ["고려대(세종)", "고려대세종", "고대세종", "고려대 세종"],
            "연세대학교": ["연세대", "연대"],
            "연세대학교 원주캠퍼스": ["연세대(원주)", "연세대원주", "연대원주"],
            "한양대학교": ["한양대", "한대"],
            "한양대학교 ERICA캠퍼스": ["한양대(ERICA)", "한양대ERICA", "한대ERICA"],
            "경희대학교": ["경희대", "경대"],
            "경희대학교 국제캠퍼스": ["경희대(국제)", "경희대국제", "경대국제"],
            "중앙대학교": ["중앙대", "중대"],
            "중앙대학교 안성캠퍼스": ["중앙대(안성)", "중앙대안성", "중대안성"],
            "한국항공대학교": ["한국항공대", "항공대", "한항대"]
        }
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """두 문자열의 유사도를 계산합니다 (0.0 ~ 1.0)"""
        if not str1 or not str2:
            return 0.0
        
        # 정규화: 공백 제거만 (한국어는 소문자 변환 불필요)
        str1 = self._normalize_string(str1)
        str2 = self._normalize_string(str2)
        
        # SequenceMatcher를 사용한 유사도 계산
        similarity = SequenceMatcher(None, str1, str2).ratio()
        return similarity
    
    def _normalize_string(self, text: str) -> str:
        """문자열을 정규화합니다. (한국어에 최적화)"""
        if not text:
            return ""
        
        # 공백 제거만 (한국어는 소문자 변환 불필요)
        normalized = re.sub(r'\s+', '', text)
        return normalized
    
    def find_university_match(self, target_university: str, all_universities: List[str], 
                            threshold: float = 0.7) -> Optional[Tuple[str, float, str]]:
        """대학교명을 매칭합니다. (별칭, 캠퍼스명 등 고려)"""
        if not all_universities:
            return None
        
        # 1. 정확한 매칭 시도
        exact_match = self.find_best_match(target_university, all_universities, 0.95)
        if exact_match:
            return (exact_match[0], exact_match[1], "exact")
        
        # 2. 별칭을 통한 매칭 시도
        alias_match = self._find_by_alias(target_university, all_universities)
        if alias_match:
            return alias_match
        
        # 3. 퍼지 매칭 시도
        fuzzy_match = self.find_best_match(target_university, all_universities, threshold)
        if fuzzy_match:
            return (fuzzy_match[0], fuzzy_match[1], "fuzzy")
        
        # 4. 유사한 후보들 찾기
        similar_candidates = self._find_similar_universities(target_university, all_universities, 0.5)
        if similar_candidates:
            return (similar_candidates[0][0], similar_candidates[0][1], "candidate")
        
        return None
    
    def _find_by_alias(self, target: str, all_universities: List[str]) -> Optional[Tuple[str, float, str]]:
        """별칭을 통해 대학교를 찾습니다."""
        normalized_target = self._normalize_string(target)
        
        for official_name, aliases in self.university_aliases.items():
            # 공식명과 직접 비교
            if self._normalize_string(official_name) == normalized_target:
                if official_name in all_universities:
                    return (official_name, 1.0, "exact")
            
            # 별칭과 비교
            for alias in aliases:
                if self._normalize_string(alias) == normalized_target:
                    if official_name in all_universities:
                        return (official_name, 0.9, "alias")
        
        return None
    
    def _find_similar_universities(self, target: str, all_universities: List[str], 
                                 threshold: float) -> List[Tuple[str, float]]:
        """대학교명과 유사한 모든 대학교를 찾습니다."""
        similar_universities = []
        
        for university in all_universities:
            similarity = self.calculate_similarity(target, university)
            if similarity >= threshold:
                similar_universities.append((university, similarity))
        
        # 유사도 순으로 정렬
        similar_universities.sort(key=lambda x: x[1], reverse=True)
        return similar_universities
    
    def find_best_match(self, target: str, candidates: List[str], threshold: float = 0.8) -> Optional[Tuple[str, float]]:
        """후보 목록에서 가장 유사한 문자열을 찾습니다."""
        if not candidates:
            return None
        
        best_match = None
        best_similarity = 0.0
        
        for candidate in candidates:
            similarity = self.calculate_similarity(target, candidate)
            if similarity > best_similarity and similarity >= threshold:
                best_similarity = similarity
                best_match = candidate
        
        if best_match:
            return (best_match, best_similarity)
        return None
    
    def find_similar_majors(self, target_major: str, all_majors: List[str], threshold: float = 0.7) -> List[Tuple[str, float]]:
        """학과명과 유사한 모든 학과를 찾습니다."""
        similar_majors = []
        
        for major in all_majors:
            similarity = self.calculate_similarity(target_major, major)
            if similarity >= threshold:
                similar_majors.append((major, similarity))
        
        # 유사도 순으로 정렬
        similar_majors.sort(key=lambda x: x[1], reverse=True)
        return similar_majors
    
    def fuzzy_match_major(self, target_major: str, all_majors: List[str], 
                         strict_threshold: float = 0.9, 
                         fuzzy_threshold: float = 0.7) -> Optional[Tuple[str, float, str]]:
        """학과명을 퍼지 매칭으로 찾습니다."""
        # 1. 정확한 매칭 시도
        exact_match = self.find_best_match(target_major, all_majors, strict_threshold)
        if exact_match:
            return (exact_match[0], exact_match[1], "exact")
        
        # 2. 퍼지 매칭 시도
        fuzzy_match = self.find_best_match(target_major, all_majors, fuzzy_threshold)
        if fuzzy_match:
            return (fuzzy_match[0], fuzzy_match[1], "fuzzy")
        
        # 3. 유사한 후보들 반환 (매칭 실패 시)
        similar_candidates = self.find_similar_majors(target_major, all_majors, 0.5)
        if similar_candidates:
            return (similar_candidates[0][0], similar_candidates[0][1], "candidate")
        
        return None

# 전역 인스턴스
similarityChecker = SimilarityChecker()
