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
        self.token = "" # temp API key
        self.channel_name = ""
        self.channel_id = channel_id  # input parameter
        self._max_result = 10  # temp

        # Attributes for channel info crawling
        
        self.channel_info_list = [] #[channel_name, channel_description, channel_subscriberCount]

        # Attributes for Activity info Crawling
        self.videos_id_list = []
        self.videos_URL_list = []


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
        URL = URL + f"&fields=items(snippet.title,snippet.description,statistics.subscriberCount)"
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
            self.channel_info_list.append(response['items'][0]['snippet']['title'])
            self.channel_info_list.append(response['items'][0]['snippet']['description'])
            if 'subscriberCount' in response['items'][0]['statistics']: # in case of NULL Count
                self.channel_info_list.append(response['items'][0]['statistics']['subscriberCount'])
            else:
                self.channel_info_list.append("0")
            print(response)
            print(self.channel_info_list)
        else:
            print('wrong response')


    #activities?part=snippet,contentDetails&channelId=UCsU-I-vHLiaMfV_ceaYz5rQ&maxResults=5&pageToken=CAUQAA
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
        



    # 채널 정보가 담긴 list를 csv로 변환하는 함수
    def convert_channel_to_csv(self,channel_info_list,video_id_list):
        pass

    # video_id를 종합해 URL 형태로 만드는 함수
    #
    def create_videos_URL(self):
        pass


    # 입력받은 URL을 요청하는 함수
    #
    def request_video_URL(self):
        pass



    # 응답으로 받은 json에서 필요한 정보를 발라내는 함수
    def parse_videos_json(self,video_json):
        pass



    # 응답으로 받은 json에서
    def convert_videos_to_csv(self,video_info_list):
        pass

    
    def start(self):

        print("start crawler...")
        self.channel_id = self.verify_channel_id(self.channel_id)
        print('got channel id : ',self.channel_id)

        ## channel info get sequence
        channel_URL = self.create_channel_URL(self.channel_id)
        channel_json = self.request_channel_URL(channel_URL)
        self.parse_channel_json(channel_json)

        # channel activity get sequence
        activity_URL = self.create_activity_URL(self.channel_id)
        activity_response, next_page_token =self.request_activity_URL(activity_URL)
        self.parse_activity_json(activity_response)
        print("next page: ",next_page_token)
        while True:
            if (next_page_token!=None) and (len(self.videos_id_list)<=100) :
                print("next page requesting...")
                activity_URL =activity_URL+ "&nextPageToken=" + next_page_token

            else:
                break

        print(activity_URL)

        
        
        
if __name__ == "__main__":
    channel_id = input()
    crawler = Youtube_Crawler(channel_id)
    crawler.start()
