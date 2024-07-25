from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from datetime import datetime

def get_player_game_log(player_name, season):
    # Find the player
    player_dict = players.find_players_by_full_name(player_name)
    if not player_dict:
        raise ValueError(f"Player '{player_name}' not found")
    
    player_id = player_dict[0]['id']
    
    # Get game log for the specified season
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    games = game_log.get_data_frames()[0]
    
    # Extract date and points, convert date to datetime object
    game_data = []
    for _, game in games.iterrows():
        date = datetime.strptime(game['GAME_DATE'], '%b %d, %Y')
        points = game['PTS']
        game_data.append((date, points))
    
    return sorted(game_data)