import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

def create_sentiment_chart(sentiment_data):
    dates, sentiments = zip(*sentiment_data)
    plt.figure(figsize=(10, 6))
    plt.plot(dates, sentiments)
    plt.title('Sentiment Trend')
    plt.xlabel('Date')
    plt.ylabel('Sentiment')
    
    chart_path = 'static/images/sentiment_chart.png'
    plt.savefig(chart_path)
    plt.close()
    
    return '/' + chart_path

def create_word_cloud(reddit_data):
    text = ' '.join([post['title'] + ' ' + post['text'] for post in reddit_data])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    word_cloud_path = 'static/images/word_cloud.png'
    plt.savefig(word_cloud_path)
    plt.close()
    
    return '/' + word_cloud_path