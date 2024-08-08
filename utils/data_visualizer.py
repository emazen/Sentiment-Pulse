import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
from mpld3 import plugins
import mpld3

def create_sentiment_chart(sentiment_data, overall_sentiment, sentiment_label):
    if not sentiment_data:
        return '/static/images/no_data.png'
    
    dates, sentiments, titles, urls = zip(*sentiment_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Convert dates to numbers for linear regression
    dates_num = mdates.date2num(dates)
    
    # Create line plot
    ax.plot(dates, sentiments, '-', alpha=0.5)

    # Create scatter plot
    scatter = ax.scatter(dates, sentiments, c=sentiments, cmap='coolwarm', vmin=-1, vmax=1, s=50)
    
    # Calculate and plot trend line
    z = np.polyfit(dates_num, sentiments, 1)
    p = np.poly1d(z)
    ax.plot(dates, p(dates_num), "r--", alpha=0.8, label='Trend')
    
    ax.set_title('Sentiment Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment')
    
    plt.tight_layout()
    
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