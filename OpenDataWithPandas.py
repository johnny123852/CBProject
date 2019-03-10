#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
pd.__version__


# In[8]:


myCSV_a = pd.read_csv('C:\\Users\\Johnny Hsiao\\Desktop\\a_lvr_land_a.csv')
myCSV_b = pd.read_csv('C:\\Users\\Johnny Hsiao\\Desktop\\b_lvr_land_a.csv')
myCSV_e = pd.read_csv('C:\\Users\\Johnny Hsiao\\Desktop\\e_lvr_land_a.csv')
myCSV_f = pd.read_csv('C:\\Users\\Johnny Hsiao\\Desktop\\f_lvr_land_a.csv')
myCSV_h = pd.read_csv('C:\\Users\\Johnny Hsiao\\Desktop\\h_lvr_land_a.csv')
df_a = pd.DataFrame(myCSV_a)
df_b = pd.DataFrame(myCSV_b)
df_e = pd.DataFrame(myCSV_e)
df_f = pd.DataFrame(myCSV_f)
df_h = pd.DataFrame(myCSV_h)


# In[21]:


df_all = pd.concat([df_a,df_b,df_e,df_f,df_h])
df_all = df_all.fillna(0)
df_all


# In[28]:


def strToNum(strNum):
    num = 0
    if not strNum:
        return num
    if strNum==0:
        return num
    strNum = strNum.replace('層','')
    switcher = {
        '一':'1',
        '二':'2',
        '三':'3',
        '四':'4',
        '五':'5',
        '六':'6',
        '七':'7',
        '八':'8',
        '九':'9',
        '十':'10'
    }
    numStr ='0' 
    for strs in strNum:
        numStr += switcher.get(strs,'')
    num = int(numStr)
    return num

strFloor = ('')
numFloor = strToNum(strFloor)
print(numFloor)


# In[29]:


floor = []
for i in df_all['總樓層數']:
    temp = strToNum(i)
    floor.append(temp)
myFloor = pd.Series(floor)
df_all.insert(12,column='總樓層數Int',value=myFloor)


# In[30]:


df_all


# In[31]:


filter_a_1 = (df_all['主要用途'] == '住家用')
filter_a_2 = (df_all['建物型態'].str.startswith('住宅大樓') )
filter_a_3 = (df_all['總樓層數Int']>102)
filter_a = df_all[filter_a_1 & filter_a_2 & filter_a_3]
filter_a


# In[32]:


filter_a.to_csv('C:\\Users\\Johnny Hsiao\\Desktop\\filter_a.csv')


# In[35]:


totalCount = len(df_all)


# In[52]:


splitCar = df_all['交易筆棟數'].str.split('車位',n=1,expand = True)
df_all['車位'] = splitCar[1]


# In[58]:


totalCarNum = 0
for num in df_all['車位']:
    totalCarNum += int(num)
totalCarNum


# In[60]:


totalPrice = 0
for num in df_all['總價元']:
    totalPrice += int(num)
avgPrice = totalPrice/totalCount
avgPrice


# In[61]:


totalCarPrice = 0
for num in df_all['車位總價元']:
    totalCarPrice += int(num)
avgCarPrice = totalCarPrice/totalCarNum
avgCarPrice


# In[65]:


filterB = {'總件數':[totalCount],
           '總車位數':[totalCarNum],
           '平均總價元':[avgPrice],
           '平均車位總價元':[avgCarPrice]}
filter_b = pd.DataFrame(filterB)
filter_b.to_csv('C:\\Users\\Johnny Hsiao\\Desktop\\filter_b.csv')


# In[ ]:




