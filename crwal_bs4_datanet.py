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
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    cursor.execute("INSERT INTO news (division, title, content, article_date, img_url, main_url) VALUES (%s, %s, %s, %s, %s, %s);", ('데이터넷', news_title, news_content, news_date, news_img_url, news_main_url))
    conn.commit()
    return

conn, cursor = connection_MYSQL()

#크롤링
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def news_crawl(news_id):
        if(news_id%100 == 0):
            rand_value = random.randint(0, 5)
            time.sleep(rand_value)

        # try:
        target_url = 'https://www.datanet.co.kr'
        url = target_url + '/news/articleList.html?page=' + str(news_id) + '&view_type=sm'

        print(url)
        response = requests.get(url, headers=headers)
        #response = requests.get(url, headers=headers, proxies=proxies) #토르 네트워크 사용 시 주석해제 - 느리지만 추적 어렵게 함(우회), selenium보단 빠름

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        common_selector = '#user-container > div.float-center.max-width-1080 > div.user-content > section > article > div.article-list > section'

        for i in range(1, 21, 1):
            news_exist = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ')')

            if news_exist is None:
                continue

            news_title = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div.list-titles > a > strong').text.strip()

            news_content = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > p > a').text.strip()[:200] + '...'

            try:
                news_img_url = target_url + '/news' + soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div.list-image')['style'].strip()[22:-1]
            except:
                news_img_url = ''

            news_main_url = target_url + soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div.list-titles > a')['href'].strip()

            temp_news_date = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div.list-dated').text.strip()
            news_date = date_refine_boannews(temp_news_date)

            global conn
            global cursor

            insert_MYSQL(news_title, news_content, news_date, news_img_url, news_main_url, conn, cursor)

    # except Exception as e:
    #     print(e)
    #     print('=====================================')
    #     print('크롤링 에러 page ' + str(news_id) + " ")
    #     print('=====================================')
    #     return

        rand_value = random.randint(0, 5)
        time.sleep(rand_value)

# 날짜 정제 - 데이터넷
def date_refine_boannews(temp_news_date):
    return temp_news_date[-16:] + ':00'


if __name__ == '__main__':

    start_time = time.time() #시간 측정

    # 일반 크롤링
    for i in range(7207, 7694):  #1~7693
        news_crawl(i)

    print("--- %s seconds ---" % (time.time() - start_time))