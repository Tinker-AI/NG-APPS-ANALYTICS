from pandas.tseries.offsets import SemiMonthBegin
from google_play_scraper import reviews_all, Sort, reviews
from app_store_scraper import AppStore
import re
import string
import json
from nltk.corpus import stopwords
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)
stopwords.add("app")


def fetchPlaystorereviews(id):
    """
    Fetches all reviews of an app in Google Playstore

    Args:
    id: google playstore app id

    Returns:
    All reviews of the app in form of a dataframe.
    """
    results, token = reviews(
      id,           # found in app's url
      lang='en',        # defaults to 'en'
      country='ng',     # defaults to 'us'
      sort=Sort.NEWEST, # start with most recent
      count=200       # batch size
    )

    allResults = []

    # results = reviews_all(
    # id,
    # #sleep_milliseconds=0, # defaults to 0
    # lang='en', # defaults to 'en'
    # country='ng' # defaults to 'us'
    # #sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
    #  # defaults to None(means all score)
    # )

    for i in range(len(results)):
        result = results[i]["content"]
        allResults.append(result)
    df = pd.DataFrame(allResults, columns=["review"])
    
    return df


def fetchAppstorereviews(app_name):
    """
    Fetches all reviews of an app in Appstore

    Args:
        app_name: name of the app in App store

    Returns:
        All reviews for the app in the form of a dataframe
    
    """
    RESULT = []
    app = AppStore(country="ng", app_name=app_name)
    app.review(how_many=1000)
    for i in range(len(app.reviews)):
        response = app.reviews[i]['review']
        RESULT.append(response)
    df = pd.DataFrame(RESULT, columns=['review'])
    
    return df


def remove_newline(review):
    return re.sub('\n', ' ', str(review.lower()))
def remove_symbols(review):
    re.sub(r'^\x00-\x7F+', ' ', review)
    return re.sub(r'[@!.,(\/&)?:#*...-;'']', '', str(review)) 
def remove_urls(review):
    return re.sub(r'http\S+', '', str(review))
 

def preprocessReview(review):
    review = remove_urls(review)
    review = remove_symbols(review)
    review = remove_newline(review)

    return review


# def sentiment_scores(sentence):
 
    # # Create a SentimentIntensityAnalyzer object.
    # sid_obj = SentimentIntensityAnalyzer()
 
    # # polarity_scores method of SentimentIntensityAnalyzer
    # # object gives a sentiment dictionary.
    # # which contains pos, neg, neu, and compound scores.
    # sentiment_dict = sid_obj.polarity_scores(sentence)
 
    # # decide sentiment as positive, negative and neutral
    # if sentiment_dict['compound'] >= 0.05 :
    #     result="positive"
    # elif sentiment_dict['compound'] <= -0.05 :
    #     result="negative"
    # else:
    #     result="neutral"
    # return result

def sentiment_scores(sentence):
    """This function calculates the sentiment scores for each review"""
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['neu'] > 0.80 and sentiment_dict['neu'] > sentiment_dict['pos'] and sentiment_dict['neu'] > sentiment_dict['neg']:
        result="neutral"

    elif sentiment_dict['pos'] > sentiment_dict['neg']:
        result="positive"
    else:
        result="negative"
    return result


def sentiment_chart(df):
    """Visualizes the sentiments from an app's reviews in form of a pie chart"""  

    # using the dataframe to plot a pie chart of the sentiments
    colors = ['lightcoral', 'lightskyblue', 'green']
    pie, ax = plt.subplots()
    plt.xticks(rotation='horizontal')
    x = df.groupby("Sentiment").count()['cleanReview']
    
    labels = list(df["Sentiment"].unique())
    labels = labels[::-1]
    colors = ['lightcoral', 'lightskyblue', 'green']

    plt.pie(x=x, autopct="%1.1f%%", \
                    shadow=True, labels=labels, \
                    colors=colors, explode=None, startangle=120)
    plt.title('App Reviews Sentiments', size=15)
    plt.show()
 

def sentiments_and_word_cloud(df):

    pos_sent_mask = "./asset/thumb_up.png"
    neg_sent_mask = "./asset/thumb_down.png"
    neu_sent_mask = "./asset/thumb_side.png"

    
    # sentiment = df["Sentiment"].value_counts().index[0]
    sentiment = df.groupby("Sentiment").count()['cleanReview'].index[-1]

    return sentiment

    # if sentiment=="negative":
    #     img = np.array(Image.open(neg_sent_mask))

    # elif sentiment=="positive":
    #     img = np.array(Image.open(pos_sent_mask))

    # else:
    #     img = np.array(Image.open(neu_sent_mask))
    
    # img = img+1*255

    # wc = WordCloud(background_color=None, max_font_size=100, max_words=10000, mask=img,
    #                 mode="RGBA", width=1600, height=800, stopwords=stopwords, colormap=matplotlib.cm.Accent)

    
    # wc.generate(' '.join(df["cleanReview"]))
    # fig, ax = plt.subplots()
    # ax = plt.imshow(wc, interpolation='bilinear')
    # plt.axis("off")
    # return fig