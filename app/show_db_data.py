#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import SessionLocal
from sqlalchemy import text

def main():
    # DB 연결
    session = SessionLocal()
    
    try:
        # 입학성적 데이터 조회 (대학교명, 학과명, 전형명, 커트라인 포함)
        print("=== 입학성적 데이터 (대학교명, 학과명, 전형명, 50/70/90 커트라인) ===")
        
        # JOIN 쿼리로 한 번에 조회 (올바른 컬럼명 사용)
        query = text("""
            SELECT 
                u.univ_name as university_name,
                m.m_name as major_name,
                a.admission_type,
                a.cut_fifty,
                a.cut_seventy,
                a.cut_ninety
            FROM admission_score a
            JOIN university u ON a.univ_id = u.univ_id
            JOIN major m ON a.major_id = m.m_id
            ORDER BY u.univ_name, m.m_name
            LIMIT 20
        """)
        
        result = session.execute(query)
        
        print(f"{'대학교명':<20} {'학과명':<20} {'전형명':<25} {'50%컷':<8} {'70%컷':<8} {'90%컷':<8}")
        print("-" * 100)
        
        count = 0
        for row in result:
            print(f"{row.university_name:<20} {row.major_name:<20} {row.admission_type:<25} "
                  f"{row.cut_fifty:<8} {row.cut_seventy:<8} {row.cut_ninety:<8}")
            count += 1
        
        # 전체 개수 조회
        count_query = text("SELECT COUNT(*) as total FROM admission_score")
        total_result = session.execute(count_query)
        total_count = total_result.scalar()
        
        print()
        print(f"총 {total_count}개 입학성적 데이터")
        
        # 추가 통계 정보
        print("\n=== 추가 통계 ===")
        
        # 전형별 개수
        type_count_query = text("""
            SELECT admission_type, COUNT(*) as count 
            FROM admission_score 
            GROUP BY admission_type 
            ORDER BY count DESC
        """)
        type_counts = session.execute(type_count_query)
        print("전형별 개수:")
        for row in type_counts:
            print(f"  {row.admission_type}: {row.count}개")
        
        # 대학교별 개수 (상위 10개)
        univ_count_query = text("""
            SELECT u.univ_name, COUNT(*) as count 
            FROM admission_score a
            JOIN university u ON a.univ_id = u.univ_id
            GROUP BY a.univ_id, u.univ_name
            ORDER BY count DESC
            LIMIT 10
        """)
        univ_counts = session.execute(univ_count_query)
        print("\n대학교별 입학성적 데이터 개수 (상위 10개):")
        for row in univ_counts:
            print(f"  {row.univ_name}: {row.count}개")
        
    finally:
        session.close()

if __name__ == '__main__':
    main()
