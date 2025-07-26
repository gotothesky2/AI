from fastapi import APIRouter, Depends
from typing import List
from app.services.UserService import userService
from app.DTO.UserDTO import UserCreateRequest, UserUpdateRequest, UserResponse
from app.domain.User import User
from app.util.exceptions import (
    ErrorCode, 
    raise_business_exception, 
    raise_validation_exception
)
from app.util.exception_handler import create_success_response

router = APIRouter(prefix="/users")

@router.post("", summary="사용자 생성")
async def create_user(request: UserCreateRequest):
    """
    새로운 사용자를 생성합니다.
    """
    try:
        user = userService.createUser(
            name=request.name,
            email=request.email,
            phone_number=request.phone_number,
            grade_num=request.grade_num,
            highschool=request.highschool,
            sex=request.sex
        )
        return create_success_response(
            UserResponse.model_validate(user, from_attributes=True),
            "사용자가 성공적으로 생성되었습니다."
        )
    except Exception as e:
        raise_business_exception(ErrorCode.USER_ALREADY_EXISTS, str(e))

@router.get("/{uid}", summary="사용자 조회")
async def get_user(uid: str):
    """
    특정 사용자를 조회합니다.
    """
    try:
        user = userService.getUserById(uid)
        return create_success_response(
            UserResponse.model_validate(user, from_attributes=True),
            "사용자 조회가 완료되었습니다."
        )
    except Exception as e:
        raise_business_exception(ErrorCode.USER_NOT_FOUND, str(e))

@router.get("/email/{email}", summary="이메일로 사용자 조회")
async def get_user_by_email(email: str):
    """
    이메일로 사용자를 조회합니다.
    """
    try:
        user = userService.getUserByEmail(email)
        return create_success_response(
            UserResponse.model_validate(user, from_attributes=True),
            "이메일로 사용자 조회가 완료되었습니다."
        )
    except Exception as e:
        raise_business_exception(ErrorCode.USER_NOT_FOUND, str(e))

@router.get("", summary="모든 사용자 조회")
async def get_all_users():
    """
    모든 사용자를 조회합니다.
    """
    try:
        users = userService.getAllUsers()
        user_responses = [UserResponse.model_validate(user, from_attributes=True) for user in users]
        return create_success_response(user_responses, "모든 사용자 조회가 완료되었습니다.")
    except Exception as e:
        raise_business_exception(ErrorCode.DATABASE_ERROR, str(e))

@router.put("/{uid}", summary="사용자 정보 수정")
async def update_user(uid: str, request: UserUpdateRequest):
    """
    사용자 정보를 수정합니다.
    """
    try:
        # None이 아닌 값만 필터링
        update_data = {k: v for k, v in request.dict().items() if v is not None}
        user = userService.updateUser(uid, **update_data)
        return create_success_response(
            UserResponse.model_validate(user, from_attributes=True),
            "사용자 정보가 성공적으로 수정되었습니다."
        )
    except Exception as e:
        raise_business_exception(ErrorCode.USER_NOT_FOUND, str(e))

@router.delete("/{uid}", summary="사용자 삭제")
async def delete_user(uid: str):
    """
    사용자를 삭제합니다.
    """
    try:
        userService.deleteUser(uid)
        return create_success_response(message=f"사용자 {uid}가 성공적으로 삭제되었습니다.")
    except Exception as e:
        raise_business_exception(ErrorCode.USER_NOT_FOUND, str(e))

@router.patch("/{uid}/token", summary="토큰 업데이트")
async def update_user_token(uid: str, token_amount: int):
    """
    사용자의 토큰을 업데이트합니다.
    """
    try:
        user = userService.updateToken(uid, token_amount)
        return create_success_response(
            UserResponse.model_validate(user, from_attributes=True),
            "토큰이 성공적으로 업데이트되었습니다."
        )
    except Exception as e:
        raise_business_exception(ErrorCode.USER_NOT_FOUND, str(e)) 