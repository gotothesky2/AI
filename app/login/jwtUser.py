# 기존 JWT 관련 코드 (하위 호환성을 위해 유지)
# 새로운 JWT 시스템은 jwt_util.py를 사용하세요

import os
from datetime import datetime, timedelta
from jose import JWT

# 새로운 JWT 시스템 사용을 위한 리다이렉트
from .jwt_util import jwt_util, JWTUtil

# 하위 호환성을 위한 별칭
JWTUser = JWTUtil
jwt_user = jwt_util