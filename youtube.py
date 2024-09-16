import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from googleapiclient.errors import HttpError
import streamlit as st
import googleapiclient.discovery
import time

channel_details = []
upload_ids = []
video_ids = []
video_details = []
comment_data=[]
comments_df={}
channel_data_df={}
video_info_df={}
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#environmental variable Declaration,youtube variable declaration and database engine creation
#channel_id=UC0h1_R8oxsy68J-Z4dDvrKw UCttEB90eQV25-u_U-W2o8mQ UC6mcZ39IWdIXRijApU29r-Q
api_key="AIzaSyBtWxqZ1bh6geM7nlnmgrfeyaDocO1F6do"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
engine = create_engine("mysql+mysqlconnector://root:""@localhost/demo")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#function get the details of channel using channel id
def Scratch_data(channel_id): 
    channel_details = get_channel_details(channel_id)
    #channel_data_df = pd.DataFrame(channel_details)
            

    video_ids = get_video_ids(channel_id)
    video_details = get_video_details(video_ids)
    #video_info_df = pd.DataFrame(video_details)
    comment_data = get_comment_data(video_ids)
    #comments_df = pd.DataFrame(comment_data)
def view_details(channel_id):
            
            channel_details = get_channel_details(channel_id)
            channel_data_df = pd.DataFrame(channel_details)
            

            video_ids = get_video_ids(channel_id)
            video_details = get_video_details(video_ids)
            video_info_df = pd.DataFrame(video_details)


            comment_data = get_comment_data(video_ids)
            comments_df = pd.DataFrame(comment_data)
            channel_data_df = pd.DataFrame(channel_details)
            st.write("The channel Data:")
            video_info_df = pd.DataFrame(video_details)
            st.write(channel_data_df)
            st.write("The video Data:")
            st.write(video_info_df)
            comments_df = pd.DataFrame(comment_data)
            st.write("The comments Data:")
            st.write(comments_df)
def sql_tables():
                
            channel_data_df = pd.DataFrame(channel_details)
            video_info_df = pd.DataFrame(video_details)
            comments_df = pd.DataFrame(comment_data)
            channel_data_df.to_sql(name='channel_db', con=engine, if_exists='append', index=False)
            video_info_df.to_sql(name='vedio_db', con=engine, if_exists='append', index=False)
            comments_df.to_sql(name='comment_db', con=engine, if_exists='append', index=False)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
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

def main():
    st.set_page_config(
    page_title="Youtube Data Harvesting",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded")
    
    page_element="""
           <style>
           [data-testid="stAppViewContainer"]{
           
           background-size: auto;
           background-repeat:repeat;
           }
        

        /* Add custom CSS styles here */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333333;
            line-height: 1.6;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 8px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
           .title-text {
            font-size: 24px;
            font-weight: bold;
            color: #FF5733; /* Custom title color */
            margin-bottom: 20px;
        }
        
      </style>
        """
    
    st.markdown(page_element, unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["home","Channel Data Display","Query And Outputs"])
    with t1:
     st.markdown("<h1 style='text-align: center;font-family:Italic; color: red';>Youtube Data Harvesting </h1>", unsafe_allow_html=True)
    #col1, col2, col3 = st.columns([2, 1, 1])
     channel_id = st.text_input("Enter YouTube Channel ID:", value="UCttEB90eQV25-u_U-W2o8mQ")
     if channel_id:
       
       if st.button("Process Channel ID", key="process_button"):
             Scratch_data(channel_id)
             st.success("Scratched the data")
      
            
    with t2:
             st.markdown("<h1 style='text-align: center;font-family:Italic; color: red';>View Channel Details </h1>", unsafe_allow_html=True)
             st.subheader("Click the view the Scratched Data")
             if st.button("view data",key="views"):
                view_details(channel_id)
             st.subheader("Do you want migrate data inot MYSQL Server?")
             if st.button("Migrate data"):
                sql_tables()
                st.success("stored to Database")
    with t3: 
               st.write(" ")
               st.markdown("<h1 style='text-align: center;font-family:Italic; color: red';>Query Databas</h1>", unsafe_allow_html=True)


               question = st.selectbox(
        'Please Select Your Question',
        ("Select a Query",
         "1. Videos and their channels: Display video titles along with their corresponding channels.",
         "2. Channels with most videos: Highlight channels with the highest video counts and the number of videos.",
         "3. Top 10 viewed videos: Present the top 10 most viewed videos and their respective channel names.",
         "4. Comments per video: Display comment count and corresponding video names.",
         "5. Top liked videos: Show highest likes with respective channel names.",
         "6. Likes: Display total likes for each video along with names.",
         "7. Channel views: Showcase total views per channel with corresponding names.",
         "8. 2022 Publishers: List channels that published videos in 2022.",
         "9. Avg. video duration: Present average duration for each channel's videos with names.",
         "10. Most commented videos: Show videos with the highest comments and their channel names."),
        help="Select a pre-written query to analyze data"
    )

    
               st.write(f"Analyzing data for question: {question}")
               if question == "1. Videos and their channels: Display video titles along with their corresponding channels.":
                 query_1 = pd.read_sql_query("SELECT Channel_Name, Video_Title FROM video_db ORDER BY Channel_Name;", engine)
                 st.write(query_1)

               elif question == "2. Channels with most videos: Highlight channels with the highest video counts and the number of videos.":
                 query_2 = pd.read_sql_query('''SELECT Channel_Name, COUNT(Video_ID) AS Video_Count 
                                            FROM video_db 
                                            GROUP BY Channel_Name 
                                            ORDER BY Video_Count DESC;''', engine)
                 st.write(query_2)

               elif question == "3. Top 10 viewed videos: Present the top 10 most viewed videos and their respective channel names.":
                  query_3 = pd.read_sql_query('''SELECT Channel_Name, Video_Title, View_Count 
                                            FROM video_db 
                                            ORDER BY View_Count DESC 
                                            LIMIT 10;''', engine)
                  st.write(query_3)

               elif question == "4. Comments per video: Display comment count and corresponding video names.":
                  query_4 = pd.read_sql_query('''SELECT b.Video_Title, a.Video_ID, COUNT(a.Comment_ID) AS Comment_Count 
                                            FROM comment_db a 
                                            LEFT JOIN video_db b ON a.Video_ID = b.Video_ID 
                                            GROUP BY a.Video_ID 
                                            ORDER BY Comment_Count DESC;''', engine)
                  st.write(query_4)

               elif question == "5. Top liked videos: Show highest likes with respective channel names.":
                   query_5 = pd.read_sql_query('''SELECT a.Channel_Name, a.Video_Title, a.Likes_Count 
                                            FROM video_db a 
                                            ORDER BY Likes_Count DESC 
                                            LIMIT 10;''', engine)
                   st.write(query_5)

               elif question == "6. Likes: Display total likes for each video along with names.":
                  query_6 = pd.read_sql_query('''SELECT Video_Title, Likes_Count 
                                            FROM video_db;''', engine)
                  st.write(query_6)

               elif question == "7. Channel views: Showcase total views per channel with corresponding names.":
                  query_7 = pd.read_sql_query('''SELECT DISTINCT Channel_Name, Channel_Views 
                                            FROM channel_db;''', engine)
                  st.write(query_7)

               elif question == "8. 2022 Publishers: List channels that published videos in 2022.":
                  query_8 = pd.read_sql_query('''SELECT DISTINCT Channel_Name 
                                            FROM video_db 
                                            WHERE YEAR(Publish_Date) = 2022;''', engine)
                  st.write(query_8)

               elif question == "9. Avg. video duration: Present average duration for each channel's videos with names.":
                   query_9 = pd.read_sql_query('''SELECT Channel_Name, AVG(Duration) AS Avg_Duration 
                                            FROM video_db 
                                            GROUP BY Channel_Name;''', engine)
                   st.write(query_9)

               elif question == "10. Most commented videos: Show videos with the highest comments and their channel names.":
                  query_10 = pd.read_sql_query('''SELECT b.Channel_Name, b.Video_Title, COUNT(a.Comment_Text) AS Comment_Count 
                                             FROM comment_db a 
                                             LEFT JOIN video_db b ON a.Video_ID = b.Video_ID 
                                             GROUP BY a.Video_ID, b.Channel_Name 
                                             ORDER BY Comment_Count DESC;''', engine)
                  st.write(query_10)

if __name__ == "__main__":
    main()
