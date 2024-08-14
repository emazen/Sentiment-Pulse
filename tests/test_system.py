import unittest
import json
from app import app
import time

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_full_analysis_flow(self):
        # Test the index page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'NBA Player Sentiment Analysis', response.data)

        # Test player name autocomplete
        response = self.app.get('/player-names?q=Leb')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('LeBron James', data)

        # Test full analysis
        response = self.app.post('/analyze', data={
            'player_name': 'LeBron James',
            'season': '2022/2023'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check if all expected keys are in the response
        expected_keys = ['player_info', 'overall_sentiment', 'sentiment_label', 'chart_path', 'points_chart_path']
        for key in expected_keys:
            self.assertIn(key, data)
        
        # Check player info
        self.assertEqual(data['player_info']['name'], 'LeBron James')
        self.assertIsInstance(data['player_info']['ppg'], float)
        self.assertIsInstance(data['player_info']['rpg'], float)
        self.assertIsInstance(data['player_info']['apg'], float)
        
        # Check sentiment data
        self.assertIsInstance(data['overall_sentiment'], float)
        self.assertIn(data['sentiment_label'], ['Positive', 'Negative', 'Neutral'])
        
        # Check chart paths
        self.assertTrue(data['chart_path'].endswith('.html'))
        self.assertTrue(data['points_chart_path'].endswith('.html'))

        # Test leaderboard
        response = self.app.get('/leaderboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sentiment Leaderboard', response.data)

    def test_error_handling(self):
        # Test with an invalid player name
        response = self.app.post('/analyze', data={
            'player_name': 'Invalid Player Name',
            'season': '2022/2023'
        })
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)

        # Test with an invalid season
        response = self.app.post('/analyze', data={
            'player_name': 'LeBron James',
            'season': '1900/1901'
        })
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_performance(self):
        start_time = time.time()
        response = self.app.post('/analyze', data={
            'player_name': 'LeBron James',
            'season': '2022/2023'
        })
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        
        # Check if the request was processed within a reasonable time (e.g., 10 seconds)
        self.assertLess(end_time - start_time, 10)

    def test_concurrent_requests(self):
        import threading

        def make_request():
            response = self.app.post('/analyze', data={
                'player_name': 'Stephen Curry',
                'season': '2022/2023'
            })
            self.assertEqual(response.status_code, 200)

        threads = []
        for _ in range(5):  # Simulate 5 concurrent requests
            thread = threading.Thread(target=make_request)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

if __name__ == '__main__':
    unittest.main()