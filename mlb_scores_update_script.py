
from proj_secrets import REDIS_SERVER_IP, REDIS_SERVER_PORT
from datetime import datetime, timedelta
import json
import re
import sys
import datetime
import redis

### MLB DB Index = 1 ###

default_batch_size = 30

def init_redis_conn():
    redis_conn = redis.Redis(host=REDIS_SERVER_IP, port=REDIS_SERVER_PORT, db=1, decode_responses=True)
    return redis_conn

def close_redis_conn(redis_conn):
    try:
        redis_conn.close()
        print("Redis DB connection successfully closed!")
    except Exception as e:
        print(f"Error closing Redis DB connection: {e}")
