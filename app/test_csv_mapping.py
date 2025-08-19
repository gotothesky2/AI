#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from services.ExcelMappingService import excelMappingService
    print("✅ ExcelMappingService import 성공!")
    
    # 교과 데이터.csv 파일 매핑
    print("\n🚀 CSV 매핑 시작...")
    result = excelMappingService.mapCSVToAdmissionScore('domain/교과 데이터.csv')
    
    # 결과 확인
    if result['success']:
        print(f"✅ 성공: {result['message']}")
        print(f"📊 매핑된 데이터: {result['mapped_count']}/{result['total_rows']}")
        
        # 경고 메시지 확인 (퍼지 매칭된 경우)
        if result['warnings']:
            print(f"\n⚠️ 퍼지 매칭된 학과들: {len(result['warnings'])}개")
            for warning in result['warnings'][:5]:  # 처음 5개만 표시
                print(f"  {warning}")
        
        # 매핑 상세 결과 샘플 확인
        print(f"\n🔍 매핑 상세 결과 샘플:")
        for detail in result['mapping_details'][:3]:  # 처음 3개만 표시
            print(f"  행 {detail['row']}: {detail['excel_university']} - {detail['excel_major']}")
            print(f"    → {detail['matched_university']} - {detail['matched_major']} (유사도: {detail['similarity']:.2f})")
        
        # 오류가 있는 경우
        if result['errors']:
            print(f"\n❌ 오류 발생: {len(result['errors'])}개")
            for error in result['errors'][:3]:  # 처음 3개만 표시
                print(f"  {error}")
            
    else:
        print(f"❌ 매핑 실패: {result['error']}")
        
except ImportError as e:
    print(f"❌ Import 오류: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ 실행 오류: {e}")
    import traceback
    traceback.print_exc()
