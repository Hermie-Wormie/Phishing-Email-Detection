'''work in progress'''

import os
import re
from pandas import read_csv
from pathlib import Path

from nltk import word_tokenize, download

# from bs4 import BeautifulSoup
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
count = 0

def extract_tokens(tokens):
    try:
        tokens.fillna('', inplace = True)
        tokens.drop_duplicates()
    except KeyError:
        pass
    except Exception as e:
        pass
    finally:
        if count == 0:
            tokens.to_csv(r'CLEANDATA\tokens.csv',index=False,mode='a')
        else:
            tokens.to_csv(r'CLEANDATA\tokens.csv',index=False,mode='a',headers=None)

def extract_data(words):
    try:
        words.fillna('', inplace = True)
        # words.dropna()
        words.drop_duplicates()
    except KeyError:
        pass
    except Exception as e:
        pass
    finally:
        if count == 0:
            words.to_csv(r'CLEANDATA\data-1.csv',index=False,mode='a')
        elif count > 2:
            words.to_csv(r'CLEANDATA\data-2.csv',index=False,mode='a',headers=None)
        elif count > 1:
            words.to_csv(r'CLEANDATA\data-2.csv',index=False,mode='a')
        else:
            words.to_csv(r'CLEANDATA\data-1.csv',index=False,mode='a',headers=None)

def replace_urls(body):
    url_dict = {}

    try:
        for i in range(body.shape[0]):

            urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body.loc[i,"body"])

            if urls != []: 

                urls = ','.join(urls)                
                url_dict.update({i:urls})
                body.loc[i,"body"] = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', body.loc[i,"body"])
                body.loc[i,"body"] = re.sub(r'\n', ' ', body.loc[i,"body"])
            
            else: url_dict.update({i:''})

            # will be editing soon
            tokens = (body.copy())
        
        if url_dict != {}:
            body.insert(3, 'url', body.index.map(url_dict))
        
        extract_data(body.copy())
    
    except Exception as e:
        pass

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
        df = read_csv(data)
        # df.info()
        
        df = kill_duplicates(df)
        if 'sender' not in df.columns: df.insert(0,'sender',df.index.map({x:'' for x in range(df.shape[0])}))

        try:
            # for csvs with "receiver" and "date" columns
            df.drop(columns=['receiver','date','urls'],inplace=True)
                        
        except Exception as e:
            pass

        try:

            replace_urls(df.copy())

            df.head(10)
            count += 1
        
        except Exception as e:
            pass


