from enum import auto
from altair.vegalite.v4.schema.core import Orientation
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import plotly.express as px
import seaborn as sns
sns.set_style('darkgrid')
import streamlit as st



@st.cache
def load_games():
    """ function to clean the data and load into pandas dataframe """
    app_data = pd.read_csv('./data/games.csv')
    # rename few columns to something recognisable
    app_data.rename(columns={'title': 'appName', 'genre': 'category'}, inplace=True)
    # Extract month and year
    app_data[['month', 'year']] = app_data['released'].str.split(',', expand=True)
    # convert released date to datetime
    app_data['released'] = pd.to_datetime(app_data['released']) 
    # extract weekday
    app_data['day_of_week'] = app_data['released'].apply(lambda time: time.dayofweek)
    mapper = {
    0.0: 'Monday', 1.0: 'Tuesday', 2.0: 'Wednesday', 3.0: 'Thursday',
    4.0: 'Friday', 5.0: 'Saturday', 6.0: 'Sunday',
    }
    # map all integer variables
    # following python weekday numbering
    app_data['day_of_week'] = app_data['day_of_week'].replace(mapper)
    # convert install field to numeric
    app_data['installs'] = app_data['installs'].str.replace('+', '')
    app_data['installs'] = app_data['installs'].str.replace(',', '').astype('int')

    return app_data

def game_cost(app_data):
    """Display the ratio of paid games to free ones"""
    gameCost = app_data['free'].value_counts()
    fig, ax = plt.subplots()
    categories = ["Free","Paid"]
    colors = ["lightblue", "lightgreen"]
    explode = (0, 0.1)
    ax = plt.pie(x=gameCost, labels=categories, colors=colors, 
        explode=explode, autopct='%1.1f%%', shadow=False, startangle=120)
    # plt.gcf().set_size_inches(7,7)
    return fig # each time I use "return fig", I get an AttributeError

def genre(app_data):
    fig = plt.figure(figsize=(11,7))
    plt.xticks(rotation=90)
    splot = sns.countplot(x=app_data.category, palette='rainbow')
    for p in splot.patches:
        splot.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), \
                   ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
    plt.gcf().set_size_inches(10,7)
    plt.ylabel('Total sum')
    st.title('Game Types on Playstore')
    plt.tight_layout()
    return fig

def count_installs(app_data): # previous plot keeps appearing on top of this
    fig, ax = plt.subplots()
    ax = sns.countplot(x=app_data.installs, color='blue')
    plt.xticks(rotation=90)
    # plt.gcf().set_size_inches(15,7)
    return fig

## IT TAKES TIME TO RUN
# def installs_per_type(app_data):
#     sns.displot(x=app_data.installs, hue=app_data.category, row=app_data.category, discrete=True)
#     plt.gcf().set_size_inches(20,45)
#     return plt



