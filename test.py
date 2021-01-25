import sqlite3
import time

def db_manage_channel_info(c_list):

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
            # update channel_info set channel_name = "LAS", subscribe_count=1500, channel_description="TEST" where channel_id = "UCsU-I-vHLiaMfV_ceaYz5rQ";
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



def db_manage_channel_upload(video_info_list):

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
            description = video_info[4]  # 영상설명
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

    except:
        conn.commit()
        conn.close()
        print("error")

def db_manage_channel_monthly_update_videos(video_info_list):
    #월간 테이블 존재 여부 확인 - 원래 계획은 달 단위로 일단은 한 테이블에 적재하는 것으로....
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

     

if __name__ == "__main__":
    # [video_id0,title,channel_id,pub_time,description,views,likes,comments,thumbnail_URL,video_URL]
    channel_info_list = ['UCsU-I-vHLiaMfV_ceaYz5rQ', 'JTBC News', '1500000','관점과 분석이 있는 뉴스, JTBC 뉴스 공식 유튜브 채널입니다. \n\nWelcome to the official JTBC News Channel.\n\nEasy and Fun news channel 15! You will find the faster and more accurate news on JTBC.']
    video_info_list = [['zPFTNSH1Gns', "갸갸갸?", 'UCsU-I-vHLiaMfV_ceaYz5rQ', '2021-01-23T03:00:27Z', 'rirriririririri', '710393', '6424', '4628', 'https://i.ytimg.com/vi/zPFTNSH1Gns/default.jpg', 'https://www.youtube.com/watch?v=zPFTNSH1Gns']]
    db_manage_channel_info(channel_info_list)
    time.sleep(1)
    db_manage_channel_upload(video_info_list)
    time.sleep(2)
    db_manage_channel_monthly_update_videos(video_info_list)
