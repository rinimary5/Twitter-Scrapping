import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date
from pymongo import MongoClient
#css to allign columns
st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            border:1px;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            border:1px;
            text-align: end;
        } 
        div[data-testid="column"]:nth-of-type(3)
        {
            border:1px;
            text-align: end;
        } 
        div[data-testid="column"]:nth-of-type(4)
        {
            border:1px;
            text-align: end;
        } 
        div[data-testid="column"]:nth-of-type(5)
        {
            border:1px;
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
)
header=st.container()
model_training=st.container()


with header:
    st.title("Welcome to Twitter-Scraper")
with model_training:
    hash_col,fromdate_col,tilldate_col,tweetlimit_col,search_col=st.columns(5)
    hashtag=hash_col.text_input("Enter Keyword ",'')
    since=fromdate_col.date_input("Select your from date",value=date(2023,3,4),min_value=date(2006,1,12),
                                  max_value=date(2023,3,8))
    until = tilldate_col.date_input("Select your till date", value=date(2023, 12, 4),
                                    min_value=date(2006, 1, 12),
                                    max_value=date(2024, 3, 8))
    count=tweetlimit_col.number_input("Tweet Limit",min_value=100,max_value=10000,value=500,step=100)
    #Session States for nested buttons
    if "button1" not in st.session_state:
        st.session_state["button1"] = False
    if "button2" not in st.session_state:
        st.session_state["button2"] = False
    if "button3" not in st.session_state:
        st.session_state["button3"] = False
    if "button4" not in st.session_state:
        st.session_state["button4"] = False

#Function to create the query
    def search(hashtag, since, until, count):
            q = hashtag
            q = q + f" since:{since}"
            q = q + f" until:{until}"
            return q
    query1 = search(hashtag, since, until, count)
#Function to Scrape data
    def datascrape(query1):
        tweets_list1 = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query1).get_items()):
            if i > count:
                break
            tweets_list1.append(
                [tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount,
                 tweet.retweetCount,
                 tweet.lang, tweet.source, tweet.likeCount])
            tweets_df1 = pd.DataFrame(tweets_list1,
                                      columns=['Datetime', 'Tweet Id', 'URL', 'Text', 'Username', 'Reply Count',
                                               'Retweet Count', 'Language', 'Source', 'Like Count'])
        return tweets_df1
    dfn1=datascrape(query1)
    dfn2=dfn1
#Print the scraped data when clicked on search button
    if search_col.button("Search"):
        st.session_state["button1"] = not st.session_state["button1"]

        dfn = datascrape(query1)
        st.write(dfn)

#Uploading the data into database
    if st.session_state["button1"]:
        if st.button("Upload To Database"):
            st.session_state["button2"] = not st.session_state["button2"]

            client = MongoClient('mongodb://localhost:27017')
            mydb = client.db4
            mycol = mydb.mycollection
            dfn1.reset_index(inplace=True)
            tweetsdf1_dict = dfn1.to_dict('records')
            re=mycol.insert_one({'Scraped_Word': hashtag, 'Scraped_Date':str(date.today()), 'Scraped_Data': [tweetsdf1_dict]})
            st.write(re)
            st.write("Data Uploaded to the Database")


#Download the data in CSV format
    if st.session_state["button1"]:
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        #dfn2=datascrape(query1)
        csv = convert_df(dfn2)

        st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='large_df.csv',
                mime='text/csv',
                )
        st.session_state["button3"] = not st.session_state["button3"]

#Download the data in json format

    if st.session_state["button1"]:
        @st.cache_data
        def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_json().encode('utf-8')


        json = convert_df(dfn2)

        st.download_button(
                label="Download data as json",
                data=csv,
                file_name='large_df.json',
                mime='text/json',
                )

        st.session_state["button4"] = not st.session_state["button4"]
