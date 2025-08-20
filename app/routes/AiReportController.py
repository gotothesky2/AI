from fastapi import APIRouter,Depends
from typing import List
from services.AiReportService import aiReportService
from DTO.AiRepotDto import AiReportResponse,AiReportRequest,AiReportListResponse
from login.oauth_jwt_auth import get_current_user
from domain.User import User
from globals import (
    ErrorCode,
    raise_business_exception,
    raise_file_exception,
    BusinessException,
    FileException,
    DatabaseException, raise_database_exception
)
from globals import create_success_response

router =APIRouter(prefix='/aireport')

@router.post("/me",summary="현재 유저의 모든 aiReport를 가져옵니다.")
async def getAiReportsByMe(current_user:User = Depends(get_current_user)):
    try:
        result_list:List[AiReportListResponse]= aiReportService.getAllAiReportsByUser(current_user.uid)
        return create_success_response(result_list,message="사용자 AI Report 목록 조회가 성공하였습니다.")
    except BusinessException as e:
        raise_business_exception(e.error_code,f"AiReport 목록 조히 실패{e.detail}")

    except DatabaseException as e:
        raise_business_exception(e.error_code,e.detail)
    except Exception as e:
        raise_business_exception(ErrorCode.UNKNOWN_ERROR,f"aiReport API 예상치 못한 오류{str(e)}")


@router.get("/{report_id}",summary="AiReport 내용물 get")
async def get_aiReport(report_id:int):
    try:
        result=aiReportService.getAireportByID(report_id)
        return create_success_response(result,"레포트 조회가 완료되었습니다")

    except BusinessException as e:
        raise_business_exception(e.error_code,f"레포트 조회중 에러발생{e.detail}")

    except DatabaseException as e:
        raise_database_exception(e.error_code,e.detail)

    except Exception as e:
        raise_business_exception(ErrorCode.UNKNOWN_ERROR,f"aiReport 레포트 하나 조회중 예상치 못한 오류{str(e)}")

@router.delete("/{report_id}",summary="AiReport 삭제 Api")
async def delete_aiReport(report_id:int):
    try:
        aiReportService.deleteAiReport(report_id)
        return create_success_response(message=f"aiReport ID{report_id}가 성공적으로 삭제되었습니다")
    except BusinessException as e:
        raise_business_exception(e.error_code,f"AI Report 삭제 실패 {e.detail}")
    except DatabaseException as e:
        raise_database_exception(e.error_code,f"AI 레포트 삭제중 데이터베이스 에러발생 {e.detail}")
    except Exception as e:
        raise_business_exception(ErrorCode.UNKNOWN_ERROR,f"AiReport 삭제 Api 예창치 못한 오류 {str(e)}")

@router.post("",summary="AiReport생성 Api")
async def create_aiReport(request:AiReportRequest,current_user:User = Depends(get_current_user)):
    try:
        result=aiReportService.createAiReport(request,current_user.uid)
        return create_success_response(result,f"사용자 aiReport생성 성공")
    except BusinessException as e:
        raise_business_exception(e.error_code,f"레포트 생성 실패 {e.detail}")
    except DatabaseException as e:
        raise_database_exception(e.error_code,e.detail)
    except Exception as e:
        raise_business_exception(ErrorCode.UNKNOWN_ERROR,f"레포트 생성중 예상치 못한 에러 발생 {str(e)}")

