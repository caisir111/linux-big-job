#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
import json
import sys

# import time
# from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, QTimer
# from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit
# from PyQt5.QtGui import QTextCursor


#def num_to(num):
#    numbers = {
#       0:get_url(uid,page,select_content),
#        1:sys.exit{0}
#}

def get_url(uid,page,select_content): 
    dynamic_id = '0'
#动态识别码以及uid

    for b in range(page):
        print('=============================正在进行第{}页爬取============================='.format(b+1))
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=1&host_uid={}&offset_dynamic_id={}&need_top=1&platform=web'.format(uid,dynamic_id)
#offest_dynamic_id为页id
#反爬机制，UA伪装
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        res = requests.get(url,headers=headers)
#发送连接请求
        res_json = json.loads(res.text)
#调用json库的loads方法，将其转化为python类对象
        dynamic_id = res_json['data']['cards'][11]['desc']['dynamic_id']

        select_pictures(res_json,select_content)

def select_pictures(res_json,select_content):
    long_1 = len(res_json['data']['cards'])
    for a in range(long_1):
        description = res_json['data']['cards'][a]['card']
        description_json = json.loads(description)
        #剔除无关广告动态，需每一条正常/广告动态有一样的关键词
        if select_content == 0:
            try:
                #调用保存图片的函数
                save_pictures(res_json,a)
            except:
                continue
        else:

            try:
                advert_judge = description_json['item']['description'].find(select_content) #找到关键词返回0，否则返回-1
            except:
                advert_judge = -2

            print(advert_judge)
            if advert_judge == 0 or advert_judge == 0: #关键词是广告帖则填入0，反之填入-1和-2
                continue
            else:
                try:
                    save_pictures(res_json, a)
                except:
                    continue
def save_pictures(res_json,a):

    card = res_json['data']['cards'][a]['card'].replace('\\', '')

    card_json = json.loads(card)

    long = len(card_json['item']['pictures'])

    img_url = []
    for i in range(long):
        img_url.append(card_json['item']['pictures'][i]['img_src'])
        #append添加新的字符串
        print(img_url[i])
        r = requests.get(img_url[i])
        name = img_url[i].split('album/')[1]
        #识别到album进行分割
        with open("/home/13536845956/pachong4/{}".format(name), "wb")as f:  
#本地地址
            f.write(r.content)
            f.close()

if __name__ == '__main__':

    print('\n             *******************************************************');
    print('\n             *                                                     *');
    print('\n             *               B站"动态"图片爬虫助手                 *');
    print('\n             *                                                     *');
    print('\n             *******************************************************');
    uid = input('请输入爬取uid:\n')
    page = int(input('请输入爬取的动态页数(一页12条，会自动剔除无图动态)：\n'))

    select = input('是否进行关键词剔除，Y/N?')
    if select == 'Y':
        select_content = input('请输入剔除广告的关键词：\n')
    else:
        select_content = 0
    get_url(uid,page,select_content)
    select = input('是否继续，Y/N?')
    if select == 'Y':
        uid = input('请输入爬取的uid：\n')
        page = int(input('请输入爬取的动态页数(一页12条，会自动剔除无图动态):\n'))
        select = input('是否进行关键词剔除，Y/N?')
        if select == 'Y':
            select_content = input('请输入剔除广告的关键词：\n')
        else:
            select_content = 0

        get_url(uid,page,select_content)
    
#    get_url(uid,page,select_content)
