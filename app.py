from flask import Flask, render_template, request, jsonify
from utils.reddit_scraper import get_reddit_data
from utils.sentiment_analyzer import analyze_sentiment
from utils.data_visualizer import create_sentiment_chart, create_word_cloud, create_points_chart
from utils.nba_stats import get_player_info
from datetime import datetime

app = Flask(__name__)

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
        sentiment_data = analyze_sentiment(reddit_data)
    
        sentiment_data = [(date, sentiment, title, url) for date, sentiment, title, url in sentiment_data 
                          if start_date <= date <= end_date]

        chart_path = create_sentiment_chart(sentiment_data)
        word_cloud_path = create_word_cloud(reddit_data, player_name)

        # Create points chart using the game_data from player_info
        points_chart_path = create_points_chart(player_info['game_data'])

        return jsonify({
            'chart_path': chart_path,
            'word_cloud_path': word_cloud_path,
            'points_chart_path': points_chart_path,
            'player_info': player_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)