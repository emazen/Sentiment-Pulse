import praw
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

def get_reddit_data(player_name):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    subreddit = reddit.subreddit('nba')
    posts = []

    # Increase the limit to fetch more posts
    for submission in subreddit.search(player_name, limit=1000):
        posts.append({
            'title': submission.title,
            'text': submission.selftext,
            'created_utc': submission.created_utc,
            'url' : submission.url
        })

    return posts