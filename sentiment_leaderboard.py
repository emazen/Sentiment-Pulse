import pandas as pd
from utils.reddit_scraper import get_reddit_data
from utils.sentiment_analyzer import analyze_sentiment
from utils.nba_stats import get_player_info

def update_leaderboard():
    # List of top 100 NBA players 
    top_players = ["LeBron James", "Kevin Durant", "Stephen Curry", "Giannis Antetokounmpo", "Luka Doncic",
                   "Kyrie Irving", "Joel Embiid", "Nikola Jokic", "Shai Gilgeous Alexander"]  # Add more players

    leaderboard_data = []

    for player in top_players:
        try:
            reddit_data = get_reddit_data(player)
            _, overall_sentiment, sentiment_label = analyze_sentiment(reddit_data)
            player_info = get_player_info(player, "2023-24")
            
            leaderboard_data.append({
                "name": player,
                "sentiment_score": overall_sentiment,
                "sentiment_label": sentiment_label,
                "ppg": player_info['ppg'],
                "rpg": player_info['rpg'],
                "apg": player_info['apg']
            })
        except Exception as e:
            print(f"Error processing {player}: {str(e)}")

    df = pd.DataFrame(leaderboard_data)
    df = df.sort_values("sentiment_score", ascending=False).reset_index(drop=True)
    df.to_csv("static/sentiment_leaderboard.csv", index=False)

if __name__ == "__main__":
    update_leaderboard()