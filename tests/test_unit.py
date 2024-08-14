import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from utils import reddit_scraper, sentiment_analyzer, data_visualizer, nba_stats

class TestRedditScraper(unittest.TestCase):
    @patch('praw.Reddit')
    def test_get_reddit_data(self, mock_reddit):
        mock_subreddit = MagicMock()
        mock_reddit.return_value.subreddit.return_value = mock_subreddit
        mock_submission = MagicMock()
        mock_submission.title = "Test Title"
        mock_submission.selftext = "Test Text"
        mock_submission.created_utc = 1234567890
        mock_submission.url = "https://test.com"
        mock_subreddit.search.return_value = [mock_submission]

        result = reddit_scraper.get_reddit_data("Test Player")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], "Test Title")
        self.assertEqual(result[0]['text'], "Test Text")
        self.assertEqual(result[0]['created_utc'], 1234567890)
        self.assertEqual(result[0]['url'], "https://test.com")

# Failing for now
class TestSentimentAnalyzer(unittest.TestCase):
    @patch('torch.softmax')
    @patch('transformers.AutoModelForSequenceClassification.from_pretrained')
    @patch('transformers.AutoTokenizer.from_pretrained')
    def test_analyze_sentiment(self, mock_tokenizer, mock_model, mock_softmax):
        mock_tokenizer.return_value.return_value = {'input_ids': MagicMock(), 'attention_mask': MagicMock()}
        mock_model.return_value.return_value = MagicMock(logits=MagicMock())
        mock_softmax.return_value = MagicMock(cpu=MagicMock(return_value=MagicMock(numpy=MagicMock(return_value=np.array([[0.3, 0.3, 0.4]])))))

        reddit_data = [{'title': 'Test', 'text': 'Test', 'created_utc': 1234567890, 'url': 'https://test.com'}]
        result, overall_sentiment, sentiment_label = sentiment_analyzer.analyze_sentiment(reddit_data)

        print(f"Result: {result}")

        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(overall_sentiment, 0.1, places=1)
        self.assertEqual(sentiment_label, 'Positive')

class TestDataVisualizer(unittest.TestCase):
    @patch('matplotlib.pyplot.savefig')
    @patch('mpld3.fig_to_html')
    def test_create_sentiment_chart(self, mock_fig_to_html, mock_savefig):
        mock_fig_to_html.return_value = '<div>Mock Chart</div>'
        sentiment_data = [
            (datetime(2023, 1, 1), 0.5, 'Title 1', 'https://test1.com'),
            (datetime(2023, 1, 2), -0.2, 'Title 2', 'https://test2.com')
        ]
        result = data_visualizer.create_sentiment_chart(sentiment_data, 0.15, 'Positive')
        
        self.assertTrue(result.endswith('sentiment_chart.html'))
        mock_fig_to_html.assert_called_once()
        mock_savefig.assert_not_called()

    @patch('matplotlib.pyplot.savefig')
    @patch('mpld3.fig_to_html')
    def test_create_points_chart(self, mock_fig_to_html, mock_savefig):
        mock_fig_to_html.return_value = '<div>Mock Chart</div>'
        game_data = [
            ('2023-01-01', 20),
            ('2023-01-02', 25)
        ]
        result = data_visualizer.create_points_chart(game_data)
        
        self.assertTrue(result.endswith('points_chart.html'))
        mock_fig_to_html.assert_called_once()
        mock_savefig.assert_not_called()

class TestNBAStats(unittest.TestCase):
    @patch('nba_api.stats.static.players.find_players_by_full_name')
    @patch('nba_api.stats.endpoints.playergamelog.PlayerGameLog')
    @patch('nba_api.stats.endpoints.playercareerstats.PlayerCareerStats')
    def test_get_player_info(self, mock_career_stats, mock_game_log, mock_find_players):
        mock_find_players.return_value = [{'id': '1234'}]
        
        mock_game_log_data = pd.DataFrame({
            'GAME_DATE': ['Jan 1, 2023', 'Jan 2, 2023'],
            'PTS': [20, 25]
        })
        mock_game_log.return_value.get_data_frames.return_value = [mock_game_log_data]
        
        mock_career_stats_data = pd.DataFrame({
            'SEASON_ID': ['2023-24'],
            'GP': [2],
            'PTS': [45],
            'REB': [10],
            'AST': [8]
        })
        mock_career_stats.return_value.get_data_frames.return_value = [mock_career_stats_data]

        result = nba_stats.get_player_info('Test Player', '2023-24')

        self.assertEqual(result['name'], 'Test Player')
        self.assertEqual(result['ppg'], 22.5)
        self.assertEqual(result['rpg'], 5.0)
        self.assertEqual(result['apg'], 4.0)
        self.assertEqual(len(result['game_data']), 2)

    def test_get_all_players(self):
        with patch('nba_api.stats.static.players.get_players', return_value=[{'full_name': 'Player 1'}, {'full_name': 'Player 2'}]):
            result = nba_stats.get_all_players()
            self.assertEqual(result, ['Player 1', 'Player 2'])

if __name__ == '__main__':
    unittest.main()