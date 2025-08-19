#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from sqlalchemy import text
from db import SessionLocal


def main():
    session = SessionLocal()
    try:
        query = text(
            """
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
            """
        )
        result = session.execute(query)

        out_path = os.path.join(os.path.dirname(__file__), 'admission_scores_full.csv')
        with open(out_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['대학교명', '학과명', '전형명', '50%컷', '70%컷', '90%컷'])
            count = 0
            for row in result:
                writer.writerow([
                    row.university_name,
                    row.major_name,
                    row.admission_type,
                    row.cut_fifty,
                    row.cut_seventy,
                    row.cut_ninety,
                ])
                count += 1

        print(f"총 {count}행을 저장했습니다.")
        print(f"저장 경로: {out_path}")
    finally:
        session.close()


if __name__ == '__main__':
    main()
