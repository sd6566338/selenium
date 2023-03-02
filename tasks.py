#!/usr/bin/python3
from celery import Celery
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#app = Celery('tasks', backend='redis://:@127.0.0.1:6379/0', broker='amqp://user:password@localhost:5672/myvhost')
app = Celery('tasks', backend = 'redis://127.0.0.1:6379/3',broker = 'redis://127.0.0.1:6379/4')

def hide():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-dev-shm-usage')
    return option
@app.task
def get_download_url(num,namepath,picpath,url):
    driver = webdriver.Chrome(options=hide())
    driver.get(url.format(num))
    ss = driver.find_elements(by=By.XPATH, value=namepath)
    pic = driver.find_elements(by=By.XPATH, value=picpath)
    video_name = []
    video_download_url = []
    video_pic = []
    for i in pic:
        video_pic.append(i.get_attribute('src'))
    for i in ss:
        video_name.append(i.get_attribute('title').replace(" ",""))
        video_download_url.append(i.get_attribute('href'))
    videos_download_dict = dict(zip(video_name,video_download_url))
    videos_pic_dict = dict(zip(video_name,video_pic))
    print(videos_download_dict)
    print(videos_pic_dict)
   # os.mkdir("videos_pic_dict{}.txt".format(num))
   # file = open('videos_pic_dict{}.txt'.format(num),'w')
   # file.close()
    with open("videos_pic_dict.txt", "a") as f:
        f.write(str(videos_pic_dict))
        f.write("\n")
   # os.mkdir("videos_url_dict{}.txt".format(num))
    #file = open('videos_url_dict{}.txt'.format(num),'w')
    #file.close()
    with open("videos_url_dict.txt", "a") as f:
        f.write(str(videos_download_dict))
        f.write("\n")
    driver.close()
@app.task
def get_video_download_url(k,v,videopath):
    d1 = {}
    driver = webdriver.Chrome(options=hide())
    driver.get(v)
    try:
        result = driver.find_elements(by=By.XPATH,value=videopath)
        d1[k] = result[0].get_attribute('value')
        driver.close()
        driver.quit()
        with open('video_download_url.txt','a')as f:
            f.write(str(d1))
            f.write('\n')
    except Exception as e:
        return e
