#1. 크롤링
import cursor as cursor
import requests
from bs4 import BeautifulSoup

#2. 멀티프로세싱
# import multiprocessing as mp
# from multiprocessing import Pool

#3. 시간 측정
import time

#4. 랜덤 숫자
import random

#5 https 웹사이트 보안경고 해제
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#6. DB 연동
import json
import pymysql
import logging
import sys

with open('config.json', 'r') as f:
    config = json.loads(f.read())

def connection_MYSQL():
    host = config['MYSQL']['HOST']
    database = config['MYSQL']['SCHEMA']
    port = 3306
    username = config['MYSQL']['USERNAME']
    password = config['MYSQL']['PASSWORD']

    try:
        conn = pymysql.connect(host=host, user=username, password=password, db=database, port=port, use_unicode=True, charset='utf8mb4')
        cursor = conn.cursor()
    except:
        logging.error('MySQL 연결 실패')
        sys.exit(1)
    return conn, cursor

def insert_MYSQL(news_title, news_content, news_date, news_img_url, news_main_url, conn, cursor):
    cursor.execute("INSERT INTO news (division, title, content, article_date, img_url, main_url) VALUES (%s, %s, %s, %s, %s, %s);", ('보안뉴스', news_title, news_content, news_date, news_img_url, news_main_url))
    conn.commit()
    return

conn, cursor = connection_MYSQL()

#크롤링
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def news_crawl(news_id):
    # try:
        target_url = 'https://www.boannews.com'
        url = target_url + '/media/t_list.asp?Page=' + str(news_id)

        print(url)
        response = requests.get(url, headers=headers, verify=False)
        #response = requests.get(url, headers=headers, proxies=proxies) #토르 네트워크 사용 시 주석해제 - 느리지만 추적 어렵게 함(우회), selenium보단 빠름

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        for i in range(1, 41, 2):
            news_exist = soup.select_one('#news_area > div:nth-child(' + str(i) + ')')

            if news_exist is None:
                continue

            try:
                news_img_url = target_url + soup.select_one('#news_area > div.news_list:nth-child(' + str(i) + ') > a:nth-child(1) > img')['src'].strip()
            except:
                news_img_url = ''

            news_main_url = target_url + soup.select_one('#news_area > div.news_list:nth-child(' + str(i) + ') > a.news_content')['href'].strip()

            news_content = soup.select_one('#news_area > div.news_list:nth-child(' + str(i) + ') > a.news_content').text.strip()

            try:
                news_title = soup.select_one('#news_area > div.news_list:nth-child(' + str(i) + ') > a:nth-child(1) > span.news_txt').text.strip()
            except:
                news_title = news_content[0:20] + '...'

            try:
                news_date = date_refine_boannews(soup.select_one('#news_area > div.news_list:nth-child(' + str(i) + ') > span').text.strip()[-19:])
            except:
                continue

            global conn
            global cursor

            insert_MYSQL(news_title, news_content, news_date, news_img_url, news_main_url, conn, cursor)

    # except Exception as e:
    #     print(e)
    #     print('=====================================')
    #     print('크롤링 에러 page ' + str(news_id) + " ")
    #     print('=====================================')
    #     return

        rand_value = random.randint(0, 3)
        time.sleep(rand_value)

# 날짜 정제 - 보안뉴스
def date_refine_boannews(temp_news_date):
    news_year = temp_news_date[-19:-15]
    news_month = temp_news_date[-13:-11]
    news_day = temp_news_date[-9:-7]
    news_time = temp_news_date[-5:]

    return news_year + '-' + news_month + '-' + news_day + ' ' + news_time + ':00'


if __name__ == '__main__':

    start_time = time.time() #시간 측정

    # 일반 크롤링
    for i in range(5000, 5236):  #2~5235  500~1000 해야됨
        news_crawl(i)

    # Multiprocessing 병렬 크롤링
    # print("<<<<< 사용가능 프로세스 개수 : " + str(mp.cpu_count()) + " >>>>>")
    # start = 1
    # end = 10000
    # for song_id in range(start, end):
    #     melon_crawl(song_id)
    #     if song_id % 500 == 0:3
    #         print("--- %s seconds ---" % (time.time() - start_time))
    #         time.sleep(random.uniform(0, 2))
    #         start_time = time.time()
        # print("--- %s seconds ---" % (time.time() - start_time))

    # with Pool(processes=mp.cpu_count()) as pool:  #병렬 처리 프로세스 개수 설정 : processes=갯수
    #     pool.map(melon_crawl, range(start, end)) #크롤링 범위 설정 : range(시작번호, 종료번호)
    # #
    print("--- %s seconds ---" % (time.time() - start_time))