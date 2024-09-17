'''work in progress'''

import os
import re
from pandas import read_csv, to_datetime
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

download('punkt', quiet=True)
download('stopwords', quiet=True)
# download('averaged_perceptron_tagger', quiet=True)
# download('wordnet', quiet=True)
# download('omw-1.4', quiet=True)


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

def handle_datetime(df):
    df['date'] = to_datetime(df['date'], format='%a, %d %b %Y %H:%M:%S %z', errors='coerce', utc=True)
            
    # Creating separate columns for Date and Time
    df['Date'] = df['date'].dt.date
    df['Time'] = df['date'].dt.time

    # Handling any remaining NaT values (if any)
    df = df.dropna(subset=['date'])
    
    return df

def kill_duplicates(df):
    df_new = df.drop_duplicates()
    
    return df_new

def main(dataset: list):

    for data in dataset:
        df = read_csv(data)
        # df.info()
        
        df = kill_duplicates(df)

        try:
            df.drop(columns=['receiver','date'],inplace=True)
            df = handle_datetime(df)
            
        except Exception as e:
            continue


