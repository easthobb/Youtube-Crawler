import requests
import os
import json
import csv


class Youtube_Crawler(object):

    def __init__(self, channel_name):
        print("Crawler initiating...")

        # Attributes of Crawler
        self.token = "" # temp API key
        self.channel_name = channel_name  # input parameter
        self.channel_id = ""  # convert
        self.channel_playlist_id = ""
        self._max_result = 10  # temp
        self.videos_id_list = []

        # Attributes for channel info crawling
        self.videos_URL_list = []
        self.channel_info_list = []

        # Attributes for videos crawling
        self.video_info_list = []

    @property
    def max_result(self):
        return self._max_result

    @max_result.setter
    def max_result(self, value):
        self._max_result = value

    # 클래스에서 입력받은 채널 네임의 유효성 검사
    # input channel_name, return channel_id or -1
    def verify_channel_name(channel_name):

        print("verify channel name...", channel_name)
        query = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet&forUsername={channel_name}&fields=items(id)&key"
        
        verify = requests.get()
        return

    # channel_id를 이용해 API 요청 위한 URL로 변환
    #
    def create_channel_URL(channel_id):

        # 입력받은 URL 을 요청하는 함수
        #
    def request_channel_URL(URL):

        # 채널 정보에 대해 입력받은 json을 발라내는 함수
        #
    def parse_channel_URL(channel_json):

        # 채널 응답으로 부터 videos_id_list와 URL list를 저장하는 함수
        #
    def set_videos_id_and_URL_list():

        # 채널 정보가 담긴 list를 csv로 변환하는 함수
        #

    def convert_channel_to_csv(channel_info_list):

        # video_id를 종합해 URL 형태로 만드는 함수
        #
    def create_videos_URL():

        # 입력받은 URL을 요청하는 함수
        #
    def request_video_URL():

        # 응답으로 받은 json에서 필요한 정보를 발라내는 함수
    def parse_videos_json(video_json):

        # 응답으로 받은 json에서
    def convert_videos_to_csv(video_info_list):

    def start(self):
        pass

    if __name__ == "__main__":
        channel_name = input()
        crawler = Youtube_Crawler(channel_name)
        crawler.start()
