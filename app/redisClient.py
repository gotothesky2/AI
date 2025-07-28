import os
import redis
from os import getenv
def get_redis_client():
    host=os.getenv("REDIS_HOST")
    port=int(os.getenv("REDIS_PORT"))
    db=int(os.getenv("REDIS_DB"))
    password=getenv("REDIS_PASSWORD")
    return redis.Redis(host=host, port=port, db=db, password=password)