import utils
import requests

### NFL DB Index = 0 ###

def extract_quarter(status_string):
    status_string_split = status_string.split(' - ')
    return status_string_split[1]

def extract_possession_info(game, home_team_id, home_team_abbrev, away_team_abbrev):
    if game['status']['type']['state'] != 'in':
        return "None"
    else:
        try:
            possession_info = game['competitions'][0]['situation']['possession']
            if possession_info == home_team_id:
                possession_info = home_team_abbrev
            else:
                possession_info = away_team_abbrev
            return possession_info
        except KeyError:
            return "None"
        
def resolve_team_records(game):
    home_record = "N/A"
    away_record = "N/A"

    if ("AFC" not in game['shortName'] and "NFC" not in game['shortName']):
        home_record = game['competitions'][0]['competitors'][0]['records'][0]['summary']
        away_record = game['competitions'][0]['competitors'][1]['records'][0]['summary']

    return home_record, away_record
        
def save_nfl_game_count(db_conn, num_games):
    game_count_record = {
        "id": "nfl_game_count_record",
        "game_count": num_games
    }
    db_conn.hset("nfl_game_count", mapping=game_count_record)
        
def save_nfl_game_updates(db_conn, game, id):
    print(f"Processing game: {game['shortName']}")
    team_abbrevs = utils.extract_team_abbrev(game['shortName'])
    home_team_abbrev = team_abbrevs[1]
    home_team_id = game['competitions'][0]['competitors'][0]['team']['id']
    away_team_abbrev = team_abbrevs[0]
    away_team_id = game['competitions'][0]['competitors'][1]['team']['id']
    home_score = game['competitions'][0]['competitors'][0]['score']
    away_score = game['competitions'][0]['competitors'][1]['score']
    game_state = game['status']['type']['state']
    home_record, away_record = resolve_team_records(game)
    possession_info = extract_possession_info(game, home_team_id, home_team_abbrev, away_team_abbrev)
    display_game_state = None

    if game_state == 'pre':
        display_game_state = utils.extract_pst_game_time(game['status']['type']['shortDetail'])
    elif game_state == 'in' and "Quarter" in game['status']['type']['shortDetail']:
        display_game_state = extract_quarter(game['status']['type']['shortDetail']) + " Quarter"
    else:
        display_game_state = game['status']['type']['shortDetail']

    full_game_id = f"nfl_game:{id}"

    game_record = {
        "game_id": id,
        "home_team": home_team_abbrev,
        "away_team": away_team_abbrev,
        "home_team_id": home_team_id,
        "away_team_id": away_team_id,
        "home_score": home_score,
        "away_score": away_score,
        "home_record": home_record,
        "away_record": away_record,
	    "game_state": game_state,
        "display_game_state": display_game_state,
        "possession_info": possession_info
    }
    db_conn.hset(full_game_id, mapping=game_record)
    print(f"Created game record for game: {game['shortName']}")
 
def fetch_all_live_nfl_games(db_conn):
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    response = requests.get(url)
    data = response.json()

    id = 0
    if (data['events'] == None or len(data['events']) == 0):
        print("No NFL games are currently live.")
    else:
        utils.clear_db(db_conn)
        num_games = len(data['events'])
        save_nfl_game_count(db_conn, num_games)
        for game in data['events']:
            save_nfl_game_updates(db_conn, game, id)
            id += 1

def main():
    print("----")
    db_conn = None
    try:
        db_conn = utils.init_redis_conn("nfl")
        fetch_all_live_nfl_games(db_conn)
    except Exception as e:
        print(f"An error occurred during the NFL update service's execution: {e}")
    finally:
        utils.close_redis_conn(db_conn)


if __name__ == "__main__":
    main()
