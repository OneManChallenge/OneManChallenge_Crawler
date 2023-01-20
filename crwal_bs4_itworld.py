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

#6. 기사등록일 [몇일전] 제거용
import datetime

#7. DB 연동
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
    cursor.execute("INSERT INTO news (division, title, content, article_date, img_url, main_url) VALUES (%s, %s, %s, %s, %s, %s);", ('IT월드', news_title, news_content, news_date, news_img_url, news_main_url))
    conn.commit()
    return

conn, cursor = connection_MYSQL()

#크롤링
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def news_crawl(news_id):
    # try:
        target_url = 'https://www.itworld.co.kr'
        url = target_url + '/news/?page=' + str(news_id)

        print(url)
        response = requests.get(url, headers=headers)
        #response = requests.get(url, headers=headers, proxies=proxies) #토르 네트워크 사용 시 주석해제 - 느리지만 추적 어렵게 함(우회), selenium보단 빠름

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        #94라인 if문 전용 날짜 함수
        now = datetime.datetime.now()

        common_selector = '.section-content > .node-list'

        for i in range(1, 19, 1):
            news_exist = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ')')

            if news_exist is None:
                continue

            news_title = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div > div.col > div > h5 > a').text.strip()

            news_content = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div > div.col > div > p.card-text.crop-text-2').text.strip()[:100] + '...'

            try:
                news_img_url = target_url + soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div > div.thumb.me-3.me-lg-4 > a > img')['src'].strip()
            except:
                news_img_url = ''

            news_main_url = target_url + soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div > div.col > div > h5 > a')['href'].strip()

            news_date = soup.select_one(common_selector + ' > div:nth-child(' + str(i) + ') > div > div.col > div > p.card-text.d-flex.align-items-center.justify-content-between > small').text.strip()

            if(news_date[1:2] == '일'):
                time_difference = news_date[0:1]
                news_date = str(now - datetime.timedelta(days=int(time_difference)))[0:19]
            elif(news_date[2:3] == '시'):
                news_date = str(now)[0:19]
            else:
                news_date = date_refine_boannews(news_date)

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
    news_year = temp_news_date[0:4]
    news_month = temp_news_date[5:7]
    news_day = temp_news_date[8:11]

    return news_year + '-' + news_month + '-' + news_day + ' 00:00:00'


if __name__ == '__main__':

    start_time = time.time() #시간 측정

    # 일반 크롤링
    for i in range(3520, 2000, -1):  #1~3528
        news_crawl(i)

    print("--- %s seconds ---" % (time.time() - start_time))