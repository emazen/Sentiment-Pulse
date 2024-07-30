from flask import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import mpld3
from mpld3 import plugins

def create_sentiment_chart(sentiment_data):
    if not sentiment_data:
        return '/static/images/no_data.png'
    
    dates, sentiments, titles, urls = zip(*sentiment_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create line plot
    ax.plot(dates, sentiments, '-', alpha=0.5)

    plt.tight_layout()
    
    # Create scatter plot
    scatter = ax.scatter(dates, sentiments, c=sentiments, cmap='coolwarm', vmin=-1, vmax=1, s=50)
    
    ax.set_title('Sentiment Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment')
    
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

def create_points_chart(points_data):
    if not points_data:
        return '/static/images/no_data.png'
    
    dates, points = zip(*points_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, points, '-o')

    plt.tight_layout()
    
    ax.set_title('Points per Game')
    ax.set_xlabel('Date')
    ax.set_ylabel('Points')
    
    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()
    
    # Save the plot as HTML
    chart_path = 'static/images/points_chart.html'
    html = mpld3.fig_to_html(fig)
    
    with open(chart_path, 'w') as f:
        f.write(html)
    
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