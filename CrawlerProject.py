#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen 
import pymongo as pm
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['RawData']
collection = db['House']

url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=1&searchtype=1&region=1&section=5&firstRow={}&totalRows=571'
headers = {
   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' 
}
house_ary = []
for i in range(0,2):
    res = requests.get(url.format(i*30),headers = headers)
    jd = res.json()
    df = pd.DataFrame(jd['data']['data'])
    house_ary.append(df)
df = pd.concat(house_ary)


# In[35]:


extractdf = df[['houseid','condition','linkman','nick_name']]
extractdf.head()


# In[55]:


for index, row in extractdf.iterrows():
    lessor = str(row['linkman'])
    lastname = lessor[0]
    #print(lessor)
    lessor_gender = 0
    if '小姐' in lessor:
        lessor_gender = 1
    elif '先生' in lessor:
        lessor_gender = 2
    #print(lessor_gender)
    lessor_type = str(row['nick_name'])[0:2]
    gender = str(row['condition'])
    gender_rtn = 0
    if 'girl' in gender:
        gender_rtn = 1
    elif 'boy' in gender:
        gender_rtn = 2
    req = Request('https://rent.591.com.tw/rent-detail-'+str(row['houseid'])+'.html')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    webpage = urlopen(req)
    soup = BeautifulSoup(webpage,'html.parser')
    phone = soup.find('span',{'class':'dialPhoneNum'})
    phone_num = str(phone['data-value']).replace('-','')
    house =soup.find('ul',{'class':'attr'})
    h_li_arr = house.find_all('li')
    house_type = ''
    house_status = ''
    for li in h_li_arr:
        if '型態' in str(li.string):
            house_type = str(li.string).replace('\xa0','').replace('型態:','')
        if '現況' in str(li.string):
            house_status = str(li.string).replace('\xa0','').replace('現況:','')

    print(insert_db(lastname,lessor_gender,lessor_type,gender_rtn,phone_num,house_type,house_status))


# In[54]:


def insert_db(lastname,lessor_gender,lessor_type,gender_rtn,phone_num,house_type,house_status):
    post = {"lastname": lastname,
            "lessor_gender": lessor_gender,
            "lessor_type": lessor_type,
            "gender_rtn" : gender_rtn,
            "phone_num" : phone_num,
            "house_type": house_type,
            "house_status" : house_status,
            "update_date": datetime.datetime.utcnow()}
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    return post_id
    
    


# In[ ]:




