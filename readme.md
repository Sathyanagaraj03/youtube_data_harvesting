Youtube data Harvesting Project
 
 Youtube Data Harvesting project is brought up to build an user-friendly analyzing of Youtube data using a Streamlit Application.The data are scraped from the Youtube API's and migrated to a SQL Database from which the data can be easily analysed and result will be displayed in the streamlit application
 
Prerequities needed:
        vscode
        python IDE
        XAMPP 
To run this project 
    the following steps to be followed:
        1. Installation:
            !pip install sqlalchemy mysqlclient google-api-python-client pandas streamlit googleapiclient
        2.To use this project, follow these steps:

          =>Clone the repository: git clone
          =>Install the required packages
          =>Run the Streamlit app: streamlit run app.py
          =>Access the app in your browser at http://localhost:8501

Key features of the Project:
      Collect information from Youtube API
                 Channel Details
                 Vedio Details
                 Comment Details
       Convert gathered Data into some format 
       Store it into an SQL Database
       Analyze the Data
       Displays analyzed Result in  the Streamlit Apllication
References
          Python Documentation
          Streamlit Documentation
          YouTube API Documentation
          MySQL Documentation
          SQLAlchemy Documentation
          Pandas Documentation
        


# YouTube Data Harvesting and Warehousing

Youtube Data Harvesting project is brought up to build an user-friendly analyzing of Youtube data using a Streamlit Application.The data are scraped from the Youtube API's and migrated to a SQL Database from which the data can be easily analysed and result will be displayed in the streamlit application

## Tools and Libraries Used

This project leverages the following components:

- **Python:** 
- **Streamlit:** 
- **Google API Client:** 
- **MySQL:** 


## Required Libraries

1. googleapiclient.discovery
2. streamlit
3. sqlalchemy
4. pymysql
5. pymongo
6. pandas

## Features

The YouTube Data Harvesting and Warehousing application offers the following functions:

- Collect information from Youtube API
                - Channel Details
                -Vedio Details
                -Comment Details
-Convert gathered Data into some format 
-Store the formatted data into an SQL Database
-Analyze the Data
-Displays analyzed Result in  the Streamlit Apllication

## Installation and Setup

To run the YouTube Data Harvesting and Warehousing project, follow these steps:
1.**vscode or any platform** Ensure that the vscode or any other IDE is installed on your machine.
1. **Install Python:** Ensure that the Python programming language is installed on your machine.

2. **Install Required Libraries:**
    ```
    pip install streamlit sqlalchemy PyMySQL pandas google-api-python-client dotenv
    ```

3. **Set Up Google API:**
    - Create a Google API project on the [Google Cloud Console](https://console.cloud.google.com/).
    - Obtain API credentials (JSON file) with access to the YouTube Data API v3.
    - Place the API credentials file in the project directory under the name `google_api_credentials.json`.

4. **Configure Database:**
    - Set up a MySQL database and ensure it is running.
  
5. **Configure Application:**
    - Copy the `config.sample.ini` file and rename it to `config.ini`.
    - Update the `config.ini` file with your Google API credentials and MySQL connection details.

6. **Run the Application:**
    ```
    git clone https://github.com/Sathyanagaraj03/GUVI/blob/main
    streamlit run filename.py
    ```
   Access the Streamlit application at `http://localhost:8501` in your web browser.


## References

- [Python Documentation](https://docs.python.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
  


