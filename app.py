import streamlit as st
from utility import *
from sentiment import * 
from game_utils import *
import warnings
warnings.filterwarnings('ignore')


df = load_data()

#  ---- data preprocessing---------------------------#


if st.sidebar.checkbox('view dataframe', False):
    st.write(df)

# st.pyplot(popular_category(df))
# Top_5 = df.groupby('category').size().reset_index(name='Count').nlargest(5, 'Count')
# st.write(Top_5)
# st.write('')
# st.write('')
st.altair_chart(top_cat(df))

st.altair_chart(popularRelease_date(df))
monthly_release = df.groupby('month').size().reset_index(name='Count').nlargest(5, 'Count')
st.write(monthly_release)
# st.plotly_chart(mostInstalledCat(df))
st.pyplot(appSize_hist(df))
id = 'com.axamansard.app'
data = fetch_review(id)
st.write(data)

st.pyplot(mostRatedCat(df))