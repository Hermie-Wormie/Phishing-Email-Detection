'''work in progress'''

from pandas import Series, to_datetime, read_csv, concat
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

def label_distrbution(df):
    try:
        df['label'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
        plt.title('Distribution of Phishing vs Legitimate Emails')
        plt.xlabel('Email Type')
        plt.ylabel('Count')
        plt.xticks(rotation=0)
        plt.show()
    except Exception as e:
        print(e)

def sender_domain(df):
    try:
        df = df.dropna(subset=['sender'])
        df = df[df['sender'].str.strip() != '']
        df['domain'] = df['sender'].apply(lambda x: x.split('@')[-1])
        domain_counts = df['domain'].value_counts().head(10)

        domain_counts.plot(kind='bar', color='orange')
        plt.title('Top Sender Domains')
        plt.xlabel('Domain')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.show()
    
    except Exception as e:
        print(e)

# content length graph looks a bit weird

# def email_content_length(df):
#     try:
#         df = df.dropna(subset=['body'])
#         df = df[df['body'].str.strip() != '']
#         df['content_length'] = df['body'].apply(lambda x: len(x))

#         plt.figure(figsize=(10, 5))
#         sns.boxplot(x='label', y='content_length', data=df)
#         plt.title('Length of Email Content')
#         plt.xlabel('Email Type')
#         plt.ylabel('Content Length')
#         plt.show()
#     except Exception as e:
#         print(e)

def feature_frequency(df):
    try:
        df = df.dropna(subset=['body'])
        df = df[df['body'].str.strip() != '']
        phishing_text = ' '.join(df[df['label'] == 1]['body'])
        legit_text = ' '.join(df[df['label'] == 0]['body'])

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
    except Exception as e:
        print(e)

# link analysis graph looks weird too

# def link_analysis(df):
#     try:
#         df = df.dropna(subset=['url'])
#         df = df[df['url'].str.strip() != '']
#         df['link_count'] = df['url'].apply(lambda x: x.count('http'))
#         plt.figure(figsize=(12, 6))

#         plt.hist(df[df['label'] == 1]['link_count'], bins=30, alpha=0.6, label='Phishing', color='red')
#         plt.hist(df[df['label'] == 0]['link_count'], bins=30, alpha=0.6, label='Legitimate', color='blue')
#         plt.title('Distribution of Link Counts')
#         plt.xlabel('Number of Links')
#         plt.ylabel('Frequency')
#         plt.legend()
#         plt.ylim(0, df['link_count'].value_counts().max() + 5)
#         plt.grid(axis='y', alpha=0.75)
#         plt.show()
#     except Exception as e:
#         print(e)

def time_count(df):
    try:
        df['date'] = to_datetime(df['date'], format='%a, %d %b %Y %H:%M:%S %z', errors='coerce', utc=True)
        df = df.dropna(subset=['date'])
        df['time_sent'] = to_datetime(df['date']).dt.hour

        hour_counts = df['time_sent'].value_counts().sort_index()
        hour_counts.plot(kind='line', marker='o')
        plt.title('Frequency of Emails Sent by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Count')
        plt.xticks(range(24))
        plt.grid()
        plt.show()
    except Exception as e:
        print(e)


def sentiment_analysis(df):
    try:
        sia = SentimentIntensityAnalyzer()
        df = df.dropna(subset=['body'])
        df = df[df['body'].str.strip() != '']
        df['sentiment'] = df['body'].apply(lambda x: sia.polarity_scores(x)['compound'])

        sns.barplot(x='label', y='sentiment', data=df)
        plt.title('Average Sentiment Scores by Email Type')
        plt.ylabel('Average Sentiment Score')
        plt.show()
    except Exception as e:
        print(e)

def analyze_sentiment(text):
    """Analyze sentiment of the given text using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def visualise_sentiment2(df):
    try:
        
        df = df.dropna(subset=['body'])
        df = df[df['body'].str.strip() != '']
        # Apply the function to the content column
        df[['polarity', 'subjectivity']] = df['body'].apply(lambda x: analyze_sentiment(x)).apply(Series)

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
    except Exception as e:
        print(e)
        

def read_files(dataset: list):
    return concat(map(read_csv, dataset ), ignore_index=True)