import unittest
from unittest.mock import patch, MagicMock
from app import app
import json
from datetime import datetime

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('utils.reddit_scraper.get_reddit_data')
    @patch('utils.sentiment_analyzer.analyze_sentiment')
    @patch('utils.nba_stats.get_player_info')
    @patch('utils.data_visualizer.create_sentiment_chart')
    @patch('utils.data_visualizer.create_points_chart')
    def test_analyze_endpoint(self, mock_points_chart, mock_sentiment_chart, 
                              mock_player_info, mock_analyze_sentiment, mock_reddit_data):
        # Mock the return values
        mock_reddit_data.return_value = [
            {'title': 'Test Post', 'text': 'Test Content', 'created_utc': 1623456789, 'url': 'https://reddit.com/test'}
        ]
        mock_analyze_sentiment.return_value = (
            [(datetime(2023, 6, 12), 0.5, 'Test Post', 'https://reddit.com/test')],
            0.5,
            'Positive'
        )
        mock_player_info.return_value = {
            'name': 'Test Player',
            'image_url': 'https://example.com/test.jpg',
            'ppg': 25.0,
            'rpg': 5.0,
            'apg': 5.0,
            'game_data': [('2023-06-12', 25)]
        }
        mock_sentiment_chart.return_value = '/static/images/sentiment_chart.html'
        mock_points_chart.return_value = '/static/images/points_chart.html'

        # Make a request to the /analyze endpoint
        response = self.app.post('/analyze', data={
            'player_name': 'Test Player',
            'season': '2022/2023'
        })

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['player_info']['name'], 'Test Player')
        self.assertEqual(data['player_info']['ppg'], 25.0)
        self.assertEqual(data['player_info']['rpg'], 5.0)
        self.assertEqual(data['player_info']['apg'], 5.0)
        self.assertEqual(data['overall_sentiment'], 0.5)
        self.assertEqual(data['sentiment_label'], 'Positive')
        self.assertEqual(data['chart_path'], '/static/images/sentiment_chart.html')
        self.assertEqual(data['points_chart_path'], '/static/images/points_chart.html')

    @patch('utils.nba_stats.get_all_players')
    def test_player_names_endpoint(self, mock_get_all_players):
        mock_get_all_players.return_value = ['LeBron James', 'Stephen Curry', 'Kevin Durant']

        response = self.app.get('/player-names?q=Le')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, ['LeBron James'])

    @patch('pandas.read_csv')
    def test_leaderboard_endpoint(self, mock_read_csv):
        mock_data = [
            {'name': 'Player 1', 'sentiment_score': 0.8, 'sentiment_label': 'Positive', 'ppg': 25.0, 'rpg': 5.0, 'apg': 5.0, 'image_url': 'https://example.com/1.jpg'},
            {'name': 'Player 2', 'sentiment_score': -0.2, 'sentiment_label': 'Negative', 'ppg': 20.0, 'rpg': 8.0, 'apg': 3.0, 'image_url': 'https://example.com/2.jpg'}
        ]
        mock_read_csv.return_value = MagicMock(to_dict=MagicMock(return_value=mock_data))

        response = self.app.get('/leaderboard')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Player 1', response.data)
        self.assertIn(b'Player 2', response.data)

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'NBA Player Sentiment Analysis', response.data)

    def test_invalid_player(self):
        with patch('utils.nba_stats.get_player_info', side_effect=ValueError("Player not found")):
            response = self.app.post('/analyze', data={
                'player_name': 'Invalid Player',
                'season': '2022/2023'
            })
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Player not found')

    def test_invalid_season(self):
        with patch('utils.nba_stats.get_player_info', side_effect=ValueError("No stats found for this season")):
            response = self.app.post('/analyze', data={
                'player_name': 'LeBron James',
                'season': '1900/1901'
            })
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'No stats found for this season')

if __name__ == '__main__':
    unittest.main()