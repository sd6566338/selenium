#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys,time,urllib.request,os,requests,re,threading
from tasks import get_download_url
####
#url = 'https://f7jsg.com/jingpin/play-152720.html'
#url = 'https://f7jsg.com/jingpin/play-151134.html'
#videos_url = 'https://www.c9qjx.com/jingpin/list-%E9%BA%BB%E8%B1%86%E4%B8%93%E5%8C%BA-12.html'
xpath = '//*[@class="form-control input-sm copy_btn"]'
namepath = '//div[@class="box movie_list"]/ul/div/li/a'
videopath = '//tr[@class="app_hide"]/td/input'
#videos_dict = ({'絕對領域掩飾欲望反差妍姐': 'https://www.v2kty.com/jingpin/play-148978.html', '外卖员猥亵美女，强干独自在家的小美女4': 'https://www.v2kty.com/jingpin/play-149350.html', '出差操上清纯同事（徐蕾）': 'https://www.v2kty.com/jingpin/play-149183.html'})
#videos_dict = ({'絕對領域掩飾欲望反差妍姐': 'https://www.v2kty.com/jingpin/play-148978.html'})
#page_date = driver.page_source
def hide():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-dev-shm-usage')
    return option
def get_video_info():
    with open("videos_download_dict_all.txt", "r") as f:
        videos_dict = f.read()
    return videos_dict
def download_video(video_download_url):
    with open("videos_download_dict_over.txt", "r") as f:
        videos_download_dict_over = f.read()
        print(videos_download_dict_over)
    for k,v in video_download_url.items():
        if k in videos_download_dict_over:
            continue
        else:
            #下载文件，下载成功以后将Key写入"videos_download_dict_over.txt"
            print(k+"is--downloading--")
            with open("videos_download_dict_begin.txt", "w") as f:
                name = f.write(k+".mp4")
            urllib.request.urlretrieve(v,k+".mp4")
            with open("videos_download_dict_over.txt", "a") as f:
                f.writelines(k+".mp4")
                f.writelines("\n")
                print(k+"is over")
#            video_download_url.pop(k)
def get_video_download_url(videos_dict):
    videos_dict = eval(videos_dict)
    for video_name,video_url in videos_dict.items():
        print(video_name+":"+video_url)
        ss = get_download_url.delay(xpath,video_name,video_url)
        print(ss.ready())

#get_video_download_url(videos_dict)
def download_contrl(namepath,xpath):
    with open("videos_download_dict.txt", "r") as f:
        res = f.readlines()
        if res:
            video_download_url={}
            for i in res:
                video_download_url.update(eval(i))
            print(video_download_url)
            print(type(video_download_url))
            download_video(video_download_url)
    #如果下载字典为空，则重新获取下载字典：    
        else:
            print("--get video_download_urls--")
            ##获取video专辑url
            #videos_dict = get_video_info()
            get_video_info()
            ##获取video下载url
            video_download_url = get_video_download_url(videos_dict)
            if video_download_url:
                with open("videos_download_dict.txt", "w") as f:
                    f.write(str(video_download_url).replace(" ",""))
                download_video(video_download_url)
download_contrl(namepath,xpath)
print('------over------')
