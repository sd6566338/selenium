#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys,time,urllib.request,os,requests,re,threading
#from tasks import get_download_url
from tasks import *
####
#url = 'https://f7jsg.com/jingpin/play-152720.html'
url = 'https://www.ui2ze.com/shipin/list-%E6%8E%A2%E8%8A%B1%E4%B8%BB%E6%92%AD-{}.html'
videos_url = 'https://www.ui2ze.com/shipin/list-%E6%8E%A2%E8%8A%B1%E4%B8%BB%E6%92%AD.html'
xpath = '//*[@class="form-control input-sm copy_btn"]'
namepath = '//div[@class="box movie_list"]/ul/div/li/a'
picpath = '//div[@class="box movie_list"]/ul/div/li/a/img'
videopath = '//tr[@class="app_hide"]/td/input'
def hide():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-dev-shm-usage')
    return option
def get_video_name(namepath,picpath,url):
    for num in range(1,78):
        print(url.format(num))
        ss = get_download_url.delay(num,namepath,picpath,url)
#get_video_name(namepath,picpath,url)
###get videos_url_dict_all####
def get_video_url_mp4(videopath):
    videos_url_dict_all = {}
    with open("videos_url_dict.txt", "r") as f:
        ss = f.readlines()
        for i in ss:
            videos_url_dict_all.update(eval(i))
        for k,v in videos_url_dict_all.items():
            print(v)
            result = get_video_download_url.delay(k,v,videopath)
get_video_url_mp4(videopath)
#videos_url_dict_all = get_video_info()
#dd = get_video_download_url.delay(videos_url_dict_all,videopath)
def download_video_begin():                                                                                                                     
    with open("videos_download_dict_over.txt", "r") as f:                                                                                                   
        videos_download_dict_over = f.read()                                                                                                                
    with open("video_download_url.txt", "r") as f:                                                                                                          
        result = f.read()
    for k,v in eval(result).items():                                                                                                                  
        if k in videos_download_dict_over:                                                                                                                  
            continue                         
        else:
            download_video.delay(k,v)
