from enum import auto
from altair.vegalite.v4.schema.core import Orientation
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import plotly.express as px
import seaborn as sns
sns.set_style('whitegrid')
import streamlit as st



@st.cache(allow_output_mutation=True)
def load_data():
    """ function to clean the data and load into pandas dataframe """
    app_data = pd.read_csv('./data/ModifiedNaijaApps.csv')
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


def popular_category(app_data):
    """ This function creates visualization for the most popular category"""
    fig, ax = plt.subplots()
    #fig, ax = plt.subplots()
    ax = sns.countplot(app_data.category)
    plt.xticks(rotation=90)
    plt.title('Naija app most popular category')
    
    return fig
    
def top_cat(app_data):
    """ This function generates the top five most popular category and saves it to a list
    to generate plot to understand which of these category was downloaded the most
    """
    Top_5 = app_data.groupby('category').size().reset_index(name='Count').nlargest(5, 'Count')
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
    ax = sns.barplot(y=cat_data['category'], x= cat_data['Total Installs'])
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
    plt.title('Paid apps vs free apps with respect to installation')
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
    return fig

def appType_byScore(app_data):
    """This function returns a histogram that compares the scores(stars) given between paid and free apps"""
    app_data['app_type'] = ['free' if (x)==0 else 'paid' for x in app_data['price']]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    sns.histplot(
        data=app_data,
        x="score",
        hue="app_type",
        multiple="stack",
        ax=ax1
    )
    sns.kdeplot(
        data=app_data,
        x="score",
        hue="app_type",
        multiple="stack",
        ax=ax2
    )
    ax1.set_title("Histogram")
    ax2.set_title("Kernel density")

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
    sizez = app_data.groupby('size').size().reset_index(name='Count').nlargest(5, 'Count')
    ax = sns.barplot(y=sizez['size'], x=sizez['Count'], color='seagreen')

    return fig

def appSize_bar(app_data):
    """ This function returns a bar plot that displays the top ten most downloaded app size based on their sizes"""
    fig, ax = plt.subplots()
    App_size = app_data.groupby('size').installs.sum().sort_values(ascending=False).head(10)
    plt.title('Top 10 most downloaded app size')
    ax = sns.barplot(App_size.values, App_size.index, color='red')
    return fig

def appSize_hist(app_data):
    """This function returns a histogram chart that compares the average star rating of the top five
    most downloaded app size """
    
    # we select the top 5 app sizes for clear comparison
    df_38mb = app_data[app_data['size']=='38M']
    df_7mb = app_data[app_data['size']=='7.3M']
    df_13mb = app_data[app_data['size']=='13M']
    df_16mb = app_data[app_data['size']=='16M']
    device_df = app_data[app_data['size']=='Varies with device']
    
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots()
    bins = [1.9, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5]
    graph = sns.distplot(df_38mb['score'], norm_hist=True, color='red', label='38M',
                        bins=bins, kde=False, hist_kws={"histtype": "bar", "alpha": .7})
    graph = sns.distplot(df_7mb['score'], norm_hist= True, color= 'green', label='7.3M', bins=bins, kde=False,
                        hist_kws={"histtype": "bar", "alpha" : .7})
    graph = sns.distplot(df_13mb['score'], norm_hist= True, color= 'orange', label='13M', bins=bins, kde=False,
                        hist_kws={'histtype':'bar', 'alpha': .7})
    graph = sns.distplot(df_16mb['score'], norm_hist= True, color= 'blue', label='16M', bins=bins, kde=False,
                        hist_kws={'histtype':'bar', 'alpha': .7})
    graph = sns.distplot(device_df['score'], norm_hist= True, color= 'cyan', label='Varies with device', bins=bins, kde=False,
                        hist_kws={'histtype':'bar', 'alpha': .7})
    # graph = sns.distplot(all_data['score'], norm_hist=True, color = '#023047', label= 'All apps', bins=bins, kde=False,
    #                     hist_kws = {'histtype': 'step', 'alpha': 1, 'linewidth': 5})

    # show their mean star rating
    graph.axvline(x=df_38mb['score'].mean(), color='red', linewidth=3, alpha=.7)
    graph.axvline(x=df_7mb['score'].mean(), color='green', linewidth=5, alpha=.7)
    graph.axvline(x=df_13mb['score'].mean(), color='orange', linewidth=3, alpha=.7)
    graph.axvline(x=df_16mb['score'].mean(), color='blue', linewidth=3, alpha=.7)
    graph.axvline(x=device_df['score'].mean(), color='cyan', linewidth=3, alpha=.7)
    #graph.axvline(x=all_data['score'].mean(), color='#023047', linewidth=3, alpha=1)

    #  graphics info
    graph.text(x=0.5, y=0.5, s='Naija App Store', fontsize=20, weight='bold', alpha=.82, transform=ax.transAxes)
    graph.text(x=0.5, y=0.45, s = 'app rating depending on app sizes', fontsize=16, alpha=.85, transform=ax.transAxes)
    graph.tick_params(axis='both', which ='major', labelsize=16)
    graph.axhline(y=0, color='black', linewidth=4, alpha=.7)
    #graph.set_xlim(left=1.9, right=5)
    graph.xaxis.label.set_visible(False)
    plt.legend(loc='center left', bbox_to_anchor=(0.02, 0.60))
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



def content_score(app_data):
    """This function returns a histogram plot that displays the average star rating for all app content rating"""
    cat_12 = app_data[app_data['contentRating']=='Rated for 12+']
    cat_16 = app_data[app_data['contentRating']=='Rated for 16+']
    cat_18 = app_data[app_data['contentRating']=='Rated for 18+']
    cat_3 = app_data[app_data['contentRating']=='Rated for 3+']

    fig, ax = plt.subplots()
    bins = [1.9, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75, 5]
    graph = sns.distplot(cat_12['score'], norm_hist=True, color='red', label='12+',
                        bins=bins, kde=False, hist_kws={"histtype": "bar", "alpha": .7})
    graph = sns.distplot(cat_16['score'], norm_hist= True, color='green', label='16+', bins=bins, kde=False,
                        hist_kws={'histtype':'bar', 'alpha': .7})
    graph = sns.distplot(cat_18['score'], norm_hist=True, color = 'black', label= '18+', bins=bins, kde=False,
                        hist_kws = {'histtype': 'step', 'alpha': 1, 'linewidth': .7})

    graph = sns.distplot(cat_3['score'], norm_hist=True, color='blue', label= '3+', bins=bins, kde=False,
                        hist_kws = {'histtype': 'step', 'alpha': 1, 'linewidth': .7})
    #graph = sns.distplot(all_data['score'], norm_hist=True, label= 'All apps', bins=bins, kde=False,
    #                   hist_kws = {'histtype': 'step', 'alpha': 1, 'linewidth': 5})

    # Display their mean
    graph.axvline(x=cat_12['score'].mean(), color = 'red', linewidth=3, alpha=.7)
    graph.axvline(x=cat_16['score'].mean(),color = 'magenta',linewidth=5, alpha=.7)
    graph.axvline(x=cat_18['score'].mean(), color='black', linewidth=3, alpha=.7)
    graph.axvline(x=cat_3['score'].mean(), color='blue', linewidth=3, alpha=.7)
    #graph.axvline(x=all_data['score'].mean(), linewidth=3, alpha=.7)

    # graphics info
    graph.text(x=0.1, y=0.8, s='Naija App Store', fontsize=20, weight='bold', alpha=.85, transform=ax.transAxes)
    graph.text(x=0.1, y=0.75, s = 'app rating based on content rating', fontsize=16, alpha=.85, transform=ax.transAxes)
    graph.tick_params(axis='both', which ='major', labelsize=16)
    graph.axhline(y=0, color='black', linewidth=4, alpha=.7)
    #graph.set_xlim(left=1.9, right=5)
    graph.xaxis.label.set_visible(False)
    plt.legend(loc='center left', bbox_to_anchor=(0.02, 0.60))
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
   
    monthly_release = app_data.groupby('month').size().reset_index(name='Count').nlargest(5, 'Count')
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
        x="score",
        hue="contentRating",
        multiple="stack",
        ax=ax1
    )
    sns.kdeplot(
        data=app_data,
        x="score",
        hue="contentRating",
        multiple="stack",
        ax=ax2
    )
    ax1.set_title("Histogram")
    ax2.set_title("Kernel density")

    return fig


def get_category(app_data):
    """This function is to get each category by their"""
     
    Category = app_data.category.unique().tolist()
    return [name for name in Category if name != None] 


def size_map(x):
    """function to create mapping for the top ten most downloaded app sizes to create a histogram
    chart to investigate how these various app sizes are rated by star from users based on their performance"""
    
    if x == '38M':
        return 'size_38MB'
    elif x == '7.3M':
        return 'size_7.3MB'
    elif x == '13M':
        return 'size_13MB'
    elif x == '16M':
        return 'size_16MB'
    elif x == 'Varies with device':
        return 'device_size'

def appSizes_hist(app_data):
    """This function returns a histogram chart that compares the average star rating of the top five
    most downloaded app size """

    app_data['app_sizes'] = app_data['size'].apply(size_map)
    #map_size_df = app_data.groupby('app_sizes')['score'].agg('sum').reset_index(name='Star Rating')
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    sns.histplot(
        data=app_data,
        x="score",
        hue="app_sizes",
        multiple="stack",
        ax=ax1
    )
    sns.kdeplot(
        data=app_data,
        x="score",
        hue="app_sizes",
        multiple="stack",
        ax=ax2
    )
    ax1.set_title("Star Rating")
    ax2.set_title("Kernel density")

    return fig
