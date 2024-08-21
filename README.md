# NBA Player Sentiment Analysis

## Description
This web application visualizes public opinion of NBA players over a season by performing sentiment analysis on social media data and correlating it with player performance statistics. It provides insights into the relationship between a player's on-court performance and public perception.

## Features
- Sentiment analysis of Reddit posts about NBA players
- Integration with NBA statistics API for player performance data
- Interactive visualizations of sentiment trends and player statistics
- Sentiment leaderboard comparing multiple players
- Correlation analysis between public sentiment and player performance

## Technology Stack
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- APIs: Reddit API, NBA Statistics API
- Data Analysis: Transformers library for sentiment analysis
- Visualization: Matplotlib, mpld3

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/nba-player-sentiment-analysis.git
   cd nba-player-sentiment-analysis
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open a web browser and navigate to `http://localhost:5003`

## Usage
1. Enter an NBA player's name in the search box
2. Select a season for analysis
3. Click "Analyze" to view sentiment analysis results and player statistics

## Testing
Run the test suite using:
```
python -m unittest discover tests
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Transformers library by Hugging Face
- PRAW (Python Reddit API Wrapper)
- NBA API
- Matplotlib and mpld3 for visualizations
