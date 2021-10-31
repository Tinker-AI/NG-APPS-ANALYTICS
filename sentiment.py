from pandas.tseries.offsets import SemiMonthBegin
from google_play_scraper import reviews_all
from google_play_scraper import app
import re
import string
from nltk.corpus import stopwords
import pandas as pd
# nltk.download('stopwords)


def fetch_review(id):
    """This function receives the app id as an argument to return all the reviews given for that app
    this api fetches 200 review per request"""
    results = reviews_all(id) 
    for x, item in enumerate(results):
        review_list = []
        review = item['content']
        review_list.append(review)
        #print(review_list)
        for idx, row in enumerate(review_list):
            row = ''.join(row)
            word_dict = {'text': row}
            sentiment_df = pd.DataFrame(word_dict.items(), columns=['metric', 'value'])
        #print(review_list)
    return sentiment_df       
    
        
def request_review(package_name):
    """This function takes the app id as an input to return all the reviews that were 
    given for that app by users. This api returns 40 reviews per request"""
    result = app(package_name)
    keys = ['comments']
    review = {key: result[key] for key in keys }
    review_df = pd.DataFrame(review)
        
    return review_df
               

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
    id = 'com.invest.bamboo'
    #request_review(id)
    fetch_review(id)
    #process_review()
