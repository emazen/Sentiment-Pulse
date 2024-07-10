from textblob import TextBlob
import datetime

def analyze_sentiment(reddit_data):
    sentiment_data = []

    for post in reddit_data:
        text = post['title'] + ' ' + post['text']
        sentiment = TextBlob(text).sentiment.polarity
        date = datetime.datetime.fromtimestamp(post['created_utc'])
        sentiment_data.append((date, sentiment))

    return sorted(sentiment_data)