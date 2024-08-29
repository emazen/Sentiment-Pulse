import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datetime import datetime
from functools import lru_cache

# Load pre-trained model and tokenizer
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


def analyze_sentiment(reddit_data):
    sentiment_data = []
    total_sentiment = 0

    texts = [post['title'] for post in reddit_data]  # Analyzing only the titles for speed
    sentiments = process_in_batches(texts)

    for post, sentiment in zip(reddit_data, sentiments):
        date = datetime.fromtimestamp(post['created_utc'])
        sentiment_data.append((date, sentiment, post['title'], post['url']))
        total_sentiment += sentiment

    overall_sentiment = total_sentiment / len(sentiments) if sentiments else 0
    sentiment_label = "Positive" if overall_sentiment > 0 else "Negative"

    return sorted(sentiment_data), overall_sentiment, sentiment_label

def process_in_batches(texts, batch_size=32):
    sentiments = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
        scores = torch.softmax(outputs.logits, dim=1)
        batch_sentiments = scores[:, 2] - scores[:, 0]  # Positive scores - Negative scores
        sentiments.extend(batch_sentiments.cpu().tolist())
    return sentiments