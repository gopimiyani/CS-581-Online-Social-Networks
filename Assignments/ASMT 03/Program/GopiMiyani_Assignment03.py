#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:43:46 2019

@AUTHOR: Gopi Miyani    10437266

PURPOSE OF PROGRAM: To retrieve some data from the YouTube API and do some processing on that data.

PROGRAM SPECIFICATIONS:
    Accept a search term and a maximum number of results from the user.  
    This can be done either by use of an argument list or by prompting the user for the information.  
    eg: python3   youtube_data.py   --search_term   mysearch   --search_max   mymaxresultsor:
        *** Enter your search term:  (user input)*** Enter maximum results:  (user input)Use the search term to do a YouTube search. 
        Write the results to a .csv file that will remain in existence when the program is completed.Perform some type of analysis on the results of your search.  
        For example, you could find the best-liked and least-liked videos from the search.
        Print the search term, search max, and results of your analysis.

RUN INSTRUCTIONS:
# to run from terminal window:  
#      python3 youtube_data.py --search_term mysearch --search_max mymaxresults
#  where:  search_term = the term you want to search for;  default = music
#     and  search_max = the maximum number of results;  default = 30


"""

from apiclient.discovery import build      # use build function to create a service object

import argparse       #  need for parsing the arguments in the command line
import csv            #  need since search results will be contained in a .csv file
import unidecode      #  need for processing text fields in the search results
import pandas as pd   #  need for reading csv file as dataframe
import numpy as np    #  need for data  analysis

# put your API key into the API_KEY field below, in quotes
API_KEY = "AIzaSyBLiTz3D0V6CrBoNRmh0ZoiC9P018XrC10"

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

#  function youtube_search retrieves the YouTube records

def youtube_search(options):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    
    search_response = youtube.search().list(q=options.search_term, part="id,snippet", maxResults=options.search_max).execute()
    print("\nSearch Term: ",options.search_term)
    print("Search Max: ",options.search_max)
    # create a CSV output for results video list, and write the headings line    
    csvFile = open('video_results.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["TITLE","ID","VIEWS","LIKES","DISLIKES","COMMENTS","FAVORITES"])
    
    print("\nRetriving Data...")
    # search for videos matching search term; write an output line for each
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  
            videoId = search_result["id"]["videoId"]
            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            for video_results in video_response.get("items",[]):
                viewCount = video_results["statistics"]["viewCount"]
                if 'likeCount' not in video_results["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_results["statistics"]["likeCount"]
                if 'dislikeCount' not in video_results["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_results["statistics"]["dislikeCount"]
                if 'commentCount' not in video_results["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_results["statistics"]["commentCount"]
                if 'favoriteCount' not in video_results["statistics"]:
                    favoriteCount = 0
                else:
                    favoriteCount = video_results["statistics"]["favoriteCount"]
                    
            csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount])
    print('Search results stored in video_results.csv')
    csvFile.close()
  
# fucntion youtube_data_analysis analyze serached youtube data and display analysis
def youtube_data_analysis(csvfileName):
    
    # read csv file using pandas library
    youtube_data=pd.read_csv(csvfileName)
    #youtube_data=youtube_data.reset_index(drop=True, inplace=True)
    
    print('\n*********   Data analysis on searched youtube data   *********\n\n')
    
    ## Maximum and minimum viewed videos
    maxViews=np.where(youtube_data["VIEWS"] == np.amax(youtube_data["VIEWS"]))
    maxViews_Row=youtube_data.iloc[maxViews[0],:]
    print('>> Most Viewed Video <<\nTitle: ',(maxViews_Row.TITLE).to_string(index=False))
    print('Number of views: ',maxViews_Row.VIEWS.to_string(index=False))
    
    minViews=np.where(youtube_data["VIEWS"] == np.amin(youtube_data["VIEWS"]))
    minViews_Row=youtube_data.iloc[minViews[0],:]
    print('\n>> Least Viewed Video <<\nTitle: ',minViews_Row.TITLE.to_string(index=False))
    print('Number of views: ',minViews_Row.VIEWS.to_string(index=False))
    
    ## Best liked and least liked videos 
    maxLikes=np.where(youtube_data["LIKES"] == np.amax(youtube_data["LIKES"]))
    maxLikes_Row=youtube_data.iloc[maxLikes[0],:]
    print('\n\n>> Best liked video <<\nTitle: ',maxLikes_Row.TITLE.to_string(index=False))
    print('Number of likes: ',maxLikes_Row.LIKES.to_string(index=False))
   
    minLikes=np.where(youtube_data["LIKES"] == np.amin(youtube_data["LIKES"]))
    minLikes_Row=youtube_data.iloc[minLikes[0],:]
    print('\n>> Least liked video <<\nTitle: ',minLikes_Row.TITLE.to_string(index=False))
    print('Number of likes: ',minLikes_Row.LIKES.to_string(index=False))
    
    ## Most disliked and least disliked videos
    maxDislikes=np.where(youtube_data["LIKES"] == np.amax(youtube_data["LIKES"]))
    maxDislikes_Row=youtube_data.iloc[maxDislikes[0],:]
    print('\n\n>> Most disliked video <<\nTitle: ',maxDislikes_Row.TITLE.to_string(index=False))
    print('Number of disikes: ',maxDislikes_Row.DISLIKES.to_string(index=False))
   
    minDislikes=np.where(youtube_data["LIKES"] == np.amin(youtube_data["LIKES"]))
    minDislikes_Row=youtube_data.iloc[minDislikes[0],:]
    print('\n>> Least disliked video <<\nTitle: ',minDislikes_Row.TITLE.to_string(index=False))
    print('Number of disikes: ',minDislikes_Row.DISLIKES.to_string(index=False))
    
    ## Most commented and least commented videos
    maxComments=np.where(youtube_data["COMMENTS"] == np.amax(youtube_data["COMMENTS"]))
    maxComments_Row=youtube_data.iloc[maxComments[0],:]    
    print('\n\n>> Most commented video <<\nTitle: ',maxComments_Row.TITLE.to_string(index=False))
    print('Number of comments: ',maxComments_Row.COMMENTS.to_string(index=False))
   
    minComments=np.where(youtube_data["COMMENTS"] == np.amin(youtube_data["COMMENTS"]))
    minComments_Row=youtube_data.iloc[minComments[0],:]
    print('\n>> Least commented video <<\nTitle: ',minComments_Row.TITLE.to_string(index=False))
    print('Number of comments: ',minComments_Row.COMMENTS.to_string(index=False))
    
    
    
# main routine
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YouTube Search')
    parser.add_argument("--search_term", default="music")
    parser.add_argument("--search_max", default=30)
    args = parser.parse_args()
    youtube_search(args)
    youtube_data_analysis('video_results.csv')
