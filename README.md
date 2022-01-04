# Nigerian App Analytics


## Project Description
Nigerian App Analytics is a research project on the Nigerian app market.
We looked answer questions like:
- What are the qualities of a good and successful Nigerian app ?
- How is a particular Nigerian app performing ?
- What are the available Nigerian apps in a particular app category ?
- What categories are doing well the most in the Nigerian app market ?

The project was designed with the intention of not only assisting Product Owners and Developers but the app users too.
NG App Analytics has made it very easy for Product Owners or Developers to quickly check how  thier app is performing, 
we also made it easy for developers to easily analyse the Nigerian app market so as to stategically choose a good project to embark on.
Developers can also analyse the reviews of their apps given by their customers on apple store and play store.
The data used for this research project was scrapped from playstore with the guardian of a Nigerian app, containing a comprehensive list of Nigerian apps and games of all categories, the app goes by the name [Nigerian apps and games](https://play.google.com/store/apps/details?id=com.vs.appmarket.nigeria&hl=en_US&gl=US).


The project has four section namely :
- App Analytics:
This section is designed to analyse Nigerian apps of all available categories on Google playstore
- Game Analytics:
This section is designed to analyse Nigerian game apps of all available categories on Google playstore
- App Comparison:
This section is designed to give users the opportunity analyse a Nigerian app we don't have on our database
- Sentiment Analytics:
This section is designed to analyse customer reviews of Nigerian apps on both play store and apple store


## How to Install and Run the Project
Steps to install this project include :
- Clone the github repository by running
 
`git clone https://github.com/NG-APP-ANALYTICS/Playstore-apps.git`
- Create and activate a virtual environment on your local machine
- Using your terminal and in your virtual environment, install all the dependencies in the requirement.txt file by running

`pip install -r requirements.txt`
- After installing all requirements, you should be able to run streamlit run app.py, successfully.
- This should automatically redirect you to your default browser. If it doesn't, simply copy and open the Local URL on your terminal to your browser.

## How to Use the Project
There are certain things to be kept in mind when using this project:
- We had major constraint with data because there was little available Nigerian apps on some categories
- When using any feature that involves using app id or app name. App must be explicitly Nigerian
- When using app id , the app id needs to be without extra characters like so  _com.jumia.android_, the app id for [JUMIA](https://play.google.com/store/apps/details?id=com.jumia.android&hl=en&gl=US)


## Built With
- [Python](https://www.python.org/)
- [altair](https://altair-viz.github.io/)
- [app-store-scraper](https://pypi.org/project/app-store-scraper/)
- [google-play-scraper](https://pypi.org/project/google-play-scraper/)
- [Matplotlib](https://matplotlib.org/)
- [nltk](https://www.nltk.org/)
- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Seaborn](https://seaborn.pydata.org/)
- [Streamlit](https://streamlit.io/)
- [Wordcloud](https://pypi.org/project/wordcloud/)

## Contributors
Contributor on this project include:

- [Jude Leonard](https://github.com/judeleonard)
- [Aisha Mohammed](https://github.com/aisha-rm)
- [Sharon Ibejih](https://github.com/sharonibejih)
- [Azeez Razaq](https://github.com/Gbolahan-Aziz)
