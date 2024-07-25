import matplotlib.pyplot as plt
from wordcloud import WordCloud
import mpld3
from mpld3 import plugins

import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import json

import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import json

def create_sentiment_chart(sentiment_data):
    if not sentiment_data:
        return '/static/images/no_data.png'
    
    dates, sentiments, titles, urls = zip(*sentiment_data)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create line plot
    ax.plot(dates, sentiments, '-', alpha=0.5)
    
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
    
    # Add custom JavaScript to make tooltips persist on click and open link on double-click
    html = html.replace('</body>', '''
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var svg = document.querySelector("#figure svg");
            var tooltip = document.querySelector(".mpld3-tooltip");
            var isTooltipVisible = false;
            var lastClickTime = 0;
            var urls = %s;
            
            svg.addEventListener('click', function(e) {
                var now = new Date().getTime();
                if (e.target.tagName === 'circle') {
                    var index = Array.from(e.target.parentNode.children).indexOf(e.target);
                    if (now - lastClickTime < 300) {
                        // Double click
                        window.open(urls[index], '_blank');
                    } else {
                        // Single click
                        if (isTooltipVisible) {
                            tooltip.style.visibility = 'hidden';
                            isTooltipVisible = false;
                        } else {
                            setTimeout(function() {
                                tooltip.style.visibility = 'visible';
                                isTooltipVisible = true;
                            }, 100);
                        }
                    }
                    lastClickTime = now;
                } else if (!tooltip.contains(e.target)) {
                    tooltip.style.visibility = 'hidden';
                    isTooltipVisible = false;
                }
            });
        });
    </script>
    </body>
    ''' % json.dumps(urls))
    
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