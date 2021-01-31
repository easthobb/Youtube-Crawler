import requests
import os
import json
import csv
import sqlite3

class Youtube_Crawler(object):

    def __init__(self, channel_id):
        print("Crawler initiating...")

        # set API's base URL 
        self.BASE_URL = "https://youtube.googleapis.com/youtube/v3/"

        # Attributes of Crawler
        self._token = "" # temp API key
        self.channel_name = ""
        self.channel_id = channel_id  # input parameter
        self._max_result = 50  # temp

        # Attributes for channel info crawling
        
        self.channel_info_list = [] #[channel_id, channel_name, channel_description, channel_subscriberCount]
        
        # Attributes for Activity info Crawling
        self.videos_id_list = [] 

        # Attributes for videos crawling
        self.video_info_list = []

    @property
    def max_result(self):
        return self._max_result

    @max_result.setter
    def max_result(self, value):
        self._max_result = value
        
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self,value):
        self._token = value


    # 클래스에서 입력받은 채널 id의 유효성 검사
    # input channel_name, return channel_id or -1
    def verify_channel_id(self,channel_id):
        
        print("verify channel name...", channel_id)
        query = self.BASE_URL + f"channels?part=snippet&id={channel_id}&fields=items(id)&access_token={self._token}"
        verify = requests.get(query)
        try:
            print(verify.json())
            if 'items' in verify.json():
                return verify.json()['items'][0]['id']
            else:
                print("items are not in the response")
                return -1
        except:
            print("something go wrong")
            return -1

    # channel_id를 이용해 API 요청 위한 URL로 변환
    # input channel_id return URL
    def create_channel_URL(self,channel_id):
        
        print("creating channel info request URL ...")
        URL = self.BASE_URL + f"channels?part=snippet,contentDetails,statistics&id={channel_id}"
        URL = URL + f"&fields=items(id,snippet.title,snippet.description,statistics.subscriberCount)"
        URL = URL + f"&access_token={self._token}"
        print(URL) # for debug
        return URL

    
    # 입력받은 URL 을 요청하는 함수
    # input : URL , return json
    def request_channel_URL(self,URL):
        
        ## 채널 일반 정보를 요청하는 부분
        try:
            response = requests.get(URL)
            return response
        except:
            print("request channel: something go wrong!")
        

    # 채널 정보에 대해 입력받은 json을 발라내는 함수(attributes 중 channel_info_list에 저장)
    # input: json output None
    def parse_channel_json(self,channel_json):
    
        response = channel_json.json() #response로 json 변환 to dict 
        if 'items' in response:
            self.channel_info_list.append(response['items'][0]['id'])
            self.channel_info_list.append(response['items'][0]['snippet']['title'])
            if 'subscriberCount' in response['items'][0]['statistics']: # in case of NULL Count
                self.channel_info_list.append(response['items'][0]['statistics']['subscriberCount'])
            else:
                self.channel_info_list.append("0")
            self.channel_info_list.append(response['items'][0]['snippet']['description'])
            print(self.channel_info_list)
        else:
            print('wrong response')


    # channel_id를 parameter로 채널 활동을 요청위한 URL 생성함수
    # input: channel_id ,return URL
    def create_activity_URL(self,channel_id):
        print("creating activity info request URL...")
        URL = self.BASE_URL + f"activities?part=snippet,contentDetails&channelId={channel_id}"
        URL = URL + f"&maxResults={self._max_result}"
        URL = URL + f"&access_token={self._token}"
        print(URL)
        return URL

    # 입력받은 URL을 요청하는 함수 # 추가 마지막 컨텐츠의 게시 시간까지, #APIbug
    # input : URL,return json 
    def request_activity_URL(self,URL):
        try:
            response = requests.get(URL)
            print(response)
            print("activity got response")
            # Page 끝에 도달시 nextPageToken 없음
            if 'nextPageToken' in response.json():
                next_page_token = response.json()['nextPageToken']
            else:
                print("activity! page end")
                next_page_token = None
        except:
            print("request activity: something go wrong")
        
        return response, next_page_token 
        
       
    # 채널 활동 정보에 대해 입력받은 json을 발라내는 함수(attributes 중 videos_id_list에 저장 )
    # input: json output None
    def parse_activity_json(self,activity_json):
        ## while 들어가야 함.
        for activity in activity_json.json()['items']:
            if 'upload' in activity['contentDetails']:
                self.videos_id_list.append(activity['contentDetails']['upload']['videoId'])
            else:
                pass
        print(self.videos_id_list)
        
    # video_id를 종합해 URL 형태로 만드는 함수 - maxing에 의존하지 않음
    # input: videos_id_list, return URL
    def create_videos_URL(self,videos_id_list):
        #https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=nV8eAWmVEk4,XyN-LascAL0&fields=items(statistics,snippet.title)
        #video_info_list : [[video_id, channelId, title, discription, upload_date, viewCount, likeCount,  commentCount, thumbnail_URL, video_URL],...]
        #max list = 50 
        URL = self.BASE_URL +f"videos?part=snippet,contentDetails,statistics&id="
        URL = URL + ",".join(videos_id_list)
        URL = URL + f"&access_token={self._token}"

        return URL

    # 입력받은 URL을 요청하는 함수
    # input : URL , return response(json)
    def request_video_URL(self,URL):
        try:
            response = requests.get(URL)
            return response
        except:
            print("request_video_URL : something go wrong!")


    # 응답으로 받은 json에서 필요한 정보를 발라내는 함수
    # input json output None
    def parse_videos_json(self,video_json):
        
        json=video_json.json() 
        for video in json['items']:
            try:
                video_id = video['id']
                title = video['snippet']['title']
                channel_id = video['snippet']['channelId']
                pub_time =video['snippet']['publishedAt']
                description = video['snippet']['description']
                views = video['statistics']['viewCount']
                likes = video['statistics']['likeCount']
                comments = video['statistics']['commentCount']
                thumbnail_URL = video['snippet']['thumbnails']['default']['url']
                video_URL = "https://www.youtube.com/watch?v=" + video_id
                video_info = [video_id,title,channel_id,pub_time,description,views,likes,comments,thumbnail_URL,video_URL]
                self.video_info_list.append(video_info)
            except:
                print(video," is can't parse")
    
    # 채널정보 : channel_info_list 를 DB에서 관리하는 메소드
    # input None, output None (channel_info_list에 의존적)
    def db_manage_channel_info(self):
        c_list=self.channel_info_list
        channel_id = c_list[0]
        channel_name = c_list[1]
        subscribe_count = int(c_list[2])
        channel_description = c_list[3]

        try:
            # DB connect
            conn = sqlite3.connect('crawler.db')
            cur = conn.cursor()
            print("connect")

            # DB 조회
            cur.execute(f"SELECT channel_id from channel_info;")
            db_list = cur.fetchall()
            db_channel_id_list = []
            for element in list(map(list, db_list)):
                db_channel_id_list.append(element[0])
            print("show")

            # DB 기등록된 채널
            if channel_id in db_channel_id_list:
                cur.execute(
                    f"update channel_info set channel_name = \"{channel_name}\", subscribe_count={subscribe_count}, channel_description=\"{channel_description}\" where channel_id = \"{channel_id}\";")
            else:
                cur.execute("INSERT INTO channel_info VALUES(?,?,?,?)", c_list)

            conn.commit()
            conn.close()
            print("done")
        except:
            conn.commit()
            conn.close()
            print("error")

        print(db_channel_id_list)

    # 채널업로드정보  : video_info_list 중 일부를 DB에서 관리하는 메소드
    # input None, output None (video_info_list에 의존적)
    def db_manage_channel_upload(self):
        
        video_info_list=self.video_info_list #멤버 리스트 할당

        try:
            # DB connect
            conn = sqlite3.connect('crawler.db')
            cur = conn.cursor()
            print("DB connect...")

            # 테이블에 존재하는 video_id 한번에 받아옴
            cur.execute("SELECT video_id from channel_upload;")
            db_list = cur.fetchall()
            db_video_id_list = []
            for element in list(map(list, db_list)):  # 튜플의 리스트 -> 리스트로
                db_video_id_list.append(element[0])
            print("GET channel_upload ...")

            # 개별 video에 대해 반복 조회 -> 삽입 업데이트 분기
            for video_info in video_info_list:

                # 개별 video의 영상 정보 매핑
                video_id = video_info[0]  # 조회를 위한 video_id : KEY
                channel_id = video_info[2]  # 채널아이디
                pub_time = video_info[3]  # 영상업로드시간
                description = video_info[4].replace('"','').replace('@','')  # 영상설명
                thumbnail_URL = video_info[8]  # 영상 썸네일 url
                video_URL = video_info[9]  # 영상 시청 url

                if video_id in db_video_id_list:
                    # update - 채널 id & 영상 id 안바꿈
                    cur.execute(f'''
                    update channel_upload set 
                    pub_time = "{pub_time}",
                    description = "{description}",
                    thumbnail_URL = "{thumbnail_URL}",
                    video_URL = "{video_URL}"
                    where video_id = "{video_id}";
                    ''')
                    print(video_id, "is updated")

                else:
                    print("pass")
                    # insert - 모두 새로 삽입
                    cur.execute(f'''
                    insert into channel_upload values("{video_id}","{channel_id}","{pub_time}","{description}","{thumbnail_URL}","{video_URL}");''')
                    print("pass")
                    print(video_id, "is inserted")
            
            conn.commit()
            conn.close()
            print("done")

        except Exception as e:
            conn.commit()
            conn.close()

            print(video_id,description)
            print(e)
            print("error")
    
    # 비디오정보 : video_info_list 중 일부를 DB에서 관리하는 메소드
    # input None, output None(video_info_list
    def db_manage_monthly_upload(self):
        #월간 테이블 존재 여부 확인 - 원래 계획은 달 단위로 일단은 한 테이블에 적재하는 것으로....
        video_info_list=self.video_info_list

        try:
            # DB connect
            conn = sqlite3.connect('crawler.db')
            cur = conn.cursor()
            print("DB connect...")

            # 테이블에 존재하는 video_id 한번에 받아옴
            cur.execute("SELECT video_id from monthly_update_videos;")
            db_list = cur.fetchall()
            db_video_id_list = []
            for element in list(map(list, db_list)):  # 튜플의 리스트 -> 리스트로
                db_video_id_list.append(element[0])
            print("GET monthly_upload_video ...")
            print(db_video_id_list)
            # 개별 video에 대해 반복 조회 -> 삽입 업데이트 분기
            for video_info in video_info_list:
                # 개별 video의 영상 정보 매핑
                video_id = video_info[0]  # 조회를 위한 video_id : KEY
                views = int(video_info[5])  # 조회수
                likes = int(video_info[6])  # 영상 좋아요 수
                comments = int(video_info[7]) # 영상 댓글 수
                upload = video_info[3].split("T")[0] # 영상 업로드 시간
                print(video_id,views,likes,comments,upload)
                
                if video_id in db_video_id_list:
                    # update - 채널 id 불변
                    
                    cur.execute(f'''
                    update monthly_update_videos set 
                    views = "{views}",
                    likes = "{likes}",
                    comments = "{comments}",
                    upload = "{upload}"
                    where video_id = "{video_id}";
                    ''')
                    print(video_id, "is updated")

                else:
                    print("pass")
                    # insert - 모두 새로 삽입
                    cur.execute(f'''
                    insert into monthly_update_videos values("{video_id}","{views}","{likes}","{comments}","{upload}");
                    ''')
                    print(video_id, "is inserted")
            
            conn.commit()
            conn.close()
            print("done")

        except:
            conn.commit()
            conn.close()
            print("error")


    
    def start(self):

        print("start crawler...")
        self.channel_id = self.verify_channel_id(self.channel_id)
        print('got channel id : ',self.channel_id)

        ## channel info get sequence - 채널 정보를 받아오는 시퀀스
        channel_URL = self.create_channel_URL(self.channel_id)
        channel_json = self.request_channel_URL(channel_URL)
        self.parse_channel_json(channel_json)
        print("channel info :",self.channel_info_list)

        # channel activity get sequence - 채널의 최근 업로드 비디오 100개를 받아오는 시퀀스
        activity_URL = self.create_activity_URL(self.channel_id)
        activity_response, next_page_token =self.request_activity_URL(activity_URL)
        self.parse_activity_json(activity_response)
        earlier_video_pub_time = activity_response.json()['items'][-1]['snippet']['publishedAt'] #마지막 인덱스의 업로드시간 값 접근
        print("next page: ",next_page_token)

        if next_page_token is not None: # 첫 페이지에서 끝나지는 않은지 검사
            while True:#이후 페이지가 있을 경우publishedBefore=2020-12-01T00:00:00Z
                print("video_id_list got :",len(self.videos_id_list))
                print("next page requesting...")
                temp = activity_URL  + "&publishedBefore=" + earlier_video_pub_time.split("+")[0]+"Z"
                print(temp)
                 
                activity_response, next_page_token =self.request_activity_URL(activity_URL + "&publishedBefore=" + earlier_video_pub_time.split("+")[0]+"Z")
                
                #컨텐츠 마지막 시간검사
                if len(activity_response.json()['items']) != 0: 
                    print(len(activity_response.json()['items']))
                    earlier_video_pub_time = activity_response.json()['items'][-1]['snippet']['publishedAt']

                self.parse_activity_json(activity_response)
                print("video_id_list got :",len(self.videos_id_list))
                if (next_page_token==None) or (len(list(set(self.videos_id_list)))>100) :
                    print("page end or videos over 100")
                    break
        else:
            print("requested page has a few videos. under",self._max_result)

        ## video 최근순으로 100개로 줄임
        self.videos_id_list = self.videos_id_list[0:100]
        print("video_id_list got :",len(list(set(self.videos_id_list))))

        ## video info get sequence - done
        for i in range(0,len(self.videos_id_list),self._max_result): ## 멕스 리절트 인자만큼 아이디 쿼리 날림
            video_URL = self.create_videos_URL(self.videos_id_list[i:i+self._max_result])#인덱싱해서 URL 따로날림
            video_json = self.request_video_URL(video_URL) #URL request
            self.parse_videos_json(video_json) # 해당하는 갯수만큼 json 발라냄
            
        print("the NUMBER of video IS",len(self.video_info_list))
        
        ## DB managing
        self.db_manage_channel_info()
        self.db_manage_channel_upload()
        self.db_manage_monthly_upload()

        

           
if __name__ == "__main__":
    channel_id = input()
    crawler = Youtube_Crawler(channel_id)
    crawler.start()
