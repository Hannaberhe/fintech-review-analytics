from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from collections import Counter

analyzer = SentimentIntensityAnalyzer()

def add_sentiment(df):
    sentiments = []
    for text in df['review']:
        score = analyzer.polarity_scores(str(text))
        if score['compound'] >= 0.05:
            label = 'positive'
        elif score['compound'] <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        sentiments.append({'sentiment_label': label, 'sentiment_score': score['compound']})
    
    df['sentiment_label'] = [s['sentiment_label'] for s in sentiments]
    df['sentiment_score'] = [s['sentiment_score'] for s in sentiments]
    return df

def assign_theme(review_text):
    text = str(review_text).lower()
    if any(w in text for w in ['login', 'password', 'otp', 'verify', 'register']):
        return 'Account Access'
    if any(w in text for w in ['transfer', 'payment', 'send', 'balance', 'transaction']):
        return 'Transaction Issues'
    if any(w in text for w in ['crash', 'slow', 'loading', 'freeze', 'bug', 'error']):
        return 'App Performance'
    if any(w in text for w in ['easy', 'simple', 'nice', 'good', 'great', 'love']):
        return 'User Experience'
    if any(w in text for w in ['fingerprint', 'update', 'add', 'need', 'please']):
        return 'Feature Request'
    return 'General Feedback'

if __name__ == "__main__":
    df = pd.read_csv('data/raw/reviews.csv')
    print(f"Loaded {len(df)} reviews")
    df = add_sentiment(df)
    df['theme'] = df['review'].apply(assign_theme)
    df.to_csv('data/raw/reviews_with_sentiment.csv', index=False)
    print("\nSentiment counts:")
    print(df['sentiment_label'].value_counts())
    print("\nTheme counts:")
    print(df['theme'].value_counts())
    print("\nDone!")
