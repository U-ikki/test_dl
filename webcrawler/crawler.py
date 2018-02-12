# -*- coding: utf-8 -*-

# Create URL for google image search.

from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os
import http.cookiejar
import json

#------------
# get_soup
#------------
#
# BeautifulSoup を使用して、html をパースし、以下のような構造でsoupに格納される
#
# print soup.prettify()
# <html>
#  <head>
#   <title>
#    Page title
#   </title>
#  </head>
#  <body>
#   <p id="firstpara" align="center">
#    This is paragraph
#    <b>
#     one
#    </b>
#    .
#   </p>
#   <p id="secondpara" align="blah">
#    This is paragraph
#    <b>
#     two
#    </b>
#    .
#   </p>
#  </body>
# </html>
#----------------------------
#
# 以下のように、必要な要素を取り出せる。
# 
# print(soup.title)
# <title>Page title</title>
#
# print(soup.title.string)
# Page title
#

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')


#---------
# main
#---------

query = "Yokoyama yui"  # target key word
label="0"

# 入力された query のフォーマットを画像検索のURLに変換する
query= query.split()    # "aaa","bbb", ... のフォーマットに変更
query='+'.join(query)   # 画像検索に合わせたフォーマットに変更
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
DIR="/tmp/img" # imageファイルの格納先

# クローリングする際にどのブラウザとしてアクセスするかという情報。
# これがないと、画像検索が拒否される。
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print  ("there are total" , len(ActualImages),"images")


# image file を保存する親ディレクトリを作成
if not os.path.exists(DIR):
            os.mkdir(DIR)

# 引数で与えられた文字列を path としてつなげる
# >>> os.path.join('/test', 'hoge', 'huge')
# '/test/hoge/huge'

# split の引数に何も指定しない場合、スペースやタブ等で自動的に区切る
DIR = os.path.join(DIR, query.split()[0]) 

# image file を格納する子ディレクトリ（検索キーワードの1つ目要素を使用）を作成
if not os.path.exists(DIR):
            os.mkdir(DIR)

# print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib.request.Request(img, headers=header)
        raw_img = urllib.request.urlopen(req).read()
        cntr = len([i for i in os.listdir(DIR) if label in i]) + 1
        print (cntr)
        if len(Type)==0:
            f = open(os.path.join(DIR , label + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , label + "_"+ str(cntr)+"."+Type), 'wb')
        f.write(raw_img)
        print(type(raw_img))
        f.close()
    except Exception as e:
        print ("could not load : "+img)
        print (e)



