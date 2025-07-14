from fastapi import APIRouter, HTTPException, UploadFile,File
from app.services.HmtService import hmtService
from app.DTO.HmtDTO import HmtResponse

router = APIRouter(prefix="/hmt")
#todo-유저정보 임시땜빵으로 넣어놓음 그래서 나중에 jwt 인증 구현 들어가야함
@router.post("",response_model=HmtResponse)
def create_hmt(request: UploadFile = File(...),)