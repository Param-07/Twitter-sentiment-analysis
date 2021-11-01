#!/usr/bin/env python
# coding: utf-8

# ### SENTIMENT ANALYSIS PROJECT 

# In[25]:


from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd  
import numpy as np
import re
import matplotlib.pyplot as plt
from textblob import TextBlob

############# ACCESS TOKENS FOR TWITTER APP#####################
ACCESS_TOKEN="1054428442177892352-rm4ghT9gnvVtxymuolL6bSLUaTheMV"
ACCESS_TOKEN_SECRET="SsXhcvWcdIv4gMkhTl0f45ZmDtqoCDsF2Epf22mW1PDPc"
CONSUMER_KEY="nixoGUlIAhG5D0QA7F04pY7vA"
CONSUMER_SECRET="SFTfUZTCdWoBEGejSSLAZYpGBSZAfpiDWrHt4MwKJRReBaJbCT"


####################TWITTER CLIENT###############################
class TwitterClient():
    def __init__(self, twitter_user = None):
        self.auth=TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        
        self.twitter_user=twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_user_timeline_tweets(self,num_tweets):
        tweets= []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    
    def get_friend_list(self, num_friends):
            frined_list=[]
            for friend in Cursor(self.twitter_client.frineds, id = self.twitter_user).items(num_friends):
                friend_list.append(friend)
            return friend_list
        
           
    def get_home_timelinie_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timelinie, id = self.twitter_user).item(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


######################## TWITTER AUTHENTICATOR###########################
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        return auth


########################## TWITTER STREAMER ##########################
class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    """
    CLASS FOR STREAMING AND PROCESSING LIVE TWEETS. 
    """
    def stream_tweets(self, fetched_tweeets_file_name, hash_tag_list):
# This handles twitter authentication and teh connection to the twitter streaming API.
        listener = TwitterListener(fetched_tweets_filenme)
        auth= self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
#This line filter Twitter streams to capture data by keywords:
        stream.filter(track=hash_tag_list)  
        
#######################TWITTER STREAM LISTENER########################                        
class TwitterListener(StreamListener):
    """
    THIS IS A LISTENER CLASS TAHT JUST PRINTS RECEIVED TWEETS TO STDOUT.
    """
    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        
    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,"a") as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True 
    
    def on_error(self,status):
        if status == 420:
            return False
        print(status)
########################## TWEET ANALYSER #############################################
class TweetAnalyzer():
    """
    Functionality for analysing and categorising content from tweets.
    """
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis= TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return "POSITIVE"
        elif analysis.sentiment.polarity == 0:
            return "NEUTRAL" 
        else:
            return "NEGATIVE"
    
 
    def tweets_to_data_frame(self, tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets],columns=["Tweets"])
        df["Id"] = np.array([tweet.id for tweet in tweets])
        df["Length"] = np.array([len(tweet.text) for tweet in tweets])
        df["Date"] = np.array([tweet.created_at for tweet in tweets])
        df["Source"] = np.array([tweet.source for tweet in tweets])
        df["Likes"] = np.array([tweet.favorite_count for tweet in tweets])
        df["Retweets"] = np.array([tweet.retweet_count for tweet in tweets])
        
        return df
        
if __name__=="__main__":
    twitter_client =  TwitterClient()
    tweet_analyzer= TweetAnalyzer()
    api= twitter_client.get_twitter_client_api()
    
    tweets = api.user_timeline(screen_name="pycon",count= 10)
    
    df= tweet_analyzer.tweets_to_data_frame(tweets)
    df["Sentiment"] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df["Tweets"]])
    
    print(df.head(10))
    
######################PERCENTAGE OF POSITIVE NEGATIVE NEUTRAL TWEETS#################    
    ptweet=df[df["Sentiment"] == "POSITIVE"]
    ntweet=df[df["Sentiment"] == "NEGATIVE"]
    Otweet=df[df["Sentiment"] == "NEUTRAL"]
    print("\n\nPERCENTAGE OF POISITVE TWEET IS {}".format(100*len(ptweet)/len(tweets)))
    print("\nPERCENTAGE OF NEGATIVE TWEET IS {}".format(100*len(ntweet)/len(tweets)))
    print("\nPERCENTAGE OF NEUTRAL TWEET IS {}".format(100*len(Otweet)/len(tweets)))



    

            


# In[ ]:




