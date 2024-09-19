'''work in progress'''

import os
import re
from pandas import read_csv
from pathlib import Path

from nltk import word_tokenize, download

from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

import random
random.seed(1746)

from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

download('punkt_tab', quiet=True)
download('stopwords', quiet=True)
# download('averaged_perceptron_tagger', quiet=True)
# download('wordnet', quiet=True)
# download('omw-1.4', quiet=True)

def extract_sender(senders):
    try:
        senders.drop(columns=['subject','body','urls'],inplace=True)
        senders.to_csv(r'..\CLEANDATA\senders.csv')
    except Exception as e:
        pass

def extract_subject(subjects):
    try:
        subjects.drop(columns=['subject','body','urls'],inplace=True)
        subjects.to_csv(r'..\CLEANDATA\subjects.csv')
    except Exception as e:
        pass

def extract_urls(body):
        
    try:

        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body['body'])

        if urls != []: body['url'] = urls
        
        body['body'] = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', body['body'])
    except Exception as e:
        pass
    
    return body

def tokenize(input_text):
    """
    Convert a string of text to a list with words.
    """
    lowercase = input_text.lower()
    token_list = word_tokenize(lowercase)
    clean_list = [word for word in token_list if len(re.findall(r'^[a-zA-Z0-9]+-?[\w-]*$', word)) == 1]
    
    return clean_list

def remove_stopwords(tokenized_text):
    """
    Remove stopwords from a list of words.
    """
    stop_words = stopwords.words('english')
    clean_list = [word for word in tokenized_text if word not in stop_words]
    
    return clean_list

def kill_duplicates(df):
    df_new = df.drop_duplicates()
    
    return df_new

def main(dataset: list):

    for data in dataset:
        df = read_csv(data,index_col=0)
        # df.info()
        
        df = kill_duplicates(df)

        try:
            # for csvs with "receiver" and "date" columns
            df.drop(columns=['receiver','date'],inplace=True)
                        
        except Exception as e:
            pass

        try:

            # extract_subject(df)
            extract_urls(df)

            df.head(10)
        
        except Exception as e:
            pass


