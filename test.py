from proj_secrets import REDIS_SERVER_IP, REDIS_SERVER_PORT
from redis.commands.json.path import Path
import redis


r = redis.Redis(host=REDIS_SERVER_IP, port=REDIS_SERVER_PORT, decode_responses=True)

mock_game_data = {
    "game_id": "001",
    "home_team": "PHI",
    "away_team": "NYG",
    "home_score": 23,
    "away_score": 17
}

r.hset("game:001", mapping=mock_game_data)

game_data = r.hgetall("game:001")
print({k: v for k, v in game_data.items()})