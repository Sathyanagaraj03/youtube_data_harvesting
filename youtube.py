#                                                             Simple Youtube Data Harvesting Project
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#importing necessary Libraries
import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from googleapiclient.errors import HttpError
import streamlit as st
import googleapiclient.discovery
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#initializing the list to store and access data globally
channel_details = []
upload_ids = []
video_ids = []
video_details = []
comment_data=[]
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#environmental variable Declaration,youtube variable declaration and database engine creation
#channel_id=UC0h1_R8oxsy68J-Z4dDvrKw UCttEB90eQV25-u_U-W2o8mQ UC6mcZ39IWdIXRijApU29r-Q
api_key="YOUR API KEY"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
engine = create_engine("mysql+mysqlconnector://root:""@localhost/YOUR_DATABASE_NAME")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#function get the details of channel using channel id
def get_channel_details(channel_ids):
    all_channel_data =[]
    request = youtube.channels().list(
        part ="snippet,contentDetails,statistics",
        id = channel_ids)  
    response = request.execute() 
    for i in response["items"]:
        channel_data = dict(
                    Channel_ID = i["id"], 
                    Channel_Name = i["snippet"]["title"],
                    Channel_Description = i['snippet']['description'],
                    Subscribers = i["statistics"]["subscriberCount"],
                    Channel_Views =i["statistics"]["viewCount"],
                    Video_Count = i["statistics"]["videoCount"], 
                    Playlist_ID = i["contentDetails"]["relatedPlaylists"]["uploads"]
                    ) 
        all_channel_data.append(channel_data)    
    return all_channel_data
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#function to fetch the playlist ids
def get_playlist_id(channel_ids):
    for i in get_channel_details(channel_ids) : 
        if i["Channel_ID"] == channel_ids:
            return i["Playlist_ID"] 
    return None  
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#function to fetch the video ids
def get_video_ids(channel_ids):
    playlist_id = get_playlist_id(channel_ids) 
    request = youtube.playlistItems().list(
        part ="contentDetails",  
        playlistId= playlist_id, 
        maxResults = 50) 
    response = request.execute()
    #video_ids = []
    for i in response['items']:
        data = i['contentDetails']['videoId']
        video_ids.append(data)
    next_page_token = response.get("nextPageToken") 
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part ="contentDetails",
                playlistId= playlist_id,
                maxResults = 50,
                pageToken = next_page_token)
            response = request.execute()

            for i in response['items']:
                data = i['contentDetails']['videoId']
                video_ids.append(data)

            next_page_token = response.get("nextPageToken") 
        
    return video_ids
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#function to collect necessay details of the videos
def get_video_details(video_ids):
    all_video_details = [] 

    for i in range(0,len(video_ids),50): 
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(video_ids[i:i+50])) 
        response = request.execute()
        for i in response["items"]:
            data = dict( Channel_Name = i['snippet']['channelTitle'],
                         Channel_Id = i['snippet']['channelId'],
                         Video_Id =  i["id"],
                         Video_Title = i["snippet"]["title"],
                         Publish_Date = i["snippet"]["publishedAt"],
                         Video_Description = i["snippet"]["description"],
                         View_Count =  i["statistics"]["viewCount"],
                         likes_count= i['statistics'].get('likeCount', '0'),
                         Favorite_Count = i["statistics"]["favoriteCount"],
                         Comment_Count = i["statistics"].get("commentCount"),
                         Duration = i["contentDetails"]["duration"],
                         Thumbnail = i['snippet']['thumbnails']['default']['url'],
                         Caption_Status = i['contentDetails']['caption'])

            all_video_details.append(data)
    return all_video_details
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    
#function to get comment data
def get_comment_data(video_ids):
    comment_data = []

    for i in video_ids:
        next_page_token = None
        comments_disabled = False

        while True: 
            try:
                request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=i,
                    maxResults=100,
                    pageToken=next_page_token
                )
                response = request.execute()

                # Extract comments from the current page
                for item in response["items"]:
                    data = dict(
                        Channel_ID=item["snippet"]["channelId"],
                        Comment_ID=item["snippet"]["topLevelComment"]["id"],
                        Video_ID=item["snippet"]["topLevelComment"]["snippet"]["videoId"],
                        Comment_Text=item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                        Comment_Author=item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        Comment_Published_Date=item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    )
                    comment_data.append(data)

                # Check for next page token
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break  # No more pages

            except HttpError as e:
                if e.resp.status == 403 and e.error_details[0]['reason'] == 'commentsDisabled':
                    comments_disabled = True
                    print(f"Comments are disabled for video ID: {i}")
                    break

                else:
                    raise

            if comments_disabled:
                break
    return comment_data
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#this function contains all function calls
#moreover it contains list to dataframe to store in sql database
#and also display the dataframes of channel data,video data,comment data
def main():
    st.title("Youtube Data Harvesting!!")
    channel_id = st.text_input("Enter YouTube Channel ID:", value="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    if channel_id:
        if st.button("Process Channel ID", key="process_button"):
            channel_details = get_channel_details(channel_id)
            channel_data_df=pd.DataFrame(channel_details)
            st.write("The channel Data:")
            st.write(channel_data_df)
            channel_data_df.to_sql(name='channel_db', con=engine, if_exists='append', index=False)
            upload_ids = get_playlist_id(channel_id)
            video_ids = get_video_ids(channel_id)
            video_details = get_video_details(video_ids)
            video_info_df=pd.DataFrame(video_details)
            st.write("The vedio Data:")
            st.write(video_info_df)
            video_info_df.to_sql(name='vedio_db', con=engine, if_exists='append', index=False)
            comment_data = get_comment_data(video_ids)
            comments_df=pd.DataFrame(comment_data)
            st.write("The comments Data:")
            st.write(comments_df)
            comments_df.to_sql(name='comment_db', con=engine, if_exists='append', index=False)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#this snippet contains the query to analyze and display the result of the query
        st.markdown("<h1 style='color: Grey;'># Analyze Data</h1>", unsafe_allow_html=True)
        st.markdown("<h3>Select a Query To Analyze</h3>", unsafe_allow_html=True)
#Dropdown for selecting Questions
    question = st.selectbox(
        'Please Select Your Question',
        ("Select a Query","1.Videos and their channels: Display video titles along with their corresponding channels.",
        "2.Channels with most videos: Highlight channels with the highest video counts and the number of videos.",
        "3.Top 10 viewed videos: Present the top 10 most viewed videos and their respective channel names.",
        "4.Comments per video: Display comment count and corresponding video names.",
        "5.Top liked videos: Show highest likes with respective channel names.",
        "6.Likes: Display total likes for each video along with names.",
        "7.Channel views: Showcase total views per channel with corresponding names.",
        "8.2022 Publishers: List channels that published videos in 2022.",
        "9.Avg. video duration: Present average duration for each channel's videos with names.",
        "10.Most commented videos: Show videos with the highest comments and their channel names."),help="Select pre written query to analyze data")
# Displaying the output for selected questions 
    if st.button("Query Database"):
        st.write(f"Analyzing data for question: {question}")
        if question == "1.Videos and their channels: Display video titles along with their corresponding channels.":
            query_1 = pd.read_sql_query("select Channel_Name,Video_Title from vedio_db order by channel_name;",engine)
            st.write(query_1)

        elif question == "2.Channels with most videos: Highlight channels with the highest video counts and the number of videos.":
            query_2 = pd.read_sql_query('''select channel_name,count(Video_ID) as video_count 
                                        FROM vedio_db group by channel_name order by video_count desc;''',engine)
            st.write(query_2)

        elif question == "3.Top 10 viewed videos: Present the top 10 most viewed videos and their respective channel names.":
            query_3 = pd.read_sql_query('''select * from (select channel_name, video_title,view_count, 
                                        rank() over(partition by channel_name order by view_count desc) as video_rank
                                        from vedio_db where view_count is not null) as ranking  
                                        where video_rank <= 10;''',engine)
            st.write(query_3)

        elif question == "4.Comments per video: Display comment count and corresponding video names.":
            query_4 = pd.read_sql_query('''select b.video_title,a.video_id, count(a.comment_id) as comment_count 
                                        from comment_db as a left join vedio_db as b on a.Video_Id = b.Video_Id 
                                        group by a.video_id order by count(a.comment_id) desc;''',engine)
            st.write(query_4)

        elif question == "5.Top liked videos: Show highest likes with respective channel names.":
            query_5 = pd.read_sql_query('''select a.channel_name, a.Video_Title, a.like_count from 
                                        (select channel_name, Video_Title,like_count,rank() 
                                        over(partition by channel_name order by like_count desc)as ranking 
                                        from vedio_db) as a where ranking = 1;''',engine)
            st.write(query_5)

        elif question == "6.Likes: Display total likes for each video along with names.":
            query_6 = pd.read_sql_query('''select video_title ,like_count from vedio_db;''',engine)
            st.write(query_6)

        elif question == "7.Channel views: Showcase total views per channel with corresponding names.":
            query_7 = pd.read_sql_query('''select Channel_Name , channel_views from channel_db;''',engine)
            st.write(query_7)

        elif question == "8.2022 Publishers: List channels that published videos in 2022.":
            query_8 = pd.read_sql_query('''select distinct channel_name from vedio_db 
                                        where extract(year from publish_date) = 2022;''',engine)
            st.write(query_8)

        elif question == "9.Avg. video duration: Present average duration for each channel's videos with names.":
            query_9 = pd.read_sql_query('''SELECT b.channel_name,
                                        AVG(CAST(SUBSTRING(a.duration, 3, CHAR_LENGTH(a.duration) - 1) AS DECIMAL(10,2))) AS average_duration_in_minutes
                                        FROM vedio_db AS a
                                        JOIN channel_db AS b ON a.channel_id = b.channel_id
                                        GROUP BY b.channel_name;''',engine)
            st.write(query_9)

        elif question == "10.Most commented videos: Show videos with the highest comments and their channel names.":
            query_10 = pd.read_sql_query('''SELECT b.channel_name,b.video_title, count(a.comment_text) as comment_count 
                                            from comment_db as a left join vedio_db as b 
                                            on a.video_id = b.video_id group by a.video_id,b.channel_name 
                                            order by count(a.comment_text) desc ;''',engine)
            st.write(query_10)  
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#              
#these piece of code is technically start of the project and also codewise end of the project
if __name__ == "__main__":
    main()
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    
