from flask import Flask, render_template, request, jsonify
from utils.reddit_scraper import get_reddit_data
from utils.sentiment_analyzer import analyze_sentiment
from utils.data_visualizer import create_sentiment_chart, create_points_chart
from utils.nba_stats import get_player_info, get_all_players
from datetime import datetime
import pandas as pd
import os
import numpy as np

app = Flask(__name__)

@app.route('/player-names', methods=['GET'])
def player_names():
    query = request.args.get('q', '').lower()
    all_players = get_all_players()
    matching_players = [player for player in all_players if query in player.lower()]
    return jsonify(matching_players[:10])  # Limit to 10 suggestions

def update_leaderboard(player_name, overall_sentiment, sentiment_label, player_info, correlation, season):
    csv_path = "static/sentiment_leaderboard.csv"
    
    # Only update the leaderboard if the season is 2023/2024
    if season != "2023/2024":
        return

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=["name", "sentiment_score", "sentiment_label", "ppg", "rpg", "apg", "image_url", "correlation"])
    
    # Check if player already exists in the leaderboard
    if player_name in df['name'].values:
        # Update existing player
        df.loc[df['name'] == player_name, ['sentiment_score', 'sentiment_label', 'ppg', 'rpg', 'apg', 'image_url', 'correlation']] = [
            overall_sentiment, sentiment_label, player_info['ppg'], player_info['rpg'], player_info['apg'], player_info['image_url'], correlation
        ]
    else:
        # Add new player
        new_row = pd.DataFrame({
            "name": [player_name],
            "sentiment_score": [overall_sentiment],
            "sentiment_label": [sentiment_label],
            "ppg": [player_info['ppg']],
            "rpg": [player_info['rpg']],
            "apg": [player_info['apg']],
            "image_url": [player_info['image_url']],
            "correlation": [correlation]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    
    # Sort the dataframe by sentiment_score in descending order
    df = df.sort_values("sentiment_score", ascending=False).reset_index(drop=True)
    
    # Save the updated dataframe
    df.to_csv(csv_path, index=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    player_name = request.form.get('player_name')
    season = request.form.get('season')

    if not player_name or not season:
        return jsonify({'error': 'Player name and season are required'}), 400

    try:
        start_year, end_year = map(int, season.split('/'))
        start_date = datetime(start_year, 10, 1)
        end_date = datetime(end_year, 6, 30)

        # Get player info and game data
        player_info = get_player_info(player_name, f"{start_year}-{str(end_year)[2:]}")

        reddit_data = get_reddit_data(player_name)
        sentiment_data, overall_sentiment, sentiment_label = analyze_sentiment(reddit_data)
    
        sentiment_data = [(date, sentiment, title, url) for date, sentiment, title, url in sentiment_data 
                          if start_date <= date <= end_date]

        chart_path = create_sentiment_chart(sentiment_data, overall_sentiment, sentiment_label)

        # Create points chart using the game_data from player_info
        points_chart_path = create_points_chart(player_info['game_data'])

        # Calculate correlation
        sentiment_dates = [date for date, _, _, _ in sentiment_data]
        sentiment_scores = [sentiment for _, sentiment, _, _ in sentiment_data]
        game_dates = [datetime.fromisoformat(date) for date, _ in player_info['game_data']]
        game_points = [points for _, points in player_info['game_data']]

        # Create a DataFrame with all dates
        all_dates = sorted(set(sentiment_dates + game_dates))
        df = pd.DataFrame(index=all_dates, columns=['sentiment', 'points'])

        # Fill in sentiment scores and points
        for date, sentiment in zip(sentiment_dates, sentiment_scores):
            df.loc[date, 'sentiment'] = sentiment
        for date, points in zip(game_dates, game_points):
            df.loc[date, 'points'] = points

        # Forward fill missing values
        df = df.ffill()

        # Calculate correlation
        correlation = df['sentiment'].corr(df['points'])

        # Update the leaderboard
        update_leaderboard(player_name, overall_sentiment, sentiment_label, player_info, correlation, season)

        return jsonify({
            'chart_path': chart_path,
            'points_chart_path': points_chart_path,
            'player_info': player_info,
            'overall_sentiment': round(overall_sentiment, 2),
            'sentiment_label': sentiment_label,
            'correlation': round(correlation, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    try:
        csv_path = "static/sentiment_leaderboard.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            leaderboard_data = df.to_dict('records')
        else:
            leaderboard_data = []
        return render_template('leaderboard.html', leaderboard_data=leaderboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)