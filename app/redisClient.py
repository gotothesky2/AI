import os
import redis
from os import getenv

def get_redis_client():
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    db = int(os.getenv("REDIS_DB", "0"))
    password = getenv("REDIS_PASSWORD")
    
    return redis.Redis(
        host=host, 
        port=port, 
        db=db, 
        password=password,
        decode_responses=True  # 문자열 자동 디코딩
    )