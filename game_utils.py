from enum import auto
from altair.vegalite.v4.schema.core import Orientation
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import plotly.express as px
import seaborn as sns
sns.set_style('darkgrid')
import streamlit as st
from google_play_scraper import app



@st.cache(allow_output_mutation=True)
def load_games():
    """ function to clean the data and load into pandas dataframe """
    app_data = pd.read_csv('./data/games.csv')
    # rename few columns to something recognisable
    app_data.rename(columns={'title': 'appName', 'genre': 'category', 'score': 'starRating'}, inplace=True)
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
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def count_installs(app_data): # previous plot keeps appearing on top of this
    fig, ax = plt.subplots()
    ax = sns.countplot(x=app_data.installs, color='blue')
    plt.xticks(rotation=45)
    # plt.gcf().set_size_inches(15,7)
    return fig

def top_cat(app_data):
    """ This function generates the top five most popular category and saves it to a list
    to generate plot to understand which of these category was downloaded the most
    """
    Top_5 = app_data.groupby('category').size().reset_index(name='Frequency').nlargest(5, 'Frequency')
    top_5 = Top_5['category'].tolist()
    top_pop = app_data.groupby('category')['installs'].agg(sum).loc[top_5].reset_index(name='Total Installs')
    # altair plot
    fig = alt.Chart(top_pop).mark_bar().properties(width=500, height=500).encode(
    x = 'category',
    y = 'Total Installs'
    )
    return fig

def mostInstalledCat(app_data):
    """ This function considers the overall category with the highest installation"""
    fig, ax = plt.subplots()
    plt.title('Total installation across all category')
    cat_data = app_data.groupby('category')['installs'].agg('sum').reset_index(name='Total Installs')
    ax = sns.barplot(y=cat_data['category'], x= cat_data['Total Installs'], color = 'cyan')
    return fig

def mostReviewedCat(app_data):
    """" This function is used to view the top five category with the most number of reviews"""
    cat_review = app_data.groupby('category', as_index=False)['reviews'].max().sort_values('reviews', ascending=False).head()
    fig, ax = plt.subplots()
    plt.title('Top most reviewed category')
    ax = sns.barplot(data=cat_review, x='reviews', y='category')
    return fig

def mostRatedCat(app_data):
    """This function returns a pie chart fig showing the top five most rated category"""
    cat_rating = app_data.groupby('category')['ratings'].count()
    cat_rating = cat_rating.sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    plt.xticks(rotation='horizontal')
    labels = cat_rating.keys()
    plt.pie(x=cat_rating, autopct="%.1f%%", labels=labels, pctdistance=0.9)
    #plt.title('Most Rated Category')
    return fig

def appType(app_data):
    """This function returns the most downloaded app between paid apps and free apps"""
    app_type = app_data.groupby('free')['installs'].count()
    fig, ax = plt.subplots()
    plt.xticks(rotation='horizontal')
    labels = ['Paid', 'Free']
    ax = plt.pie(x=app_type, autopct="%.1f%%", labels=labels, pctdistance=0.9)
    #plt.title('Paid apps vs free apps with respect to installation')
    return fig

def wkly_download(app_data):
    """ This function returns a bar chart showing weekly download trend"""
    # day of the week vs download
    day = app_data.groupby('day_of_week', as_index=False)['installs'].max().sort_values('installs', ascending=False)
    fig = plt.figure(figsize=(10, 5))
    plt.title('Installation trend during the week')
    viz = sns.barplot(data=day, x='installs', y='day_of_week')
    return fig

def yearly_download(app_data):     ##############################
    """This function is used to return the year with the most downloaded apps"""
    yearly_data = app_data.groupby('year')['installs'].agg('sum').reset_index(name='Total Installs')
    fig = plt.figure(figsize=(10, 6))
    plt.title('Most downloaded app by year')
    bar = sns.barplot(y=yearly_data['year'], x= yearly_data['Total Installs'])
    return fig

def appType_byScore(app_data):
    """This function returns a histogram that compares the scores(stars) given between paid and free apps"""
    app_data['app_type'] = ['free' if (x)==0 else 'paid' for x in app_data['price']]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    sns.histplot(
        data=app_data,
        x="starRating",
        hue="app_type",
        multiple="stack",
        ax=ax1
    )
    sns.kdeplot(
        data=app_data,
        x="starRating",
        hue="app_type",
        multiple="stack",
        ax=ax2
    )
    ax1.set_title("Histogram")
    ax2.set_title("")

    return fig

def monthly_download(app_data):       
    """This fucntion returns a line chart showing download trend by month as time move on"""
    monthly_data = app_data.groupby('month').mean()
    monthly_data.reset_index(inplace=True)
    fig = px.line(monthly_data, x='month', y='installs')
    fig.update_xaxes(nticks=15)
    return fig

def popularSize(app_data):
    """This function returns a bar chart that displays the top five most popular app size"""
    fig, ax = plt.subplots()
    sizez = app_data.groupby('size').size().reset_index(name='Frequency').nlargest(5, 'Frequency')
    ax = sns.barplot(y=sizez['size'], x=sizez['Frequency'], color='seagreen')

    return fig

def appSize_bar(app_data):
    """ This function returns a bar plot that displays the top ten most downloaded app size based on their sizes"""
    fig, ax = plt.subplots()
    App_size = app_data.groupby('size').installs.sum().sort_values(ascending=False).head(10)
    plt.title('Top 10 most downloaded app size')
    ax = sns.barplot(App_size.values, App_size.index, color='red')
    return fig

def appType_hist(app_data):
    """This function returns a histogram chart that compares all the reviews between free and paid apps"""

    free_apps = app_data[app_data['price']==0]
    paid_apps =  app_data[app_data['price'] != 0]

    fig, ax = plt.subplots()
    bins = [500, 1000, 1500, 2000, 2500, 3000, 5000, 6000, 8000, 10000]
    graph = sns.distplot(paid_apps['ratings'], norm_hist=True, color='#FF961F', label='Paid Apps',
                        bins=bins, kde=False, hist_kws={"histtype": "bar", "alpha": .7})
    graph = sns.distplot(free_apps['ratings'], norm_hist= True, color= '#219ebc', label='Free Apps', bins=bins, kde=False,
                        hist_kws={'histtype':'bar', 'alpha': .7})
   # graph = sns.distplot(app_data['ratings'], norm_hist=True, color = '#023047', label= 'All apps', bins=bins, kde=False,
     #                     hist_kws = {'histtype': 'step', 'alpha': 1, 'linewidth': 5})

    # show their mean review score
    graph.axvline(x=paid_apps['ratings'].mean(), color='#FF961F', linewidth=3, alpha=1)
    graph.axvline(x=free_apps['ratings'].mean(), color='#219ebc', linewidth=5, alpha=1)
   # graph.axvline(x=app_data['ratings'].mean(), color='#023047', linewidth=3, alpha=1)

    # graphics info
    graph.text(x=0.5, y=0.5, s='Naija App Store', fontsize=20, weight='bold', alpha=.75, transform=ax.transAxes)
    graph.text(x=0.5, y=0.45, s = 'app reviews by count based on the price', fontsize=16, alpha=.85, transform=ax.transAxes)
    graph.tick_params(axis='both', which ='major', labelsize=16)
    graph.axhline(y=0, color='black', linewidth=4, alpha=.7)
    #graph.set_xlim(left=1.9, right=5)
    graph.xaxis.label.set_visible(False)
    plt.legend(loc='center left', bbox_to_anchor=(0.02, 0.60))
    plt.xlabel('Reviews')
    return fig

def content_rate(app_data):      
    """This function checks for the correlation between content rating and installation in a tabular chart and then
    displays it on a bar chart"""

    # number of installations per content rating
    content_instal = app_data.groupby('contentRating')['installs'].agg('sum').reset_index(name='Number_Installations')
    # number of installation per app per content rating
    app_no = app_data.groupby('contentRating')['installs'].size().reset_index(name='Number of Apps')
    #write(content_instal)
    # write(app_no)
    fig = px.pie(content_instal, values='Number_Installations',
                names='contentRating',
                color_discrete_sequence=['red', 'goldenrod', 'cyan', 'green', 'blue','magenta'])
    return fig

def content_review(app_data):
    """This function displays on a chart which content rating attracted the most reviews"""
    content_review = app_data.groupby('contentRating')['reviews'].agg('sum').reset_index(name='Total Reviews')
    fig = px.pie(content_review, values='Total Reviews',
                     names='contentRating',
                     color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

def appName(app_data):
    """This function tries to compare the correlation between the length of an app name and the installation
    checks the total number of apps that belong to each len category with a comparism to their installation"""
    # Lets first of all create a new column for checking the appName length
    app_data['appName_len'] = ['>2 words' if len(x.split())>2 else '<=2words' for x in app_data['appName']]
    app_install = app_data.groupby('appName_len')['installs'].agg('sum').reset_index(name='Number_of_installation')
    data_apps = app_data.groupby('appName_len').size().reset_index(name='Number_of_Apps')
    #fig1 compares the total number of apps that belong to each appName_len category
    # and compares their installation
    fig1, axes = plt.subplots(figsize=(15,3), ncols=2, nrows=1)
    axes[0].set_title('Number of Installation', y= 1.1)
    axes[1].set_title('Number of Apps', y= 1.1)
    #viz1 = sns.barplot(x=app_install.appName_len, y= app_install.Number_of_installation, ax=axes[0])
    #viz2 = sns.barplot(data_apps.appName_len, y = data_apps.Number_of_Apps, ax=axes[1])
    #return fig1
    fig2, ax = plt.subplots()
    plt.title('Installation/Total Apps', y = 1.0)
    plt.tight_layout()
    ax = sns.barplot(data_apps.appName_len, y = app_install.Number_of_installation/data_apps.Number_of_Apps,
                    palette=sns.color_palette(palette='Set2', n_colors=2, desat=.8))
    return fig2

def Mostdownloaded_app(app_data):       
    """This function returns a bar chart with the most downloaded app"""
    # top ten most downloaded naija apps on playstore
    fig, ax = plt.subplots()
    app_data['appName_len'] = ['>2 words' if len(x.split())>2 else '<=2words' for x in app_data['appName']]
    App = app_data.groupby('appName').installs.sum().sort_values(ascending=False).head(10)
    plt.title('Top 10 most downloaded Naija apps')
    ax = sns.barplot(App.values, App.index)
    return fig

def MostReviewed_app(app_data):   
    """This function returns a bar chart displaying the app with the most review"""
    fig, ax =plt.subplots()
    appRating = app_data.groupby('appName').ratings.sum().sort_values(ascending=False).head(10)
    plt.title('Top 10 most reviwed Naija apps')
    ax = sns.barplot(appRating.values, appRating.index)
    return fig

def popularRelease_date(app_data):
    """This function returns a bar chart showing the top five most popular time to release app
    and the correlation between the time of release and installation in a tabular chart"""
   
    monthly_release = app_data.groupby('month').size().reset_index(name='Frequency').nlargest(5, 'Frequency')
    top_5 = monthly_release['month'].tolist()
    top_pop = app_data.groupby('month')['installs'].agg(sum).loc[top_5].reset_index(name='Total Installs')
    # altair plot
    fig = alt.Chart(top_pop).mark_bar(color='cyan', opacity=0.6).properties(width=500).encode(
    x = 'month',
    y = 'Total Installs'
    )
    return fig

def mdhist_content(app_data):
    """This function is used to preview the distribution of app content rating
    based on their star rating"""
    fig, (ax1, ax2) = plt.subplots(1, 2)
    sns.histplot(
        data=app_data,
        x="starRating",
        hue="contentRating",
        multiple="stack",
        ax=ax1
    )
    sns.kdeplot(
        data=app_data,
        x="starRating",
        hue="contentRating",
        multiple="stack",
        ax=ax2
    )
    ax1.set_title("Histogram")
    ax2.set_title("")

    return fig

def size_map(x):
    """function to create mapping for the top ten most downloaded app sizes to create a histogram
    chart to investigate how these various app sizes are rated by star from users based on their performance"""
    
    if x == '13M':
        return 'size_13MB'
    elif x == '10M':
        return 'size_10MB'
    elif x == '18M':
        return 'size_18MB'
    elif x == '17M':
        return 'size_17MB'
    elif x == '68M':
        return 'size_68MB' 

def appSizes_hist(app_data):
    """This function returns a histogram chart that compares the average star rating of the top five
    most downloaded app size """

    app_data['app_sizes'] = app_data['size'].apply(size_map)
    #map_size_df = app_data.groupby('app_sizes')['score'].agg('sum').reset_index(name='Star Rating')
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    sns.histplot(
        data=app_data,
        x="starRating",
        hue="app_sizes",
        multiple="stack",
        ax=ax1
    )
    sns.kdeplot(
        data=app_data,
        x="starRating",
        hue="app_sizes",
        multiple="stack",
        ax=ax2
    )
    ax1.set_title("Star Rating")
    ax2.set_title("")

    return fig

def get_app(app_id):
    """
    This function allow users to add their own product from playstore for comparison
    
    :Input: App ID
    
    :Output: Dataframe
    """
    result = app(
        app_id = app_id,
        lang = 'en',
        country = 'ng'
    )
    keys = ["title", "summary", "free", "genre", "installs", "ratings", "price", "size",
            "contentRating", "reviews", "released", "adSupported", "sale", "score", "similarApps", "version"]
    APP = []
    appDetails2 = {key: result[key] for key in keys}
    APP.append(appDetails2)
    data = pd.DataFrame(APP)
    return data


def convert_appSize(app_data):
    """
    This function copies the current dataframe to perform data processing on the game app size features, that
    that cleans and convert the app size feature into a float data type, and exracts all the different ranges of
    different app sizes which are saved as a new feature for auto generating star rating plot for the different 
    set size range. Only the sizes present within the dataframe feature will be returned and displayed on the plot, 
    otherwise nothing is returned for the sizes not present in the set range
    
    :Input: dataframe
    :Ouput: histogram plot 
    """
    # create a copy of dataframe to work with
    generic_data = app_data.copy()
    generic_data['size'] = generic_data['size'].apply(lambda x: str(x).replace('M', ' ') if 'M' in str(x) else x)
    generic_data['size'] = generic_data['size'].apply(lambda x: str(x).replace(',' , ' ') if ',' in str(x) else x)
    generic_data['size'] = generic_data['size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
    # convert to float and convert all values in kb to MB
    generic_data['size'] = generic_data['size'].apply(lambda x: str(x).replace('1 015', '1015'))
    generic_data['size'] = generic_data['size'].apply(lambda x: float(str(x).replace('k' , ' '))/1000 if 'k' in str(x) else x)
    generic_data['size'] = generic_data['size'].apply(lambda x: float(x))
    # create new dataframe with new generated input size values
    generic_data['size_bins_category'] = generic_data['size'].apply(categorize_size)

     # generate plot
    fig, (ax1, ax2) = plt.subplots(1, 2)
    sns.histplot(
        data=generic_data,
        x="starRating",
        hue="size_bins_category",
        multiple="stack",
        ax=ax1
    )
    sns.kdeplot(
        data=generic_data,
        x="starRating",
        hue="size_bins_category",
        multiple="stack",
        ax=ax2
    )
    ax1.set_title("Star Rating")
    ax2.set_title("")

    return fig

def categorize_size(x):
    """ This function is used to auto generate the range for the different app sizes"""
    if x <= 10.0:
        return '(1-10)MB'
    elif x > 10.0 and x <= 30.0:
        return '(11-30)MB'
    elif x > 30.0 and x <= 90.0:
        return '(31-90)MB'
    elif x > 90.0 and x <= 200.0:
        return '(91-200)MB'
    elif x > 200.0 and x <= 500.0:
        return '(201-500)MB'
    elif x > 500.0:
        return 'above 600MB'
