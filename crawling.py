import requests
import os
import json
import csv


class Youtube_Crawler(object):

    def __init__(self, channel_id):
        print("Crawler initiating...")

        # set API's base URL 
        self.BASE_URL = "https://youtube.googleapis.com/youtube/v3/"

        # Attributes of Crawler
        self.token =   # temp API key
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

    # 클래스에서 입력받은 채널 id의 유효성 검사
    # input channel_name, return channel_id or -1
    def verify_channel_id(self,channel_id):
        
        print("verify channel name...", channel_id)
        query = self.BASE_URL + f"channels?part=snippet&id={channel_id}&fields=items(id)&key={self.token}"
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
        URL = URL + f"&key={self.token}"
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
        URL = URL + f"&key={self.token}"
        print(URL)
        return URL

    # 입력받은 URL을 요청하는 함수
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
        URL = URL + f"&key={self.token}"

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
        pass

    # 채널업로드정보  : video_info_list 중 일부를 DB에서 관리하는 메소드
    # input None, output None (video_info_list에 의존적)
    def db_manage_channel_upload(self):
        pass
    
    # 비디오정보 : video_info_list 중 일부를 DB에서 관리하는 메소드
    # input None, output None(video_info_list
    def db_manage_monthly_upload(self):
        pass


    
    def start(self):

        print("start crawler...")
        self.channel_id = self.verify_channel_id(self.channel_id)
        print('got channel id : ',self.channel_id)

        ## channel info get sequence
        channel_URL = self.create_channel_URL(self.channel_id)
        channel_json = self.request_channel_URL(channel_URL)
        self.parse_channel_json(channel_json)
        print("channel info :",self.channel_info_list)

        # channel activity get sequence
        activity_URL = self.create_activity_URL(self.channel_id)
        activity_response, next_page_token =self.request_activity_URL(activity_URL)
        self.parse_activity_json(activity_response)
        print("next page: ",next_page_token)
        while True:
            
            if (next_page_token!=None) and (len(self.videos_id_list)<=101) :
                print("next page requesting...")
                print("next page :", next_page_token)
                print("next URL : ",activity_URL)
                temp = activity_URL + "&pageToken=" + next_page_token
                print(temp)
                activity_response, next_page_token =self.request_activity_URL(activity_URL + "&pageToken=" + next_page_token)
                self.parse_activity_json(activity_response)

            else:
                print("page end!")
                break
        

        ## video info get sequence - done
        for i in range(0,len(self.videos_id_list),self._max_result): ## 멕스 리절트 인자만큼 아이디 쿼리 날림
            video_URL = self.create_videos_URL(self.videos_id_list[i:i+self._max_result])#인덱싱해서 URL 따로날림
            video_json = self.request_video_URL(video_URL) #URL request
            self.parse_videos_json(video_json) # 해당하는 갯수만큼 json 발라냄
            
        for video_info in self.video_info_list:
            pass#print(video_info)
        
        ## DB managing

        

           
if __name__ == "__main__":
    channel_id = input()
    crawler = Youtube_Crawler(channel_id)
    crawler.start()
