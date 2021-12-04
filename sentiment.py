from pandas.tseries.offsets import SemiMonthBegin
from google_play_scraper import reviews_all
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
    allResults = []
    results = reviews_all(id)

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


# def process_review(text):
#     """This function returns a clean text for all the reviews"""
#     # remove non-letters
#     letters = re.sub("[^a-zA-Z", " ", text)
#     # remove punctation
#     filtered_text = "".join([char for char in letters if char not in string.punctuation])
#     # convert text to lowercase
#     text_lower = filtered_text.lower()
#     # filter out stopwords
#     words_stop = set(stopwords.words("english"))
#     # remove stopwords
#     meaningful_words = [w for w in text_lower if not w in words_stop]
#     # join the entire word back to string
#     return(" ".join(meaningful_words))


def sentiment_scores(sentence):
 
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
    else:
        result="neutral"
    return result


def sentiment_chart(df):
    """Visualizes the sentiments from an app's reviews in form of a pie chart""" 
    
    # get the sentiments from the reviews i.e positive, neutral and negative
    # df["Sentiment"] = df["review"].apply(sentiment_scores)  

    # using the dataframe to plot a pie chart of the sentiments
    colors = ['lightcoral', 'lightskyblue', 'green']
    pie, ax = plt.subplots()
    plt.xticks(rotation='horizontal')
    explode = (0.1, 0, 0)
    labels = 'negative', 'neutral', 'positive'
    plt.pie(x=df.groupby("Sentiment").count()['review'], autopct="%1.1f%%", \
                    shadow=True, labels=labels, \
                    colors=colors, explode=explode, startangle=120)
    plt.title('App Reviews Sentiments', size=15)
    plt.show()


def sentiments_and_word_cloud(df):

    pos_sent_mask = "./asset/thumb_up.png"
    neg_sent_mask = "./asset/thumb_down.png"
    neu_sent_mask = "./asset/thumb_side.png"

    
    sentiment = df["Sentiment"].value_counts().index[0]

    if sentiment=="negative":
        img = np.array(Image.open(neg_sent_mask))

    elif sentiment=="neutral":
        img = np.array(Image.open(neu_sent_mask))

    else:
        img = np.array(Image.open(pos_sent_mask))
    
    img = img+1*255

    wc = WordCloud(background_color=None, max_font_size=100, max_words=10000, mask=img,
                    mode="RGBA", width=1600, height=800, stopwords=stopwords, colormap=matplotlib.cm.Accent)

    
    wc.generate(' '.join(df["review"]))
    fig, ax = plt.subplots()
    ax = plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    return fig


# if __name__ =='__main__':  
#     app_name = 'tiktok'
#    # id = 'com.invest.bamboo'
#     df = AppleUsers_review(app_name)
    #request_review(id)
   # fetch_review(id)
    #process_review()