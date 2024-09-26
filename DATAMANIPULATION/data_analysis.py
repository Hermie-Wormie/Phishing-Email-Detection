'''work in progress'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

def label_distrbution(df):
    df['label'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Distribution of Phishing vs Legitimate Emails')
    plt.xlabel('Email Type')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.show()

def sender_domain(df):
    df['domain'] = df['sender'].apply(lambda x: x.split('@')[-1])
    domain_counts = df['domain'].value_counts().head(10)

    domain_counts.plot(kind='bar', color='orange')
    plt.title('Top Sender Domains')
    plt.xlabel('Domain')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

def email_content_length(df):
    df['content_length'] = df['body'].apply(len)

    plt.figure(figsize=(10, 5))
    sns.boxplot(x='label', y='content_length', data=df)
    plt.title('Length of Email Content')
    plt.xlabel('Email Type')
    plt.ylabel('Content Length')
    plt.show()

def feature_frequency(df):
    phishing_text = ' '.join(df[df['label'] == 'phishing']['content'])
    legit_text = ' '.join(df[df['label'] == 'legitimate']['content'])

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Phishing Emails Word Cloud')
    plt.imshow(WordCloud().generate(phishing_text), interpolation='bilinear')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Legitimate Emails Word Cloud')
    plt.imshow(WordCloud().generate(legit_text), interpolation='bilinear')
    plt.axis('off')

    plt.show()

def link_analysis(df):
    df['link_count'] = df['url'].apply(lambda x: x.count('http'))

    plt.hist(df[df['label'] == 'phishing']['link_count'], bins=20, alpha=0.5, label='Phishing', color='red')
    plt.hist(df[df['label'] == 'legitimate']['link_count'], bins=20, alpha=0.5, label='Legitimate', color='blue')
    plt.title('Distribution of Link Counts')
    plt.xlabel('Number of Links')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

def sentiment_analysis(df):
    sia = SentimentIntensityAnalyzer()
    df['sentiment'] = df['body'].apply(lambda x: sia.polarity_scores(x)['compound'])

    sns.barplot(x='label', y='sentiment', data=df)
    plt.title('Average Sentiment Scores by Email Type')
    plt.ylabel('Average Sentiment Score')
    plt.show()

def analyze_sentiment(text):
    """Analyze sentiment of the given text using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def visualise_sentiment2(df):
    # Apply the function to the content column
    df[['polarity', 'subjectivity']] = df['body'].apply(lambda x: analyze_sentiment(x)).apply(pd.Series)

    # Visualize the sentiment analysis results
    plt.figure(figsize=(12, 6))

    # Polarity
    plt.subplot(1, 2, 1)
    sns.boxplot(x='label', y='polarity', data=df)
    plt.title('Polarity Scores by Email Type')
    plt.ylabel('Polarity Score')

    # Subjectivity
    plt.subplot(1, 2, 2)
    sns.boxplot(x='label', y='subjectivity', data=df)
    plt.title('Subjectivity Scores by Email Type')
    plt.ylabel('Subjectivity Score')

    plt.tight_layout()
    plt.show()