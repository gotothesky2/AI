#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

from services.ExcelMappingService import excelMappingService


def main():
    # 매핑 실행 (기본 임계치 사용: strict=0.9, fuzzy=0.7)
    result = excelMappingService.mapCSVToAdmissionScore('domain/교과 데이터.csv')

    fuzzy_rows = [
        d for d in result.get('mapping_details', [])
        if d.get('match_type') == 'fuzzy'
    ]

    out_path = 'fuzzy_matches.csv'
    with open(out_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['row', 'excel_university', 'excel_major', 'matched_university', 'matched_major', 'similarity'])
        for d in fuzzy_rows:
            writer.writerow([
                d.get('row'),
                d.get('excel_university'),
                d.get('excel_major'),
                d.get('matched_university'),
                d.get('matched_major'),
                f"{d.get('similarity', 0):.4f}",
            ])

    print(f"퍼지 매칭 건수: {len(fuzzy_rows)}건")
    print(f"저장 경로: {out_path}")


if __name__ == '__main__':
    main()
