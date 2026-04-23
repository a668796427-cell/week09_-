import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from datetime import datetime
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 初始化 (保持你原有的邏輯)
if os.path.exists('serviceAccountKey.json'):
    cred = credentials.Certificate('serviceAccountKey.json')
else:
    firebase_config = os.getenv('FIREBASE_CONFIG')
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def index():
    # 首頁標題已改為你的名字，並加入電影查詢超連結
    link = "<h1>歡迎進入翁瑋聖的網站20260409</h1>"
    link += "<a href='/movie1'>[查詢即將上映電影]</a><hr>" 
    link += "<a href='/mis'>課程</a><hr>"
    link += "<a href='/today'>現在日期時間</a><hr>"
    link += "<a href='/me'>關於我</a><hr>"
    link += "<a href='/read'>讀取Firestore資料</a><hr>"
    return link

@app.route("/movie1")
def movie1():
    R = "<h2>即將上映電影清單 (開眼電影網)</h2>"
    url = "https://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    
    # 抓取電影名稱、超連結與海報
    result = sp.select(".filmListAllX li")
    for item in result:
        try:
            name = item.find("img").get("alt")
            introduce = "https://www.atmovies.com.tw" + item.find("a").get("href")
            post = "https://www.atmovies.com.tw" + item.find("img").get("src")
            
            # 組合 HTML 顯示
            R += f'<a href="{introduce}" target="_blank">{name}</a><br>'
            R += f'<img src="{post}" width="160"><br><br>'
        except:
            continue
            
    R += "<br><a href='/'>返回首頁</a>"
    return R

# ... 保留原本的 /mis, /today, /read 等路由 ...

if __name__ == "__main__":
    app.run(debug=True)