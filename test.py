import sqlite3


def db_manage_channel_info(c_list):
    
    channel_id = c_list[0]
    try:
        # DB connect
        conn = sqlite3.connect('crawler.db')
        cur = conn.cursor()
        
        # DB 조회
        cur.execute(f"SELECT channel_id from channel_info;")
        db_list = cur.fetchall()
        channel_id_list = []
        for element in list(map(list,db_list)):
            channel_id_list.append(element[0])

        #cur.execute("INSERT INTO channel_info VALUES(?,?,?,?)",c_list)
        
        conn.commit()
        conn.close()
        print("done")
    except:
        conn.commit()
        conn.close()
        print("error")

    print(channel_id_list)
if __name__ == "__main__":

    channel_info_list=['UCsU-I-vHLiaMfV_ceaYz5rQ', 'JTBC News', '1500000', '관점과 분석이 있는 뉴스, JTBC 뉴스 공식 유튜브 채널입니다. \n\nWelcome to the official JTBC News Channel.\n\nEasy and Fun news channel 15! You will find the faster and more accurate news on JTBC.']
    db_manage_channel_info(channel_info_list)
    