from repository.admissionScoreRepository import admissionScoreRepository
from repository.universityRepository import universityRepository
from repository.majorRepository import majorRepository
from util.Transactional import Transactional
from util.similarity_checker import similarityChecker
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional

class ExcelMappingService:
    def __init__(self):
        self.admissionScoreRepo = admissionScoreRepository
        self.universityRepo = universityRepository
        self.majorRepo = majorRepository
        self.similarityChecker = similarityChecker

    @Transactional
    def mapCSVToAdmissionScore(self, csv_file_path: str, 
                               strict_threshold: float = 0.9,
                               fuzzy_threshold: float = 0.7) -> Dict[str, Any]:
        """CSV 파일의 성적 데이터를 AdmissionScore 테이블에 매핑합니다."""
        try:
            # CSV 파일 읽기 (한국어 인코딩 지원)
            df = pd.read_csv(csv_file_path, encoding='utf-8')
            
            # 컬럼명이 없는 경우 기본 컬럼명 사용 (DB 컬럼 스네이크 케이스로 정규화)
            if len(df.columns) >= 6:
                df.columns = [
                    'university',          # 대학명
                    'admission_type',      # 전형명
                    'major',               # 학과명
                    'cut_fifty',           # 50% 컷
                    'cut_seventy',         # 70% 컷
                    'cut_ninety',          # 90% 컷
                    *[f'extra_{i}' for i in range(len(df.columns) - 6)]
                ]
            elif len(df.columns) == 5:
                df.columns = [
                    'university', 'admission_type', 'major', 'cut_fifty', 'cut_seventy'
                ]
            elif len(df.columns) == 4:
                df.columns = [
                    'university', 'admission_type', 'major', 'cut_fifty'
                ]
            
            mapped_count = 0
            errors = []
            warnings = []
            mapping_details = []
            
            # 각 행 처리
            for index, row in df.iterrows():
                try:
                    # 대학교명으로 대학교 찾기 (유사도 검사 포함)
                    excel_university_name = row.iloc[0]  # 첫 번째 컬럼: 대학교명
                    university = self._findUniversityWithSimilarity(excel_university_name)
                    
                    if not university:
                        errors.append(f"행 {index+1}: 대학교 '{excel_university_name}'을 찾을 수 없습니다.")
                        continue
                    
                    # 학과명으로 학과 찾기 (유사도 검사 포함)
                    target_major_name = row.iloc[2]  # 세 번째 컬럼: 학과명
                    all_majors = self._getAllMajorNames()
                    major_match = self._findMajorWithSimilarity(target_major_name, all_majors, 
                                                             strict_threshold, fuzzy_threshold)
                    
                    if not major_match:
                        errors.append(f"행 {index+1}: 학과 '{target_major_name}'을 찾을 수 없습니다.")
                        continue
                    
                    major, similarity, match_type = major_match
                    
                    # 매칭 결과 기록
                    mapping_details.append({
                        'row': index + 1,
                        'excel_university': excel_university_name,
                        'matched_university': university.name,
                        'excel_major': target_major_name,
                        'matched_major': major.name,
                        'similarity': similarity,
                        'match_type': match_type
                    })
                    
                    # 경고 메시지 (퍼지 매칭인 경우)
                    if match_type == "fuzzy":
                        warnings.append(f"행 {index+1}: '{target_major_name}' → '{major.name}' (유사도: {similarity:.2f})")
                    
                    # 성적 데이터 추출 및 보정 (float 파싱 + 결측치 보간)
                    def _to_float(v):
                        try:
                            if pd.isna(v):
                                return None
                            s = str(v).strip()
                            if s == '':
                                return None
                            return float(s)
                        except Exception:
                            return None
                    
                    cf = _to_float(row.iloc[3]) if len(row) > 3 else None  # cut_fifty
                    cs = _to_float(row.iloc[4]) if len(row) > 4 else None  # cut_seventy
                    cn = _to_float(row.iloc[5]) if len(row) > 5 else None  # cut_ninety

                    # 결측치 보정: DB NOT NULL 대응
                    if cf is None:
                        cf = 0.0
                    if cs is None:
                        cs = cf if cf is not None else 0.0
                    if cn is None:
                        cn = cs if cs is not None else (cf if cf is not None else 0.0)

                    score_data = {
                        'admissionType': (row.iloc[1] if pd.notna(row.iloc[1]) else '기타전형'),
                        'cutFifty': cf,
                        'cutSeventy': cs,
                        'cutNinety': cn,
                    }
                    
                    # AdmissionScore 테이블에 저장 (자동으로 업데이트 또는 생성)
                    self.admissionScoreRepo.updateOrCreate(
                        university.id, major.id, **score_data
                    )
                    
                    mapped_count += 1
                    
                except Exception as e:
                    errors.append(f"행 {index+1}: {str(e)}")
            
            return {
                "success": True,
                "mapped_count": mapped_count,
                "total_rows": len(df),
                "errors": errors,
                "warnings": warnings,
                "mapping_details": mapping_details,
                "message": f"{mapped_count}개의 성적 데이터를 성공적으로 매핑했습니다."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "CSV 파일 처리 중 오류가 발생했습니다."
            }

    def _findUniversityWithSimilarity(self, target_university_name: str):
        """유사도 검사를 통해 대학교를 찾습니다."""
        # 모든 대학교명 가져오기
        all_universities = self._getAllUniversityNames()
        
        # 유사도 검사를 통한 매칭
        university_match = self.similarityChecker.find_university_match(
            target_university_name, all_universities
        )
        
        if university_match:
            matched_name, similarity, match_type = university_match
            university = self._getUniversityByName(matched_name)
            
            # 경고 메시지 (별칭 매칭인 경우)
            if match_type == "alias":
                print(f"⚠️ 대학교명 별칭 매칭: '{target_university_name}' → '{matched_name}' (유사도: {similarity:.2f})")
            
            return university
        
        return None

    def _findMajorWithSimilarity(self, target_major_name: str, all_majors: List[str],
                                strict_threshold: float, fuzzy_threshold: float) -> Optional[Tuple[Any, float, str]]:
        """유사도 검사를 통해 학과를 찾습니다."""
        # 1. 정확한 매칭 시도
        exact_match = self.similarityChecker.find_best_match(target_major_name, all_majors, strict_threshold)
        if exact_match:
            matched_name, similarity = exact_match
            major = self._getMajorByName(matched_name)
            if major:
                return (major, similarity, "exact")
        
        # 2. 퍼지 매칭 시도
        fuzzy_match = self.similarityChecker.find_best_match(target_major_name, all_majors, fuzzy_threshold)
        if fuzzy_match:
            matched_name, similarity = fuzzy_match
            major = self._getMajorByName(matched_name)
            if major:
                return (major, similarity, "fuzzy")
        
        # 3. 유사한 후보들 찾기
        similar_candidates = self.similarityChecker.find_similar_majors(target_major_name, all_majors, 0.5)
        if similar_candidates:
            best_candidate, similarity = similar_candidates[0]
            major = self._getMajorByName(best_candidate)
            if major:
                return (major, similarity, "candidate")
        
        return None

    def _getAllUniversityNames(self) -> List[str]:
        """데이터베이스의 모든 대학교명을 가져옵니다."""
        universities = self.universityRepo.getAll()
        return [univ.name for univ in universities]

    def _getAllMajorNames(self) -> List[str]:
        """데이터베이스의 모든 학과명을 가져옵니다."""
        majors = self.majorRepo.getAll()
        return [major.name for major in majors]

    def _getUniversityByName(self, university_name: str):
        """대학교명으로 대학교를 조회합니다."""
        universities = self.universityRepo.getAll()
        for univ in universities:
            if univ.name == university_name:
                return univ
        return None

    def _getMajorByName(self, major_name: str):
        """학과명으로 학과를 조회합니다."""
        # 기존 학과 조회
        majors = self.majorRepo.getAll()
        for major in majors:
            if major.name == major_name:
                return major
        
        # 임시 매핑 (실제로는 데이터베이스에서 조회해야 함)
        major_mapping = {
            "도시계획학과": type('obj', (object,), {'id': 1, 'name': major_name}),
            "디지털콘텐츠학과": type('obj', (object,), {'id': 2, 'name': major_name}),
            "물리치료학과": type('obj', (object,), {'id': 3, 'name': major_name}),
            "한의예과": type('obj', (object,), {'id': 4, 'name': major_name}),
            "간호학과": type('obj', (object,), {'id': 5, 'name': major_name}),
            "컴퓨터공학과": type('obj', (object,), {'id': 6, 'name': major_name}),
            "AI학과": type('obj', (object,), {'id': 7, 'name': major_name})
        }
        
        return major_mapping.get(major_name)

excelMappingService = ExcelMappingService()
