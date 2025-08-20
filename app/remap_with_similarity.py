#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sqlalchemy import text
from db import SessionLocal
from util.similarity_checker import similarityChecker

def standardize_university_name(name):
    """대학교명을 표준화합니다."""
    if not name:
        return name
    
    # "대"로 끝나고 "대학교"로 끝나지 않는 경우 "학교" 추가
    if name.endswith('대') and not name.endswith('대학교'):
        return name + '학교'
    
    return name

def main():
    session = SessionLocal()
    try:
        print("=== university_major 기준으로 유사도 기반 재매핑 시작 (학교 0.8, 학과 0.6)... ===")
        
        # 1. 기존 admission_score 데이터 삭제
        print("1. 기존 admission_score 데이터 삭제 중...")
        session.execute(text("DELETE FROM admission_score"))
        session.commit()
        print("   기존 데이터 삭제 완료")
        
        # 2. university_major 테이블에서 모든 조합 조회
        print("2. university_major 테이블 조합 조회 중...")
        um_query = text("""
            SELECT um.univ_id, um.m_id, u.univ_name, m.m_name
            FROM university_major um
            JOIN university u ON um.univ_id = u.univ_id
            JOIN major m ON um.m_id = m.m_id
            ORDER BY u.univ_name, m.m_name
        """)
        um_result = session.execute(um_query)
        
        um_combinations = []
        for row in um_result:
            um_combinations.append({
                'univ_id': row.univ_id,
                'major_id': row.m_id,
                'univ_name': row.univ_name,
                'major_name': row.m_name
            })
        
        print(f"   총 {len(um_combinations)}개의 university_major 조합 발견")
        
        # 3. CSV 파일 읽기
        print("3. CSV 파일 읽기 중...")
        df = pd.read_csv('domain/교과 데이터.csv', encoding='utf-8', header=None)
        
        # 컬럼명 설정 (헤더가 없으므로 수동으로 설정)
        df.columns = ['university', 'admission_type', 'major', 'cut_fifty', 'cut_seventy', 'cut_ninety']
        
        # CSV 데이터를 미리 읽어서 유사도 계산에 사용 (최적화 + 표준화)
        csv_data = []
        for index, row in df.iterrows():
            excel_univ = row.iloc[0] if pd.notna(row.iloc[0]) else ""
            excel_major = row.iloc[2] if pd.notna(row.iloc[2]) else ""
            excel_admission_type = row.iloc[1] if pd.notna(row.iloc[1]) else "일반전형"
            
            if excel_univ and excel_major:
                # 대학교명 표준화
                standardized_univ = standardize_university_name(excel_univ)
                
                csv_data.append({
                    'row': index + 1,
                    'university': standardized_univ,  # 표준화된 대학교명
                    'original_university': excel_univ,  # 원본 대학교명 (참고용)
                    'major': excel_major,
                    'admission_type': excel_admission_type,
                    'cut_fifty': row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else None,
                    'cut_seventy': row.iloc[4] if len(row) > 4 and pd.notna(row.iloc[4]) else None,
                    'cut_ninety': row.iloc[5] if len(row) > 5 and pd.notna(row.iloc[5]) else None
                })
        
        print(f"   CSV에서 {len(df)}개 행 읽기 완료")
        print(f"   표준화 후 {len(csv_data)}개의 유효한 데이터 발견")
        
        # 표준화 결과 예시 출력
        if csv_data:
            print("   표준화 예시:")
            for i, data in enumerate(csv_data[:5]):
                print(f"     {data['original_university']} → {data['university']} {data['major']}")
            if len(csv_data) > 5:
                print(f"     ... 외 {len(csv_data)-5}개")
        
        # 4. 유사도 기반 매핑 (학교 0.8, 학과 0.6 조건)
        print("4. 유사도 기반 매핑 시작 (학교 0.8, 학과 0.6)...")
        
        mapped_count = 0
        errors = []
        mapping_details = []
        
        # 성능 최적화: 유사도 계산 결과를 캐시
        similarity_cache = {}
        
        # DB의 각 university_major 조합에 대해 CSV에서 가장 유사한 것 찾기
        for i, um_combo in enumerate(um_combinations):
            if i % 100 == 0:
                print(f"   진행률: {i}/{len(um_combinations)} ({i/len(um_combinations)*100:.1f}%)")
            
            best_csv_match = None
            best_total_similarity = 0
            best_univ_similarity = 0
            best_major_similarity = 0
            
            # CSV의 각 행과 유사도 계산 (학교와 학과를 따로 비교)
            for csv_row in csv_data:
                # 캐시 키 생성 (학교와 학과 따로)
                cache_key = (um_combo['univ_name'], um_combo['major_name'], csv_row['university'], csv_row['major'])
                
                if cache_key in similarity_cache:
                    # 캐시된 결과 사용
                    univ_similarity, major_similarity = similarity_cache[cache_key]
                else:
                    # 학교명과 학과명을 따로 비교
                    univ_similarity = similarityChecker.calculate_similarity(csv_row['university'], um_combo['univ_name'])
                    major_similarity = similarityChecker.calculate_similarity(csv_row['major'], um_combo['major_name'])
                    
                    # 캐시에 저장
                    similarity_cache[cache_key] = (univ_similarity, major_similarity)
                
                # 학교 유사도 0.8 이상, 학과 유사도 0.6 이상인 경우만 고려
                if univ_similarity >= 0.8 and major_similarity >= 0.6:
                    # 전체 유사도는 학교와 학과의 가중 평균 (학교를 더 중요하게)
                    total_similarity = (univ_similarity * 0.6) + (major_similarity * 0.4)
                    
                    # 더 높은 유사도를 가진 CSV 행 찾기
                    if total_similarity > best_total_similarity:
                        best_total_similarity = total_similarity
                        best_csv_match = csv_row
                        best_univ_similarity = univ_similarity
                        best_major_similarity = major_similarity
                
                # 부분 문자열 포함 여부도 확인 (유사도가 낮아도 포함되면 매칑)
                elif (csv_row['university'] in um_combo['univ_name'] or 
                      um_combo['univ_name'] in csv_row['university']) and major_similarity >= 0.6:
                    # 부분 문자열 포함 시 높은 유사도 부여
                    partial_univ_similarity = 0.9  # 부분 포함 시 높은 점수
                    total_similarity = (partial_univ_similarity * 0.6) + (major_similarity * 0.4)
                    
                    # 더 높은 유사도를 가진 CSV 행 찾기
                    if total_similarity > best_total_similarity:
                        best_total_similarity = total_similarity
                        best_csv_match = csv_row
                        best_univ_similarity = partial_univ_similarity
                        best_major_similarity = major_similarity
            
            # 조건을 만족하는 매핑이 있는 경우
            if best_csv_match:
                try:
                    # 성적 데이터 추출 및 변환
                    cut_fifty = 0.0
                    cut_seventy = 0.0
                    cut_ninety = 0.0
                    
                    # cut_fifty 처리
                    if best_csv_match['cut_fifty'] is not None:
                        try:
                            cut_fifty = float(str(best_csv_match['cut_fifty']).strip())
                        except:
                            cut_fifty = 0.0
                    
                    # cut_seventy 처리 (cut_fifty 기반)
                    if best_csv_match['cut_seventy'] is not None:
                        try:
                            cut_seventy = float(str(best_csv_match['cut_seventy']).strip())
                        except:
                            cut_seventy = cut_fifty
                    else:
                        cut_seventy = cut_fifty
                    
                    # cut_ninety 처리 (cut_seventy 기반)
                    if best_csv_match['cut_ninety'] is not None:
                        try:
                            cut_ninety = float(str(best_csv_match['cut_ninety']).strip())
                        except:
                            cut_ninety = cut_seventy
                    else:
                        cut_ninety = cut_seventy
                    
                    # admission_score에 삽입
                    insert_query = text("""
                        INSERT INTO admission_score (univ_id, major_id, admission_type, cut_fifty, cut_seventy, cut_ninety)
                        VALUES (:univ_id, :major_id, :admission_type, :cut_fifty, :cut_seventy, :cut_ninety)
                    """)
                    
                    session.execute(insert_query, {
                        'univ_id': um_combo['univ_id'],
                        'major_id': um_combo['major_id'],
                        'admission_type': best_csv_match['admission_type'],
                        'cut_fifty': cut_fifty,
                        'cut_seventy': cut_seventy,
                        'cut_ninety': cut_ninety
                    })
                    
                    mapped_count += 1
                    
                    # 매핑 결과 기록
                    mapping_details.append({
                        'db_university': um_combo['univ_name'],
                        'db_major': um_combo['major_name'],
                        'csv_original_university': best_csv_match['original_university'],
                        'csv_standardized_university': best_csv_match['university'],
                        'csv_major': best_csv_match['major'],
                        'univ_similarity': best_univ_similarity,
                        'major_similarity': best_major_similarity,
                        'total_similarity': best_total_similarity,
                        'admission_type': best_csv_match['admission_type']
                    })
                
                except Exception as e:
                    errors.append({
                        'db_university': um_combo['univ_name'],
                        'db_major': um_combo['major_name'],
                        'reason': str(e)
                    })
            else:
                # 조건을 만족하는 매핑이 없는 경우
                errors.append({
                    'db_university': um_combo['univ_name'],
                    'db_major': um_combo['major_name'],
                    'reason': "학교 유사도 0.8 또는 학과 유사도 0.6 조건 미충족"
                })
        
        # 5. 커밋
        session.commit()
        print(f"\n5. 매핑 완료!")
        
        # 6. 결과 출력
        print(f"\n=== 매핑 결과 ===")
        print(f"총 CSV 행: {len(df)}개")
        print(f"성공적으로 매핑: {mapped_count}개")
        print(f"매핑 실패: {len(errors)}개")
        print(f"매핑 성공률: {mapped_count/len(df)*100:.1f}%")
        
        # 7. 매핑 상세 결과 CSV 저장
        if mapping_details:
            mapping_df = pd.DataFrame(mapping_details)
            mapping_df.to_csv('similarity_mapping_results.csv', index=False, encoding='utf-8-sig')
            print(f"\n매핑 상세 결과를 'similarity_mapping_results.csv'에 저장했습니다.")
        
        # 8. 오류 결과 CSV 저장
        if errors:
            error_df = pd.DataFrame(errors)
            error_df.to_csv('similarity_mapping_errors.csv', index=False, encoding='utf-8-sig')
            print(f"매핑 오류 결과를 'similarity_mapping_errors.csv'에 저장했습니다.")
        
        # 9. 최종 통계
        final_count_query = text("SELECT COUNT(*) as count FROM admission_score")
        final_count = session.execute(final_count_query).scalar()
        print(f"\n최종 admission_score 테이블 데이터: {final_count}개")
        
    except Exception as e:
        session.rollback()
        print(f"에러 발생: {e}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    main()
