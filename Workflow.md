**Scrape Tweets Using snscrape:**

Released on July 8, 2020, snscrape is a scraping tool for social networking services (SNS).\
It scrapes things like users, user profiles, hashtags, searches, threads, list posts and returns the discovered items without using Twitter’s API.

**Getting Started with snscrape:**\
**Requirements:**\
MongoDB\
Python 3.8 or higher\
pandas\
Streamlit


**Installing snscrape:**\
pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git/
Note: To run git cli commands, you have to have git installed before running your pip command.

**Creating a GUI using streamlit:**\
Streamlit lets you turn data scripts into shareable web apps in minutes, not weeks. It’s all Python, open-source, and free!\
**Installation**\
Open a terminal and run:\
$ pip install streamlit

**For storing (Mongodb):**\
Store each collection of data into a document into Mongodb.\
 -installs MongoDB 6.0 Community Edition(MongoDBCompass)

**Create a python code :**\
importing all the necessary modules

**Modules Required:**
1) streamlit
2) snscrape.modules.twitter
3) pandas
4) datetime from date
5) MongoClient from pymongo


**For Scrapping Tweets :**\
Use snscrape.modules.twitter.TwitterSearchScraper(query1) function to scrape the tweet and store it in a list.

**Upload To Database:**\
 Using  client = MongoClient('mongodb://localhost:27017'):\
Store each collection of scraped tweet data into a document into Mongodb along with the hashtag or keyword we used to Scrape from twitter.

**To Download the file in JSON Format:**\
df.to_json().encode('utf-8')\
df has the whole scrapped data which was stored in the list.

**To Download the file in CSV format:**\
df.to_csv().encode('utf-8')\
df has the whole scrapped data which was stored in the list.


