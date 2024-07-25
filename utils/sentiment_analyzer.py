import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import datetime
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_vader_lexicon():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        print("Downloading VADER lexicon...")
        nltk.download('vader_lexicon', quiet=True)

download_vader_lexicon()

def analyze_sentiment(reddit_data):
    sid = SentimentIntensityAnalyzer()
    sentiment_data = []

    for post in reddit_data:
        text = post['title'] + ' ' + post['text']
        sentiment_scores = sid.polarity_scores(text)
        
        # Use the compound score as the sentiment value
        sentiment_value = sentiment_scores['compound']
        
        date = datetime.datetime.fromtimestamp(post['created_utc'])
        sentiment_data.append((date, sentiment_value, post['title'], post['url']))

    return sorted(sentiment_data)