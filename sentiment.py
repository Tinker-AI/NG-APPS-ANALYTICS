from pandas.tseries.offsets import SemiMonthBegin
from google_play_scraper import reviews_all
from google_play_scraper import app
from app_store_scraper import AppStore
import re
import string
import numpy as np
from nltk.corpus import stopwords
import pandas as pd
# nltk.download('stopwords)



def fetch_review(id):
    """
    Fetches all reviews of an app

    Args:
    id: google playstore app id

    Returns:
    All reviews of the app in form of a dataframe.
    """
    allResults = []
    results = reviews_all(id) 
    for i in range(len(results)):
      result = results[i]["content"]
      allResults.append(result)
    df = pd.Series(allResults, name="content")
    
    return df
      
    
        
def request_review(package_name):
    """This function takes the app id as an input to return all the reviews that were 
    given for that app by users. This api returns 40 reviews per request"""
    result = app(package_name)
    keys = ['comments']
    review = {key: result[key] for key in keys }
    review_df = pd.DataFrame(review)
        
    return review_df


def AppleUsers_review(app_name):
    """
    This function fetches all the reviews given for an app in the apple store

    Args:
        app_name: name of the app in App store

    Returns:
        All reviews for the app in the form of a dataframe
    
    """
    RESULT = []
    app = AppStore(country="ng", app_name=app_name)
    app.review(how_many=100)
    for i in range(len(app.reviews)):
        response = app.reviews[i]['review']
        RESULT.append(response)
    df = pd.Series(RESULT, name='Reviews')
    
    return df

               

def process_review(text):
    """This function returns a clean text for all the reviews"""
    # remove non-letters
    letters = re.sub("[^a-zA-Z", " ", text)
    # remove punctation
    filtered_text = "".join([char for char in letters if char not in string.punctuation])
    # convert text to lowercase
    text_lower = filtered_text.lower()
    # filter out stopwords
    words_stop = set(stopwords.words("english"))
    # remove stopwords
    meaningful_words = [w for w in text_lower if not w in words_stop]
    # join the entire word back to string
    return(" ".join(meaningful_words))




if __name__ =='__main__':  
    app_name = 'tiktok'
   # id = 'com.invest.bamboo'
    AppleUsers_review(app_name)
    #request_review(id)
   # fetch_review(id)
    #process_review()
