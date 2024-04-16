import streamlit as st
import time
import pandas as pd
import googleapiclient.discovery
import mysql.connector
from tabulate import tabulate
from googleapiclient.errors import HttpError
from sqlalchemy import create_engine, inspect
from sqlalchemy import text


api_key="AIzaSyBQYFRDBDuClwq0IvMeeFZsRarj7cIt3zU"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
engine = create_engine("mysql+mysqlconnector://root:""@localhost/mydatabase")


#empty dict and list declaration
#id="UCj22tfcQrWG7EMEKS0qLeEg"
#channel_id="UCkz0sTqhRemHL7w6cI8kpOw"
channel_id="UC0h1_R8oxsy68J-Z4dDvrKw"
playlist_ids=[]
comments={}
channel_data={}
videos_ids=[]
vedio_info={}
all_comments=[]
video_details=[]


#to fetch channel data
def channelDataFetch(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        #id="UCj22tfcQrWG7EMEKS0qLeEg"
        id= channel_id
    )
    response = request.execute()
    channel_data={
         'channel_id':channel_id,
        'channel_name':[response['items'][0]['snippet']['title']],
        'channel_description':[response['items'][0]['snippet']['description']],
        #'subcription_count':[response['items'][0]['statistics']['subscriptionCount']],
        'view_count':[response['items'][0]['statistics']['viewCount']],
        'video_count':[response['items'][0]['statistics']['videoCount']],
        'likes':[response['items'][0]['contentDetails']['relatedPlaylists']['likes']],
        'uploads':[response['items'][0]['contentDetails']['relatedPlaylists']['uploads']]  
          }
    
    return channel_data
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*********>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#

#fetch playlist ids
def fetch_playlistids(channel_id):
    request = youtube.playlists().list(
          part="snippet,contentDetails,status,id,player",
        channelId=channel_id
    )
    response = request.execute()

    playlist_ids=[]
    for i in range(0,len(response['items'])):
        playlist_ids.append(response['items'][i]['id'])
    return playlist_ids



#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<$$$$$$$$$$$>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
#get video id 
def get_video_ids( playlist_ids):
    
    for playlist_id in playlist_ids:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )   
        response = request.execute()

        for item in response['items']:
            videos_ids.append(item['contentDetails']['videoId'])

    return videos_ids



#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<@@@@@@@@@@>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#gathered vedio details
def get_video_details(videos_ids):    
    for video_id in videos_ids:
        request = youtube.videos().list(
            part="id,contentDetails,statistics,snippet",
            id=video_id
        )
        response = request.execute()
        
        if response['items']:  
            item = response['items'][0] 
            video_info = {
                
                'Channel_Name' : item['snippet']['channelTitle'],
                'channel_id':channel_id,
                'video_id': item['id'],
                'video_name': item['snippet']['title'],
                'video_description': item['snippet']['description'],
                 'Publish_Date' :item["snippet"]["publishedAt"],
                'likes': item['statistics'].get('likeCount', '0'), 
                'favorite_count': item['statistics'].get('favoriteCount', '0'),
                'comment_count': item['statistics'].get('commentCount', '0'),
                'view_count': item['statistics'].get('viewCount', '0'),
                 'Duration' : item["contentDetails"]["duration"],
                'Thumbnail' :item['snippet']['thumbnails']['default']['url'],
                'Caption_Status' :item['contentDetails']['caption']
            }
            #result = [(channel_id, channel_name, channel_des, view_count, video_count, likes, uploads)]
            video_details.append(video_info)
    
    return video_details



#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!!!!!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#get comments infos
def get_comments(videos_ids):
    all_comments = []
    for video_id in videos_ids:
        nextPageToken = None
        while True:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken 
            )
            response = request.execute()
            for item in response['items']:
                comment = {
                    'video_id':video_id,
                    'comment_description': item['snippet']['topLevelComment']['snippet']['textOriginal'],
                    'comment_author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'comment_published_at': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    'comment_id': item['id']
                }
                all_comments.append(comment)

            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break 

    return all_comments




#function calls
df=channelDataFetch(channel_id)
playlist_ids=fetch_playlistids(channel_id)
videos_ids=get_video_ids(playlist_ids)
vedio_info=get_video_details(videos_ids)
comments=get_comments(videos_ids)
videos_ids

