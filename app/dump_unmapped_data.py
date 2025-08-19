#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pandas as pd
from sqlalchemy import text
from db import SessionLocal

def main():
    session = SessionLocal()
    try:
        # CSV 파일 읽기
        df = pd.read_csv('domain/교과 데이터.csv', encoding='utf-8')
        
        # 컬럼명 설정
        if len(df.columns) >= 6:
            df.columns = ['university', 'admission_type', 'major', 'cut_fifty', 'cut_seventy'] + list(df.columns[5:])
        elif len(df.columns) == 5:
            df.columns = ['university', 'admission_type', 'major', 'cut_fifty', 'cut_seventy']
        elif len(df.columns) == 4:
            df.columns = ['university', 'admission_type', 'major', 'cut_fifty']
        
        # DB에서 매핑된 데이터 조회
        mapped_query = text("""
            SELECT DISTINCT a.univ_id, a.major_id
            FROM admission_score a
        """)
        mapped_result = session.execute(mapped_query)
        mapped_pairs = set()
        for row in mapped_result:
            mapped_pairs.add((row.univ_id, row.major_id))
        
        # 대학교명으로 ID 매핑
        univ_name_to_id = {}
        univ_query = text("SELECT univ_id, univ_name FROM university")
        univ_result = session.execute(univ_query)
        for row in univ_result:
            univ_name_to_id[row.univ_name] = row.univ_id
        
        # 학과명으로 ID 매핑
        major_name_to_id = {}
        major_query = text("SELECT m_id, m_name FROM major")
        major_result = session.execute(major_query)
        for row in major_result:
            major_name_to_id[row.m_name] = row.m_id
        
        # 매핑되지 않은 데이터 찾기
        unmapped_data = []
        
        for index, row in df.iterrows():
            excel_univ = row.iloc[0] if pd.notna(row.iloc[0]) else ""
            excel_major = row.iloc[2] if pd.notna(row.iloc[2]) else ""
            
            if excel_univ and excel_major:
                univ_id = univ_name_to_id.get(excel_univ)
                major_id = major_name_to_id.get(excel_major)
                
                if univ_id and major_id:
                    # 둘 다 DB에 있지만 admission_score에 없는 경우
                    if (univ_id, major_id) not in mapped_pairs:
                        unmapped_data.append({
                            'row': index + 1,
                            'university': excel_univ,
                            'major': excel_major,
                            'admission_type': row.iloc[1] if pd.notna(row.iloc[1]) else "",
                            'cut_fifty': row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else "",
                            'cut_seventy': row.iloc[4] if len(row) > 4 and pd.notna(row.iloc[4]) else "",
                            'cut_ninety': row.iloc[5] if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                            'reason': 'DB에 존재하지만 admission_score에 매핑되지 않음'
                        })
                elif not univ_id:
                    # 대학교가 DB에 없는 경우
                    unmapped_data.append({
                        'row': index + 1,
                        'university': excel_univ,
                        'major': excel_major,
                        'admission_type': row.iloc[1] if pd.notna(row.iloc[1]) else "",
                        'cut_fifty': row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else "",
                        'cut_seventy': row.iloc[4] if len(row) > 4 and pd.notna(row.iloc[4]) else "",
                        'cut_ninety': row.iloc[5] if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                        'reason': '대학교가 DB에 존재하지 않음'
                    })
                elif not major_id:
                    # 학과가 DB에 없는 경우
                    unmapped_data.append({
                        'row': index + 1,
                        'university': excel_univ,
                        'major': excel_major,
                        'admission_type': row.iloc[1] if pd.notna(row.iloc[1]) else "",
                        'cut_fifty': row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else "",
                        'cut_seventy': row.iloc[4] if len(row) > 4 and pd.notna(row.iloc[4]) else "",
                        'cut_ninety': row.iloc[5] if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                        'reason': '학과가 DB에 존재하지 않음'
                    })
        
        # CSV로 저장
        out_path = 'unmapped_data.csv'
        with open(out_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['행번호', '대학교', '학과', '전형명', '50%컷', '70%컷', '90%컷', '매핑실패사유'])
            
            for data in unmapped_data:
                writer.writerow([
                    data['row'],
                    data['university'],
                    data['major'],
                    data['admission_type'],
                    data['cut_fifty'],
                    data['cut_seventy'],
                    data['cut_ninety'],
                    data['reason']
                ])
        
        print(f"매핑되지 않은 데이터: {len(unmapped_data)}개")
        print(f"저장 경로: {out_path}")
        
        # 통계 출력
        reasons = {}
        for data in unmapped_data:
            reason = data['reason']
            reasons[reason] = reasons.get(reason, 0) + 1
        
        print("\n매핑 실패 사유별 통계:")
        for reason, count in reasons.items():
            print(f"  {reason}: {count}개")
        
    finally:
        session.close()

if __name__ == '__main__':
    main()
