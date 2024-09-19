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
        senders.dropna()
        senders.drop_duplicates()
        senders.to_csv(r'CLEANDATA\senders.csv',index=False)
    except Exception as e:
        pass

def extract_subject(subjects):
    try:
        subjects.drop(columns=['sender','body','urls'],inplace=True)
    except KeyError:
        subjects.drop(columns=['body'],inplace=True)
    except Exception as e:
        pass
    finally:
        subjects.dropna()
        subjects.drop_duplicates()
        subjects.to_csv(r'CLEANDATA\subjects.csv',index=False)

def extract_body(words):
    try:
        words.drop(columns=['url'],inplace=True)
    except KeyError:
        pass
    except Exception as e:
        pass
    finally:
        words.dropna()
        words.drop_duplicates()
        words.to_csv(r'CLEANDATA\body.csv',index=False)

def extract_urls(url):
    try:
        url.drop(columns=['body'],inplace=True)
        url.dropna()
        url.to_csv(r'CLEANDATA\urls.csv',index=False)
    except Exception as e:
        pass

def replace_urls(body):
    url_dict = {}
    
    try:

        body.drop(columns=['sender','subject','urls'],inplace=True)
    
    except KeyError:

        body.drop(columns=['subject'],inplace=True)

    except Exception as e:
        pass

    try:
        for i in range(body.shape[0]):

            urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body.values[i][0])

            if urls != []: 
                
                url_dict.update({i:urls})
                body.loc[i,"body"] = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', body.loc[i,"body"])
            
            else: url_dict.update({i:''})

            # will be editing soon
            tokens = body.copy()
            body.loc[i,"body"] = sanitize_whitespace(body.loc[i,"body"])
        
        if url_dict != {}:
            body['url'] = body.index.map(url_dict)
            extract_urls(body.copy())
        
        extract_body(body.copy())
    
    except Exception as e:
        pass

def sanitize_whitespace(input_string):
    """
    Remove extra whitespace
    """
    lines = input_string.split('\n')
    for index, line  in enumerate(lines):
        if line=='.':
            lines.remove(line)
            for i in range(1, len(lines)): # check for lines that contain text
                if (lines[index-i] != ''):
                    lines[index-i] += '.'
                    break
                    
    output_string = '\n'.join(lines)
    
    return output_string.strip()

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

        try:
            # for csvs with "receiver" and "date" columns
            df.drop(columns=['receiver','date'],inplace=True)
                        
        except Exception as e:
            pass

        try:

            # extract_subject(df)
            replace_urls(df.copy())
            extract_sender(df.copy())
            extract_subject(df.copy())

            df.head(10)
        
        except Exception as e:
            pass


