#!/usr/bin/env python
# coding: utf-8

# # Data extraction project from the divar site
# 
# 

# # Requirements

# In[1]:


pip install -U selenium


# In[2]:


pip install pandas


# In[12]:


pip install pysqlite3 

# only supports Chrome version 102
# # Import the required libraries and modules

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 


# # Residential sales

# In[23]:


url = 'https://divar.ir/s/tehran/buy-residential/' # آدرس صفحه خرید و فروش
s = Service('chromedriver.exe') # The path to your driver

driver = webdriver.Chrome(service = s)
driver.get(url)
driver2 = webdriver.Chrome(service = s)
time.sleep(3)


# # Find Data

# In[24]:


all_items = driver.find_elements(By.XPATH, value = "//a[@class='kt-post-card kt-post-card--outlined kt-post-card--has-chat']")
links = [item.get_attribute('href') for item in all_items]

len(links)


# In[26]:


maxFind = 3 # Number of page Load
data_buy_residential = []
flag = 0
while True:
    try:
        for link in links:
            driver2.get(link)
            time.sleep(1)
            all_items = driver2.find_elements(By.XPATH, value = "//div[@class='post-info']")
            for item in all_items:
                try:
                    price = item.find_element(By.XPATH, value = ".//p[@class='kt-unexpandable-row__value'][1]").text
                except:
                    price = ''

                try:
                    place = item.find_element(By.XPATH, value = ".//div[@class='kt-page-title__subtitle kt-page-title__subtitle--responsive-sized']").text
                except:
                    place = ''      

                try:
                    size = item.find_element(By.XPATH, value = ".//span[@class='kt-group-row-item__value'][1]").text
                except:
                    size = '-1' 

                try:
                    year = item.find_element(By.XPATH, value = ".//span[@class='kt-group-row-item__value'][2]").text
                except:
                    year = '-1' 

                try:
                    room = item.find_element(By.XPATH, value = ".//span[@class='kt-group-row-item__value'][3]").text
                except:
                    room = '-1'    

                data_buy_residential.append([price, place, int(size), int(year), int(room) ])
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight,)")
        time.sleep(3)
        all_items = driver.find_elements(By.XPATH, value = "//a[@class='kt-post-card kt-post-card--outlined kt-post-card--has-chat']")
        links = [item.get_attribute('href') for item in all_items]
        flag += 1
        if flag >= maxFind: break
    except:
        break


# In[27]:


len(data_buy_residential)


# # Residential rent

# In[31]:


url = 'https://divar.ir/s/tehran/rent-residential/' # آدرس صفحه اجاره مسکونی
s = Service('chromedriver.exe') # The path to your driver

driver = webdriver.Chrome(service = s)
driver2 = webdriver.Chrome(service = s)
driver.get(url)
time.sleep(3)


# # Find Data

# In[32]:


all_items = driver.find_elements(By.XPATH, value = "//a[@class='kt-post-card kt-post-card--outlined kt-post-card--has-chat']")
links = [item.get_attribute('href') for item in all_items]

len(links)


# In[33]:


maxFind = 3 # Number of page Load
data_rent_residential = []
flag = 0
while True:
    try:
        for link in links:
            driver2.get(link)
            time.sleep(1)
            all_items = driver2.find_elements(By.XPATH, value = "//div[@class='post-info']")
            for item in all_items:
                try:
                    price = item.find_element(By.XPATH, value = ".//p[@class='kt-unexpandable-row__value'][1]").text
                except:
                    price = ''

                try:
                    place = item.find_element(By.XPATH, value = ".//div[@class='kt-page-title__subtitle kt-page-title__subtitle--responsive-sized']").text
                except:
                    place = ''      

                try:
                    size = item.find_element(By.XPATH, value = ".//span[@class='kt-group-row-item__value'][1]").text
                except:
                    size = '-1' 

                try:
                    year = item.find_element(By.XPATH, value = ".//span[@class='kt-group-row-item__value'][2]").text
                except:
                    year = '-1' 

                try:
                    room = item.find_element(By.XPATH, value = ".//span[@class='kt-group-row-item__value'][3]").text
                except:
                    room = '-1'    

                data_rent_residential.append([price, place, int(size), int(year), int(room) ])
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight,)")
        time.sleep(3)
        all_items = driver.find_elements(By.XPATH, value = "//a[@class='kt-post-card kt-post-card--outlined kt-post-card--has-chat']")
        links = [item.get_attribute('href') for item in all_items]
        flag += 1
        if flag >= maxFind: break
    except:
        break


# In[34]:


len(data_rent_residential)


# # Save Data

# In[29]:


import sqlite3

DBconnect = sqlite3.connect('Database-Divar.db', check_same_thread=False)
c = DBconnect.cursor()


# ## Save rents

# In[35]:


for row in data_rent_residential:
    c.execute("INSERT INTO TblBuyRent VALUES (?,?,?,?,?,?)", (row[0], row[1], row[2], row[3], row[4], 'rent'))
    print(row)
DBconnect.commit()


# ## Save sales

# In[30]:


for row in data_buy_residential:
    c.execute("INSERT INTO TblBuyRent VALUES (?,?,?,?,?,?)", (row[0], row[1], row[2], row[3], row[4], 'buy'))
    print(row)
DBconnect.commit()


# In[ ]:




