from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, playercareerstats
from datetime import datetime
import numpy as np

def get_player_info(player_name, season):

    
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
    
    # Get career stats for the season averages
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    season_stats = career_stats.get_data_frames()[0]
    
    # Filter for the specified season
    season_stats = season_stats[season_stats['SEASON_ID'] == season]
    
    if season_stats.empty:
        raise ValueError(f"No stats found for {player_name} in season {season}")
    
    # Extract relevant stats
    games_played = float(season_stats['GP'].values[0])
    ppg = float(season_stats['PTS'].values[0]) / games_played
    rpg = float(season_stats['REB'].values[0]) / games_played
    apg = float(season_stats['AST'].values[0]) / games_played

    
    # Get player image URL
    image_url = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"
    
    return {
        'name': player_name,
        'image_url': image_url,
        'ppg': round(ppg, 1),
        'rpg': round(rpg, 1),
        'apg': round(apg, 1),
        'game_data': [(date.isoformat(), float(points)) for date, points in sorted(game_data)]
    }