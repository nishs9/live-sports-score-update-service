from proj_secrets import REDIS_SERVER_IP, REDIS_SERVER_PORT
from datetime import datetime, timedelta
import redis
import re
import datetime

league_to_db_index = {
    "nfl": 0,
    "mlb": 1
}

def init_redis_conn(league_abbrev):
    db_index = league_to_db_index[league_abbrev]
    redis_conn = redis.Redis(host=REDIS_SERVER_IP, port=REDIS_SERVER_PORT, db=db_index, decode_responses=True)
    return redis_conn

def close_redis_conn(redis_conn):
    if redis_conn is None:
        print("Redis DB connection is already closed.")

    try:
        redis_conn.close()
        print("Redis DB connection successfully closed!")
    except Exception as e:
        print(f"Error closing Redis DB connection: {e}")

def clear_db(db_conn):
    try:
        db_conn.flushdb()
        print("DB successfully cleared!")
    except Exception as e:
        print(f"Error encountered while clearing DB: {e}")

def extract_team_abbrev(team_string):
    match = re.match(r'(\S+)\s\S+\s(\S+)', team_string)
    if match:
        return match.groups()
    else:
        print("The following game string is in an invalid format:")
        print(team_string)

def extract_pst_game_time(time_string):
    time_split_list = time_string.split(' ')
    est_game_time = time_split_list[2] + ' ' + time_split_list[3]
    time_obj = datetime.datetime.strptime(est_game_time, '%I:%M %p')
    time_obj = time_obj - timedelta(hours=3)
    pst_game_time = time_obj.strftime('%I:%M %p')
    return pst_game_time