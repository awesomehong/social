from bs4 import BeautifulSoup
import requests
import re
import sys
import pprint

comment_list = []

article_url = "https://www.edaily.co.kr/news/read?newsId=01184086632295792&mediaCodeNo=257&OutLnkChk=Y"

oid = article_url.split("oid=")[1].split("&")[0]
aid = article_url.split("aid=")[1]
page = 1
header = {
    "User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.3 (KHTML, like Gecko) Chrome/65.0.325.181 Safari/537.36", "referer": article_url,
}

while True :
    comment_url = "https://www.edaily.co.kr/news/read?newsId=01184086632295792&mediaCodeNo=257&OutLnkChk=Y"
    oid +