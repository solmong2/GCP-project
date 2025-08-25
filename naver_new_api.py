# 네이버 뉴스 api 예제코드

import os
import sys
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request

client_id = "UjmdUBHZ8D0gqm1nBCBM"
client_secret = "0zRXvkrAR2"

encText = urllib.parse.quote("주가")
url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=100" # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
else:
    print("Error Code:" + rescode)

data = json.loads(response_body.decode('utf-8'))

news_items = data['items']

news_list = []

for item in news_items:
    news_dict = {
        'title': item['title'],  # 제목
        'description': BeautifulSoup(item['description'], 'html.parser').get_text(),  # HTML 제거
        'pubDate': datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z'),  # 날짜 변환
        'link': item['link']  # 링크
    }
    news_list.append(news_dict)

# 확인
print(news_list[0]['description'])

df = pd.DataFrame(news_list)
print(df.head())
df.to_csv('news_data1.csv', index=False, encoding='utf-8-sig')
