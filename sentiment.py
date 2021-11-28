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
import json
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from PIL import Image
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)
stopwords.add("app")


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
    df = pd.DataFrame(allResults, columns=["review"])
    
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



#AISHA
def sentiment_scores(sentence):
    """This function calculates the sentiment scores for each review"""
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        result="positive"
    elif sentiment_dict['compound'] <= -0.05 :
        result="negative"
    else :
        result="neutral"
    return result


def sentiment_type(df):
    """This function returns takes a dataframe with reviews of an app, calculates and returns the appropriate sentiment type of each review"""
    
    df["Sentiment"] = df["review"].apply(sentiment_scores)
    return df


def sentiment_chart(df):
  """This function plots a pie chart of the sentiments gotten from an app's reviews"""

  data = df.groupby("Sentiment")["review"].count()
  data = data.sort_values(ascending = False)
  pie, ax = plt.subplots(figsize=[10, 10])
  plt.xticks(rotation='horizontal')
  explode = (0, 0.1, 0.1)
  labels = data.keys()
  fig = plt.pie(x=data, autopct="%.1f%%", shadow=True, labels=labels, explode=explode, pctdistance=0.5)
  plt.title('App Sentiments')
  return fig



#just trying out a single function here where an app ID is passed and it fetches the reviews, calculates the sentiment scores and plot the sentiment types
#combines the above functions but takes too long to run. Might not be beeded, depends on what you think. Also codes above may need correction.

# def sentiment_chart(id):
#   """This function plots a pie chart of the sentiments gotten from an app's reviews"""
  
#   # get the reviews for the app using the defined function
#   reviews = fetch_review(id)  
  
#   #get the sentiments from the reviews i.e positive, neutral and negative
#   reviews["Sentiment"] = reviews["review"].apply(sentiment_scores)  

#   #using the dataframe to plot a pie chart of the sentiments
#   data = reviews.groupby("Sentiment")["review"].count()
#   data = data.sort_values(ascending = False)
#   pie, ax = plt.subplots(figsize=[10, 10])
#   plt.xticks(rotation='horizontal')
#   explode = (0, 0.1, 0.1)
#   labels = data.keys()
#   fig = plt.pie(x=data, autopct="%.1f%%", shadow=True, labels=labels, explode=explode, pctdistance=0.5)
#   plt.title('App Sentiments')
#   return fig



if __name__ =='__main__':  
    app_name = 'tiktok'
   # id = 'com.invest.bamboo'
    AppleUsers_review(app_name)
    #request_review(id)
   # fetch_review(id)
    #process_review()
