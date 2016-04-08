#coding:utf-8
#File: main.py
#Auth: lixp(@500wan.com)
#Date: 2015-12-21 09:38:48
#Desc: 

import os
import sys
from PIL import Image,ImageDraw,ImageEnhance
import requests
from lib.ocr import remove_noise 
from lib.ocr import pytesser 
from lib import crawler

task_list = []
leftmoney = 0  #余额

#任务列表
#Task:【优先级x的任务:彩种xxx购买y包】{'priority':x,'name':'yyy','num':z}
def deal_task():
    global task_list
    global leftmoney
    if not task_list: return
    #优先级排序
    task_list = sorted(task_list, key=lambda task_list : task_list.get('priority',0)) 
    #订单购买
    for task in task_list:
        for lottery in lottery_list:
            if task.get('name','') == lottery.get('name'):
                leftpack = lottery.get('num')
                packnum  = lottery.get('package')
                price    = lottery.get('price')
                package = task.get('num',0)
                #库存不足
                if leftpack < package:
                    needmoney = packnum*price*leftpack
                    #余额不足
                    if needmoney > leftmoney:
                        postpack = leftmoney/(packnum*price)
                    else:
                        postpack = leftpack

                else:
                    needmoney = packnum*price*package
                    if needmoney > leftmoney:
                        postpack = leftmoney/(packnum*price)
                    else:
                        postpack = package 
                leftmoney = leftmoney - packnum*price*postpack 

                #提交订单
                do_commit(lottery,postpack)
                task['num'] -= postpack
            else:
                pass
    #过滤掉已完成的任务
    task_list = [task for task in task_list if task.get('num',0) > 0]
    

def ocr_appendcode():
    #图片去噪点
    image = Image.open("./data/token.jpg")
    image = image.convert("L")
    remove_noise.clearNoise(image,127,2,1)

    #ocr识别
    enhancer = ImageEnhance.Contrast(image)
    image_enhancer = enhancer.enhance(4)
    text = pytesser.image_to_string(image_enhancer)
    return filter(str.isdigit, text)
    
if __name__ == '__main__':
    #首页安装cookie-handler
    crawler.install_cookiehandler()

    #获取动态验证码
    #有可能不是4位，需容错
    crawler.get_appendcode_img()
    appendCode = ocr_appendcode() 

    #发起登录获取cookie
    crawler.do_login(appendCode)

    #抓取订单参数
    params = crawler.get_form_params()

    #发起购买订单
    lottery = {'product_ID':115,
               'name':'麻辣6'.decode('utf-8').encode('gbk'),
               'unit':'包'.decode('utf-8').encode('gbk'),
               'packnum':120,
               'price':5}
    #print crawler.do_commit(params, lottery, 1)
