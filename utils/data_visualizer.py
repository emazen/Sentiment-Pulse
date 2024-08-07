from datetime import time, datetime
import matplotlib.dates as mdates
import time
from flask import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import mpld3
from mpld3 import plugins

def create_sentiment_chart(sentiment_data, overall_sentiment, sentiment_label):
    if not sentiment_data:
        return '/static/images/no_data.png'
    
    dates, sentiments, titles, urls = zip(*sentiment_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create line plot
    ax.plot(dates, sentiments, '-', alpha=0.5)

    # Create scatter plot
    scatter = ax.scatter(dates, sentiments, c=sentiments, cmap='coolwarm', vmin=-1, vmax=1, s=50)
    
    ax.set_title('Sentiment Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment')
    
    # Add overall sentiment to the top right
    ax.text(0.98, 0.98, f"Overall Sentiment: {overall_sentiment:.2f}\n{sentiment_label}", 
            transform=ax.transAxes, ha='right', va='top', 
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))
    
    # Create tooltip HTML with only the title
    tooltip_html = [f"<div>{title}</div>" for title in titles]
    
    # Use the built-in HTML tooltip
    tooltip = plugins.PointHTMLTooltip(scatter, tooltip_html, css='''
        .mpld3-tooltip {
            background-color: white;
            border: 1px solid black;
            font-family: Arial;
            font-size: 12px;
            padding: 5px;
        }
    ''')
    plugins.connect(fig, tooltip)
    
    # Save the plot as HTML
    chart_path = 'static/images/sentiment_chart.html'
    html = mpld3.fig_to_html(fig)
    
    with open(chart_path, 'w') as f:
        f.write(html)
    
    plt.close()
    
    return '/' + chart_path

def create_points_chart(game_data):
    dates = [datetime.fromisoformat(date) for date, _ in game_data]
    points = [points for _, points in game_data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, points, marker='o')
    
    plt.title('Points per Game')
    plt.ylabel('Points')
    
    # Format x-axis to show dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    
    plt.gcf().autofmt_xdate()  
    plt.tight_layout()
    
    chart_path = 'static/points_chart.png'
    plt.savefig(chart_path)
    plt.close()
    
    return chart_path


def create_word_cloud(reddit_data, player_name):
    # Combine all text from reddit data
    text = ' '.join([post['title'] + ' ' + post['text'] for post in reddit_data])
    
    # Create a set of stopwords
    stopwords = set(STOPWORDS)
    
    #Custom stopwords
    custom_stopwords = {
        player_name.lower(),  # Player's full name
        player_name.split()[0].lower(),  # Player's first name
        player_name.split()[1].lower(), # Player's last name
        'https',
        'http',
        'twitter',
        'youtube',
        'com',
        'www'
        'highlight'
        'discussion'
        'will'
        'game'
        'NBA'
    }
    stopwords.update(custom_stopwords)
    
    # Generate word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        stopwords=stopwords,
        min_font_size=10
    ).generate(text)
    
    # Create and save the figure
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    timestamp = int(time.time())
    word_cloud_path = f'static/images/word_cloud_{timestamp}.png'
    plt.savefig(word_cloud_path, bbox_inches='tight')
    plt.close()
    
    return '/' + word_cloud_path