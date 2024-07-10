from flask import Flask, render_template, request, jsonify
from utils.reddit_scraper import get_reddit_data
from utils.sentiment_analyzer import analyze_sentiment
from utils.data_visualizer import create_sentiment_chart, create_word_cloud
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    player_name = request.form.get('player_name')
    if not player_name:
        return jsonify({'error': 'Player name is required'}), 400

    try:
        reddit_data = get_reddit_data(player_name)
        sentiment_data = analyze_sentiment(reddit_data)
        chart_path = create_sentiment_chart(sentiment_data)
        word_cloud_path = create_word_cloud(reddit_data)

        return jsonify({
            'chart_path': chart_path,
            'word_cloud_path': word_cloud_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)