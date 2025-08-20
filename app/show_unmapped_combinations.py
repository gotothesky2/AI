#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from sqlalchemy import text
from db import SessionLocal

def main():
    session = SessionLocal()
    try:
        print("=== university_major에 존재하지만 admission_score에 매핑되지 않은 조합 ===")
        
        # university_major에는 있지만 admission_score에는 없는 조합 찾기
        query = text("""
            SELECT 
                u.univ_name as university_name,
                m.m_name as major_name,
                um.univ_id,
                um.m_id
            FROM university_major um
            JOIN university u ON um.univ_id = u.univ_id
            JOIN major m ON um.m_id = m.m_id
            WHERE NOT EXISTS (
                SELECT 1 FROM admission_score a 
                WHERE a.univ_id = um.univ_id AND a.major_id = um.m_id
            )
            ORDER BY u.univ_name, m.m_name
        """)
        
        result = session.execute(query)
        
        # 결과를 리스트로 저장
        unmapped_combinations = []
        for row in result:
            unmapped_combinations.append({
                'university': row.university_name,
                'major': row.major_name,
                'univ_id': row.univ_id,
                'major_id': row.m_id
            })
        
        print(f"총 {len(unmapped_combinations)}개의 매핑되지 않은 조합이 있습니다.")
        print()
        
        # 처음 50개 출력
        print("=== 처음 50개 조합 ===")
        for i, combo in enumerate(unmapped_combinations[:50]):
            print(f"{i+1:3d}. {combo['university']:<20} - {combo['major']}")
        
        if len(unmapped_combinations) > 50:
            print(f"\n... 총 {len(unmapped_combinations)}개 중 50개만 표시")
        
        # CSV로 저장
        out_path = 'unmapped_university_major_combinations.csv'
        with open(out_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['대학교명', '학과명', '대학교ID', '학과ID'])
            
            for combo in unmapped_combinations:
                writer.writerow([
                    combo['university'],
                    combo['major'],
                    combo['univ_id'],
                    combo['major_id']
                ])
        
        print(f"\n전체 결과를 '{out_path}' 파일로 저장했습니다.")
        
        # 통계 정보
        print(f"\n=== 통계 정보 ===")
        
        # university_major 총 개수
        total_um_query = text("SELECT COUNT(*) as count FROM university_major")
        total_um = session.execute(total_um_query).scalar()
        
        # admission_score 총 개수
        total_as_query = text("SELECT COUNT(*) as count FROM admission_score")
        total_as = session.execute(total_as_query).scalar()
        
        # 매핑된 조합 수
        mapped_query = text("""
            SELECT COUNT(DISTINCT CONCAT(univ_id, '_', major_id)) as count 
            FROM admission_score
        """)
        mapped_count = session.execute(mapped_query).scalar()
        
        print(f"university_major 테이블 총 조합: {total_um}개")
        print(f"admission_score 테이블 총 매핑: {total_as}개")
        print(f"매핑된 고유 조합: {mapped_count}개")
        print(f"매핑되지 않은 조합: {len(unmapped_combinations)}개")
        print(f"매핑률: {mapped_count/total_um*100:.1f}%")
        
    finally:
        session.close()

if __name__ == '__main__':
    main()
