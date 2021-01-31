# Youtube-Crawler

This repository is for YouTube crawler. This crawler is based on Youtube DATA API 3.0. I use flask for simple&fast implementation and execution. Initial authentication for logging in through Google OAuth 2.0 on the flask web app, and a procedure for exchanging Access Token using a refresh token has been implemented. If you want to reuse this repository, you can create an app in Google API Console and set a redirect path and save client_secrets.json in the project path. Alternatively, it works if you replace the API key with token, but it is not recommended. Finally, the result is stored in DB, and DB is configured according to the attached query, and I used sqlite3. If you want to use other DBs, change the connection of the db_manage methods in Youtube_Crawler.class.

**You can see dev seq here!**
https://www.notion.so/hobbeskim/Youtube-Crawler-1064150849894cc79c640fce73257101

## Have to prepare
    Google App registration for using Youtube Data API 
    client_secrets.json # for initial Authentication

## Requirements
- #1 have to save recent 100 contents info from a channel that entered id. info have to contain
    - title
    - upload channel
    - upload time
    - description
    - views
    - likes
    - thumbnail url
    - video url

- #2 have to save info about channel that entered id. info have to contain
    - channel name
    - channel title
    - channel subscriber
    - channel description

## Schema and SQL query

![schema_erd](https://user-images.githubusercontent.com/57410044/106375400-02208d80-63cf-11eb-82c2-95b12a862790.png)

    ###########SQL
    ###########테이블 생성 쿼리

    ###########channel_info.tb 생성
    create table channel_info(
	    channel_id TEXT PRIMARY KEY,
	    channel_name TEXT,
	    subscribe_count INTEGER,
	    channel_description TEXT );


    ###########channel_upload.tb 생성
    create table channel_upload(
	    video_id TEXT PRIMARY KEY,
	    channel_id TEXT,
	    pub_time TEXT,
	    description TEXT,
	    thumbnail_URL TEXT,
	    video_URL TEXT ,
	    FOREIGN KEY(channel_id) 
	    REFERENCES channel_info(channel_id)
    );

    ############ table monthly_update_videos.tb 생성
    create table monthly_update_videos(
	    video_id TEXT PRIMARY KEY,
	    views INTEGER,
	    likes INTEGER,
	    comments INTEGER ,
	    upload TEXT,
	    FOREIGN KEY(video_id) 
	    REFERENCES channel_upload(video_id)
    );

## Execution
    #### CLI : at venv
    pip3 install -r requirements.txt

    #### CLI : if you wanna run at local
    export OAUTHLIB_INSECURE_TRANSPORT=1
    flask run -p 5000

    #### web GUI@localhost
    enter youtube channel id

    #### if first set or your refresh token expired, enter your browser http://localhost or other):5000/authorize 

    #### if your access token expired, enter refresh button on web ui

![webui](https://user-images.githubusercontent.com/57410044/106375804-c38cd200-63d2-11eb-9567-6e0e3af04f52.png)
![DBresult1](https://user-images.githubusercontent.com/57410044/106375830-fafb7e80-63d2-11eb-9d61-4cab6c802fcb.png)
![DBresult2](https://user-images.githubusercontent.com/57410044/106375838-08b10400-63d3-11eb-884a-499c06435e54.png)
![DBresult3](https://user-images.githubusercontent.com/57410044/106375850-21211e80-63d3-11eb-89ec-00baad1e2e9b.png)



@MIT license
if you wanna ask something about this repo, or donate , please mail to receiver@kakao.com 

