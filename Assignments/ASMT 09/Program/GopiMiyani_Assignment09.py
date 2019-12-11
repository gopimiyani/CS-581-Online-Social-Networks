#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:36:34 2019

@AUTHOR: Gopi Miyani    10437266

PURPOSE OF PROGRAM: To retrieve some data from the Twitter API, and do some processing of your design on that data.

PROGRAM SPECIFICATIONS:
    Accept twos earch terms and a maximum number of results from the user.  
    This can be done either by use of an argument list or by prompting the user for the information.  
    eg: python3   youtube_data.py   --search_term1 mysearch1 --search_term2 mysearch2 --search_max   mymaxresults
    or:*** Enter your first search term:  (user input)
    *** Enter your second search term:  (user input)
    *** Enter maximum results:  (user input)

Use the search terms to do twitter searches.  
Write the results to .csv files that will remain in existence when the program is completed.
Perform some type of analysis on the results of your searches.

RUN INSTRUCTIONS:
# to run from terminal window:  
       python3   GopiMiyani_Assignment09.py   --search_term1 mysearch1 --search_term2 mysearch2 --search_max   mymaxresults

"""

from textblob import TextBlob	# needed to analyze text for sentiment
import argparse    				# for parsing the arguments in the command line
import csv						# for creating output .csv file
import tweepy					# Python twitter API package
import unidecode				    # for processing text fields in the search results
import pandas as pd             # for csv file processing
import matplotlib.pyplot as plt # need fo plotting graphs


### PUT AUTHENTICATOIN KEYS HERE ###
CONSUMER_KEY = "zefNriHX0nyOdkX4VVzJD6Erd"
CONSUMER_KEY_SECRET = "id4VkvYlkadoAsmLlFhI08EGqW48TUkbkbMg6aDAnxmjoyAKvG"
ACCESS_TOKEN = "1153121156360298496-utRTm2eCI25wHjlxYPGNyVeN5dtEAE"
ACCESS_TOKEN_SECRET = "I5ZHFa6up6K5qvFZraX5XkUy28XkVXco0fjGT4VhAaZAp"


def twitter_search(search_terms,search_max):
    
    # do the twitter search
    for search_term in search_terms:
        # create a .csv file to hold the results, and write the header line
        csvFile = open('twitter_results_' + search_term + '.csv','w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["username","userid","location","created", "tweet", "retweets", "favourite_count","followers",
        "friends","polarity","subjectivity"])
        
        for tweet in tweepy.Cursor(api.search, q = search_term, lang = "en", 
            		result_type = "popular").items(search_max):
            		
                created = tweet.created_at				# date created
                text = tweet.text						# text of the tweet
                text = unidecode.unidecode(text) 
                retweets = tweet.retweet_count			# number of retweets
                favourite_count=tweet.favorite_count    # number of favourites
                username  = tweet.user.name            	# user name
                userid  = tweet.user.id              	# userid
                location = tweet.user.location          # user location
                followers = tweet.user.followers_count 	# number of user followers
                friends = tweet.user.friends_count      # number of user friends
                
                	# use TextBlob to determine polarity and subjectivity of tweet
                text_blob = TextBlob(text)
                polarity = text_blob.polarity
                subjectivity = text_blob.subjectivity
                    
                	# write tweet info to .csv tile
                csvWriter.writerow([username, userid, location, created, text, retweets, favourite_count, followers, 
                	friends, polarity, subjectivity])
        csvFile.close()
        

def twitter_data_analysis(search_terms):
    
    # read both csv file using pandas library
    twitter_data1=pd.read_csv("twitter_results_"+search_terms[0]+".csv")
    twitter_data2=pd.read_csv("twitter_results_"+search_terms[1]+".csv")
    
    print('\n*************   Data Analysis on Searched Twitter Data   *************\n\n')
    
    
    ## Determine overall sentiment (i.e. more positivity or negativity) towards the searc_term1
    sentiment_df1 = pd.DataFrame(twitter_data1, columns=["polarity", "tweet"])
    fig, ax = plt.subplots(figsize=(8, 6))
    # Plot histogram 
    sentiment_df1.hist(bins=[-1, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1],
                 ax=ax,
                 color="purple")
    plt.title("Overall Sentiment of " + search_terms[0] + " Tweets")
    plt.show()
    
    ## Determine overall sentiment (i.e. more positivity or negativity) towards the searc_term2
    sentiment_df2 = pd.DataFrame(twitter_data2, columns=["polarity", "tweet"])
    fig, ax = plt.subplots(figsize=(8, 6))
    # Plot histogram 
    sentiment_df2.hist(bins=[-1, -0.75, -0.5, -0.25, -0.15, 0.0, 0.25, 0.5, 0.75, 1],
                 ax=ax,
                 color="purple")
    plt.title("Overall Sentiment of " + search_terms[1] + " Tweets")
    plt.show()
    
    # Count total positive, negative and neutral tweets of searc_term1 using TextBlob
    pos_tweet1=0
    neg_tweet1=0
    neutral_tweet1=0
    for tweet in twitter_data1["tweet"]:
        analysis = TextBlob(tweet)
        if analysis.sentiment[0]>0:       
            pos_tweet1=pos_tweet1+1
        elif analysis.sentiment[0]<0:       
            neg_tweet1=neg_tweet1+1  
        else:       
            neutral_tweet1=neutral_tweet1+1
            
    # Count total positive, negative and neutral tweets of searc_term2 using TextBlob
    pos_tweet2=0
    neg_tweet2=0
    neutral_tweet2=0
    for tweet in twitter_data2["tweet"]:
        analysis = TextBlob(tweet)
        if analysis.sentiment[0]>0:       
            pos_tweet2=pos_tweet2+1
        elif analysis.sentiment[0]<0:       
            neg_tweet2=neg_tweet2+1  
        else:       
            neutral_tweet2=neutral_tweet2+1
         
    ## Plot bar chart to comapre sentiments of both searched tweets using searc_term1 and search_term2
    # data to plot
    n_groups = 3
    sentiments_tweets1 = (pos_tweet1,neg_tweet1,neutral_tweet1)
    sentiments_tweets2 = (pos_tweet2,neg_tweet2,neutral_tweet2)
    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    # Create bar for searched tweets using search_term1
    rects1 = plt.bar(index, sentiments_tweets1, bar_width,
    alpha=opacity,
    color='blue',
    label=search_terms[0])
    
    #Create bar for searched tweets using search_term2
    rects2 = plt.bar(index + bar_width, sentiments_tweets2, bar_width,
    alpha=opacity,
    color='orange',
    label=search_terms[1])
    
    # Set labels of x and y axis and title of plot
    plt.xlabel('Sentiments')
    plt.ylabel('Number of Tweets')
    plt.title('Sentiments Analysis of Searched Tweets')
    plt.xticks(index + bar_width, ('Positive', 'Negative', 'Neutral'))
    plt.legend()
    # Set layout and draw plot
    plt.tight_layout()
    plt.show()

  

if __name__ == "__main__":
    
    # AUTHENTICATION (OAuth)
    authenticate = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(authenticate)
    
    # Get the input arguments - search_term1, search_term2 and search_max
    parser = argparse.ArgumentParser(description='Twitter Search')
    parser.add_argument("--search_term1", action='store', dest='search_term1', default="facebook")
    parser.add_argument("--search_term2", action='store', dest='search_term2', default="google")
    parser.add_argument("--search_max", action='store', dest='search_max', default=40)
    args = parser.parse_args()
    
    # Make list of search terms
    search_terms = [args.search_term1,args.search_term2]
    search_max = int(args.search_max)
    
    print('\nSearch Terms: ',search_terms)
    print('Max Results: ',search_max)
    # Search tweets for both search terms 
    twitter_search(search_terms,search_max)
    
    # Perform data analysis of searched twitter data
    twitter_data_analysis(search_terms)
    
    