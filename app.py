from flask import Flask, render_template, request, jsonify
from utils.reddit_scraper import get_reddit_data
from utils.sentiment_analyzer import analyze_sentiment
from utils.data_visualizer import create_sentiment_chart, create_word_cloud
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    player_name = request.form.get('player_name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not player_name:
        return jsonify({'error': 'Player name is required'}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        reddit_data = get_reddit_data(player_name)
        sentiment_data = analyze_sentiment(reddit_data)
    
        if start_date and end_date:
            sentiment_data = [(date, sentiment, title, url) for date, sentiment, title, url in sentiment_data 
                            if start_date <= date <= end_date]

        chart_path = create_sentiment_chart(sentiment_data)
        word_cloud_path = create_word_cloud(reddit_data)

        return jsonify({
            'chart_path': chart_path,
            'word_cloud_path': word_cloud_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # or any other available port