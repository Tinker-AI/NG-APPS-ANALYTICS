import streamlit as st
from utility import *
from sentimentt import * 
from game_utils import *
from PIL import Image

import warnings
warnings.filterwarnings('ignore')

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

st.sidebar.markdown("""<style>body {background-color: #2C3454;white;}</style><body></body>""", unsafe_allow_html=True)
st.markdown("""<h1 style='text-align: center; white;font-size:60px;margin-top:-50x;'>APP ANALYTICS</h1><h1 style='text-align: center; color: black;font-size:30px;margin-top:-30px;'>Research Project on Nigerian Products<br></h1>""", unsafe_allow_html=True)

def home_page():
    st.markdown("""<h2 style='text-align: left; color: white;'>Problem Statement</h2><p style='color: white;'>""")
    

st.sidebar.title('Menu')
Options = st.sidebar.selectbox(
    '', ['Home', 'App Analytics', 'Game Analytics', 'Sentiment Analytics'], index=0
)

if Options == "App Analytics":
    
    # load csv app data  
    df = load_data()
    if st.sidebar.checkbox('view dataframe', False):
        st.write(df)

    names = get_category(df)
    names.append('Analyze All Category')
    category_name = st.sidebar.selectbox("Category Name", names, key='1')

    # create plot for all categories combined 
    if category_name == 'Analyze All Category':
        st.markdown("###### View the most popular category on Playstore")
        st.pyplot(popular_category(df))
        st.write('')

        st.markdown("###### Shows which of the top 5 most popular category was downloaded the most")
        st.altair_chart(top_cat(df))
        Top_5 = df.groupby('category').size().reset_index(name='Count').nlargest(5, 'Count')
        top_5 = Top_5['category'].tolist()
        top_pop = df.groupby('category')['installs'].agg(sum).loc[top_5].reset_index(name='Total Installs')
        st.write(top_pop)
        st.write('')

        st.markdown("###### Plot that shows the overall most installed category")
        st.pyplot(mostInstalledCat(df))
        st.write('')

        st.write("###### The plot to show the category that had the most review")
        st.pyplot(mostReviewedCat(df))
        st.write('')

        st.write("###### This plot shows the most rated category")
        st.pyplot(mostRatedCat(df))
        st.write('')
        st.write('')

        st.write("###### This plot shows what apps are downloaded mostly across all category between free and paid apps")
        st.pyplot(appType(df))
        st.write('')

        st.write("###### This plot shows weekly trend for the most download across all category")
        st.pyplot(wkly_download(df))
        st.write('')

        st.write("###### This plot compares all the reviews given between paid and free apps across all category")
        st.pyplot(appType_hist(df))
        st.write('')

        st.write("###### This plot shows the average star rating between paid and free apps across all category")
        st.pyplot(appType_byScore(df))
        st.write('')

        st.write("###### This plot shows monthly download trend across all category")
        st.plotly_chart(monthly_download(df))
        st.write('')

        st.write("###### This shows most popular app sizes across all Category")
        st.pyplot(popularSize(df))
        st.write('')

        st.write('###### Top ten most popular app size across all Category')
        st.pyplot(appSize_bar(df))
        st.write('')

        st.write('###### This plot compares the average star rating for the top 5 most downloaded app Size across all category')
        st.pyplot(appSizes_hist(df))
        st.write('')

        st.markdown('###### This plot displays the variation between content rating and installation across all category')
        st.plotly_chart(content_rate(df))
        # number of installations per content rating
        content_instal = df.groupby('contentRating')['installs'].agg('sum').reset_index(name='Number_Installations')
        # number of installation per app per content rating
        app_no = df.groupby('contentRating')['installs'].size().reset_index(name='Number of Apps')
        st.write(content_instal)
        st.write('')
        st.write('')
        st.write(app_no)

        st.markdown('###### This plot shows the content rating that attracted the most review across all category')
        st.plotly_chart(content_review(df))
        st.write('')

        st.markdown("###### This plot shows the effect of app name length on installation across all category")
        st.pyplot(appName(df))
        st.write('')

        st.markdown('###### content rating distribution based on their star rating across all category')
        st.pyplot(mdhist_content(df))
        st.write('')

        st.markdown("###### This plot shows the most downloaded app across all the category")
        st.pyplot(Mostdownloaded_app(df))
        st.write('')

        st.markdown('###### This plot shows the most reviewed app across all the category')
        st.pyplot(MostReviewed_app(df))
        st.write('')

        st.markdown('###### This plot shows the top 5 most popular release date across all the category')
        st.altair_chart(popularRelease_date(df))
        # Table representation
        monthly_release = df.groupby('month').size().reset_index(name='Count').nlargest(5, 'Count')
        top_5 = monthly_release['month'].tolist()
        top_pop = df.groupby('month')['installs'].agg(sum).loc[top_5].reset_index(name='Total Installs')
        st.write(top_pop)

    else:
        category_data = df[df['category']==category_name]
        #st.write(category_data)
        st.write('')   # create white spaces
        st.markdown('## Analyze {} Apps'.format(category_name))
        st.write('')
        st.pyplot(appSize_bar(category_data))
        st.write('')

        st.markdown('###### This plot shows the common app sizes in {}'.format(category_name))
        st.pyplot(popularSize(category_data))
        st.write('')

        st.markdown("###### Most downloaded apps in {}".format(category_name))
        top_pop = category_data.groupby('appName')['installs'].agg(sum).head(10).reset_index(name='Total Installs')
        fig = alt.Chart(top_pop).mark_bar(color='magenta').properties(width=500, height=500).encode(
        x = 'appName',
        y = 'Total Installs'
        )
        st.altair_chart(fig)
        st.write('')

        st.markdown("###### Top ten Apps with the most review in {} category".format(category_name))
        cat_review = category_data.groupby('appName', as_index=False)['reviews'].max().sort_values('reviews', ascending=False).head(10)
        fig = px.bar(cat_review, y='reviews', x='appName', color_discrete_sequence=['green']
        )
        st.plotly_chart(fig)
        st.write('')

        st.write("###### Top ten most rated Apps in {} category".format(category_name))
        cat_rating = category_data.groupby('appName', as_index=False)['ratings'].max().sort_values('ratings', ascending=False).head(10)
        fig = alt.Chart(cat_rating).mark_bar(color='orange').properties(width=500, height=500).encode(
            x = 'appName',
            y = 'ratings'
        )
        st.altair_chart(fig)

        st.write("###### Day of the week that have the most download for {}".format(category_name))
        st.pyplot(wkly_download(category_data))
        st.write('')

        st.markdown("###### Star rating distribution of content rating for {}".format(category_name))
        st.pyplot(mdhist_content(category_data)) 
        st.write('') 

        st.markdown("###### Star ratings of top ten different app sizes in {} category".format(category_name))
        size_var = category_data.groupby('size', as_index=False)['score'].max().sort_values('score', ascending=True).head(10)
        fig = px.histogram(size_var, x='score', nbins=10, color='size')
        st.plotly_chart(fig)
        st.write('')

        st.markdown("###### Star ratings of the least ten different app sizes in {} category".format(category_name))
        size_var = category_data.groupby('size', as_index=False)['score'].max().sort_values('score', ascending=False).head(10)
        fig = px.histogram(size_var, x='score', nbins=10, color='size')
        st.plotly_chart(fig)
        st.write('')

        st.markdown("###### Monthly download trend for {} apps".format(category_name))
        st.plotly_chart(monthly_download(category_data))
        st.write('')

        st.markdown("###### Content Rating type with the most review for {} apps".format(category_name))
        content_review = category_data.groupby('contentRating')['reviews'].agg('sum').reset_index(name='Total Reviews')
        fig = px.pie(content_review, values='Total Reviews',
                     names='contentRating',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)
        st.write('')

        st.markdown("###### Popular release date for {} apps".format(category_name))
        st.altair_chart(popularRelease_date(category_data))
        st.write('')

        st.write("###### Effect of appName length on average installation for {} apps".format(category_name))
        st.pyplot(appName(category_data))
        st.write('')

        st.markdown("###### Content Rating type with the highest installation for {} apps".format(category_name))
        st.plotly_chart(content_rate(category_data))
        st.write('')

        st.markdown('###### This plot shows the statistics distribution between paid and free {} apps based on their star rating'.format(category_name))
        st.pyplot(appType_byScore(category_data))
        st.write('')

        
if Options == "Game Analytics":
    # load game data
    games_df = load_games()
    
    # preview game_csv data through the frontend
    if st.sidebar.checkbox('View Game Data', False):
        st.write(games_df)

    names = get_category(games_df)
    names.append('Analyze All Games')
    category_name = st.sidebar.selectbox("Category Name", names, key='1')
  
    if category_name == "Analyze All Games":
        st.markdown('###### This plot shows the statistics cost of games between paid and free games across all category')
        st.pyplot(game_cost(games_df))
        st.write('')

        st.markdown('###### This plot shows the most popular game category')
        st.pyplot(genre(games_df))

        st.markdown('###### This plot shows the total installation count across all category')
        st.pyplot(count_installs(games_df))
        st.write('')

        st.markdown("###### Shows which of the top 5 most popular game category was downloaded the most")
        st.altair_chart(top_cat(games_df))
        st.write('')

        st.markdown("###### Plot that shows the overall most installed game category")
        st.pyplot(mostInstalledCat(games_df))
        st.write('')

        st.write("###### The plot to show the category that had the most review")
        st.pyplot(mostReviewedCat(games_df))
        st.write('')

        st.write("###### This plot shows the most rated category")
        st.pyplot(mostRatedCat(games_df))
        st.write('')
        st.write('')

        st.write("###### This plot shows what apps are downloaded mostly across all category between free and paid apps")
        st.pyplot(appType(games_df))
        st.write('')

        st.write("###### This plot shows weekly trend for the most download across all category")
        st.pyplot(wkly_download(games_df))
        st.write('')

        st.write("###### This plot compares all the reviews given between paid and free apps across all category")
        st.pyplot(appType_hist(games_df))
        st.write('')

        st.write("###### This plot shows the average star rating between paid and free apps across all category")
        st.pyplot(appType_byScore(games_df))
        st.write('')

        st.write("###### This plot shows monthly download trend across all category")
        st.plotly_chart(monthly_download(games_df))
        st.write('')

        st.write("###### This shows most popular app sizes across all game category")
        st.pyplot(popularSize(games_df))
        st.write('')

        st.write('###### Top ten most popular app size across all Category')
        st.pyplot(appSize_bar(games_df))
        st.write('')

        st.write('###### This plot compares the average star rating for the top 5 most downloaded app size across all category')
        st.pyplot(appSizes_hist(games_df))
        st.write('')

        st.markdown('###### This plot displays the variation between content rating and installation across all category')
        st.plotly_chart(content_rate(games_df))
        st.write('')
    
        st.markdown('###### This plot shows the content rating that attracted the most review across all category')
        st.plotly_chart(content_review(games_df))
        st.write('')

        st.markdown("###### This plot shows the effect of game name length on installation across all category")
        st.pyplot(appName(games_df))
        st.write('')

        st.markdown('###### content rating distribution based on their star rating across all category')
        st.pyplot(mdhist_content(games_df))
        st.write('')

        st.markdown("###### This plot shows the most downloaded game across all the category")
        st.pyplot(Mostdownloaded_app(games_df))
        st.write('')

        st.markdown('###### This plot shows the most reviewed game across all the category')
        st.pyplot(MostReviewed_app(games_df))
        st.write('')

        st.markdown('###### This plot shows the top 5 most popular release date across all the category')
        st.altair_chart(popularRelease_date(games_df))
        # Table representation
        monthly_release = games_df.groupby('month').size().reset_index(name='Count').nlargest(5, 'Count')
        top_5 = monthly_release['month'].tolist()
        top_pop = games_df.groupby('month')['installs'].agg(sum).loc[top_5].reset_index(name='Total Installs')
        st.write(top_pop)

    else:
        try:
            game_data = games_df[games_df['category']== category_name]
            st.write('')   # create white spaces
            st.markdown('## Analyze {} Apps'.format(category_name))
            st.write('')
            st.pyplot(appSize_bar(game_data))
            st.write('')

            st.markdown('###### This plot shows the common game sizes in {}'.format(category_name))
            st.pyplot(popularSize(game_data))
            st.write('')

            st.markdown("###### Most downloaded game apps in {}".format(category_name))
            top_pop = game_data.groupby('appName')['installs'].agg(sum).head(10).reset_index(name='Total Installs')
            fig = alt.Chart(top_pop).mark_bar(color='magenta').properties(width=500, height=500).encode(
            x = 'appName',
            y = 'Total Installs'
            )
            st.altair_chart(fig)
            st.write('')

            st.markdown("###### Top ten game apps with the most review in {} category".format(category_name))
            cat_review = game_data.groupby('appName', as_index=False)['reviews'].max().sort_values('reviews', ascending=False).head(10)
            fig = px.bar(cat_review, y='reviews', x='appName', color_discrete_sequence=['green']
            )
            st.plotly_chart(fig)
            st.write('')

            st.write("###### Top ten most rated game Apps in {} category".format(category_name))
            cat_rating = game_data.groupby('appName', as_index=False)['ratings'].max().sort_values('ratings', ascending=False).head(10)
            fig = alt.Chart(cat_rating).mark_bar(color='orange').properties(width=500, height=500).encode(
                x = 'appName',
                y = 'ratings'
            )
            st.altair_chart(fig)

            st.write("###### Day of the week that most games were downloaded from {}".format(category_name))
            st.pyplot(wkly_download(game_data))
            st.write('')

            st.markdown("###### Star rating distribution of game content rating for {}".format(category_name))
            st.pyplot(mdhist_content(game_data)) 
            st.write('') 

            st.markdown("###### Star ratings of top ten different game app sizes in {} category".format(category_name))
            size_var = game_data.groupby('size', as_index=False)['score'].max().sort_values('score', ascending=True).head(10)
            fig = px.histogram(size_var, x='score', nbins=10, color='size')
            st.plotly_chart(fig)
            st.write('')

            st.markdown("###### Star ratings of the least ten different game app sizes in {} category".format(category_name))
            size_var = game_data.groupby('size', as_index=False)['score'].max().sort_values('score', ascending=False).head(10)
            fig = px.histogram(size_var, x='score', nbins=10, color='size')
            st.plotly_chart(fig)
            st.write('')

            st.markdown("###### Monthly download trend for {} game apps".format(category_name))
            st.plotly_chart(monthly_download(game_data))
            st.write('')

            st.markdown("###### Content Rating type with the most review for {} game apps".format(category_name))
            content_review = game_data.groupby('contentRating')['reviews'].agg('sum').reset_index(name='Total Reviews')
            fig = px.pie(content_review, values='Total Reviews',
                            names='contentRating',
                            color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig)
            st.write('')

            st.markdown("###### Popular release date for {} game apps".format(category_name))
            st.altair_chart(popularRelease_date(game_data))
            st.write('')

            st.write("###### Effect of game name length on average installation for {} game apps".format(category_name))
            st.pyplot(appName(game_data))
            st.write('')

            st.markdown("###### Content Rating type with the highest installation for {} game apps".format(category_name))
            st.plotly_chart(content_rate(game_data))
            st.write('')

            st.markdown('###### Statistics distribution between paid and free {} game apps based on their star rating'.format(category_name))
            st.pyplot(appType_byScore(game_data))
            st.write('')
        except ValueError:
            st.write("### ... Sorry this feature does not have enough data to display this chart")


elif Options == "Sentiment Analytics":
    img = Image.open("./asset/sentiment.jpg")
    st.image(img)
    st.markdown('### Want to analyze users feedback in realtime? Select your choice')
    se = st.sidebar.radio(label="Sentiment Analysis", options=(' ','GooglePlay Apps (Android)', 'AppStore Apps (iOS)'))
    

    if se =="GooglePlay Apps (Android)":
        id = st.text_input("What's the Nigerian App's ID on Playstore? e.g com.invest.bamboo")
        st.write("Fetching all reviews from Playstore may take a little while...")
        
        df = fetchPlaystorereviews(id)
        st.write(df)
        df["cleanReview"] = [preprocessReview(review) for review in df["review"]]
        df["Sentiment"] = df["cleanReview"].apply(sentiment_scores)
        st.pyplot(sentiment_chart(df))
        st.write(sentiments_and_word_cloud(df))

            
      

    elif se =="AppStore Apps (iOS)":
        try:
            app_name = st.text_input("What's the Nigerian App's Name on Appstore?")
            st.write("Fetching all reviews from Appstore may take a while...")
            df = fetchAppstorereviews(app_name)
            st.write(df)
            df["cleanReview"] = [preprocessReview(review) for review in df["review"]]
            df["Sentiment"] = df["cleanReview"].apply(sentiment_scores)
            st.pyplot(sentiment_chart(df))
            st.pyplot(sentiments_and_word_cloud(df))

        except:
            pass
    






    
    













        
        


        




    





