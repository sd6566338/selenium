#!/usr/bin/python3
from celery import Celery
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#app = Celery('tasks', backend='redis://:@127.0.0.1:6379/0', broker='amqp://user:password@localhost:5672/myvhost')
app = Celery('get_video_download_url', backend = 'redis://127.0.0.1:6379/3',broker = 'redis://127.0.0.1:6379/4')

def hide():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-dev-shm-usage')
    return option
#@app.task
#def add(x, y):
#    return x + y
#res = add.delay(3,4)
#time.sleep(2)
#
#print(res.result)
#print(res.ready())
#video_download_url = {}
@app.task
def get_video_download_url(videos_url_dict_all,videopath):
    video_name = []
    video_download_url = []
    for k,v in videos_url_dict_all.items():
        video_name.append(k)
        driver = webdriver.Chrome(options=hide())
        driver.get(v)
        ss = driver.find_elements(by=By.XPATH, value=videopath)
        video_download_url.append(ss[0].get_attribute('value'))
        videos_dict = dict(zip(video_name,video_download_url))
        # ~E~W~S~I~M~W~O
        driver.close()
        # ~E~W~S~I~M~Z~]
        driver.quit()
    with open("video_download_url.txt", "w") as f:
        f.write(videos_dict)
    return videos_dict

@app.task
def download_video(video_download_url):
    with open("videos_download_dict_over.txt", "r") as f:
        videos_download_dict_over = f.read()
    with open("video_download_url.txt", "r") as f:
        video_download_url = eval(f.read())
    for k,v in video_download_url.items():
        if k in videos_download_dict_over:
            continue
        else:
            print(k+"is--downloading--")
            with open("videos_download_dict_begin.txt", "w") as f:
                name = f.write(k+".mp4")
            urllib.request.urlretrieve(v,".{}/{}.mp4".format(k,k))
            with open("videos_download_dict_over.txt", "a") as f:
                f.writelines(k+".mp4")
                f.writelines("\n")
                print(k+"is over")
