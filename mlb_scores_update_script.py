import utils
import requests
import re

### MLB DB Index = 1 ###

def parse_inning_string(inning_string):
    # In the case that there is a rain delay, we convert the inning string into something
    # shorter so that it doesn't get cut off on the LED display.
    pattern = r"Rain Delay, (Top|Bottom) (\d+)(st|nd|rd|th)"

    match = re.match(pattern, inning_string)

    if match:
        inning_half = match.group(1)[0].upper()
        inning_number = match.group(2)
        output_string = f"RD: {inning_half}{inning_number}"
        return output_string
    else:
        return inning_string
    
def save_mlb_game_updates(db_conn, game, id):
    print(f"Processing game: {game['shortName']}")
    team_abbrevs = utils.extract_team_abbrev(game['shortName'])
    away_team_abbrev = team_abbrevs[0]
    home_team_abbrev = team_abbrevs[1]
    home_score = game['competitions'][0]['competitors'][0]['score']
    away_score = game['competitions'][0]['competitors'][1]['score']

    current_state = game['status']['type']['state']
    if current_state == 'pre':
        inning = utils.extract_pst_game_time(game['status']['type']['shortDetail'])
        first_base_status = False
        second_base_status = False
        third_base_status = False
    elif current_state == 'in':
        inning = parse_inning_string(game['status']['type']['detail'])
        first_base_status = game['competitions'][0]['situation']['onFirst']
        second_base_status = game['competitions'][0]['situation']['onSecond']
        third_base_status = game['competitions'][0]['situation']['onThird']
    else:
        inning = parse_inning_string(game['status']['type']['shortDetail'])
        first_base_status = False
        second_base_status = False
        third_base_status = False

    game_record = {
        "game_id": id,
        "away_team": away_team_abbrev,
        "home_team": home_team_abbrev,
        "away_score": away_score,
        "home_score": home_score,
        "first_base": str(first_base_status),
        "second_base": str(second_base_status),
        "third_base": str(third_base_status),
        "inning": inning,
        "current_state": current_state
    }
    db_conn.hset(f"mlb_game:{id}", mapping=game_record)
    print(f"Created game record for game: {game['shortName']}")

def save_mlb_game_count(db_conn, num_games):
    game_count_record = {
        "id": "mlb_game_count_record",
        "game_count": num_games
    }
    db_conn.hset("mlb_game_count", mapping=game_count_record)

def fetch_all_live_mlb_games(db_conn):
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    response = requests.get(url)
    data = response.json()

    id = 0
    if (data['events'] == None or len(data['events']) == 0):
        print("No MLB games are currently live.")
    else:
        utils.clear_db(db_conn)
        num_games = len(data['events'])
        save_mlb_game_count(db_conn, num_games)
        for game in data['events']:
            save_mlb_game_updates(db_conn, game, id)
            id += 1

def main():
    print("----")
    db_conn = None
    try:
        db_conn = utils.init_redis_conn("mlb")
        fetch_all_live_mlb_games(db_conn)
    except Exception as e:
        print(f"An error occurred during the MLB update service's execution: {e}")
    finally:
        utils.close_redis_conn(db_conn)

if __name__ == "__main__":
    main()