#coding:utf-8
#File: crawler.py
#Auth: lixp(@500wan.com)
#Date: 2016-01-05 17:54:57
#Desc: 

import urllib
import urllib2                                
import random
import cookielib
from bs4 import BeautifulSoup

#首页安装cookie-handler
def install_cookiehandler():
    url = 'http://www.ticaihui.com/'
    c = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)

#获取验证码图片
def get_appendcode_img():
    url = 'http://www.ticaihui.com/platform/sysadmin/login/login.dox?operate=displayAppendCode&randomNum='+str(random.random())
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    html = page.read()
    f = open(r'./data/token.jpg','wb')
    f.write(html)
    f.close()

#发起登录获取cookie
def do_login(appendCode):
    url  = "http://www.ticaihui.com/platform/sysadmin/login/login.dox"
    data = {"loginID":"4402026029",
            "password":"151041",
            "appendCode":appendCode,
        "operate":"loginClientByIVTNoWithAjax"}
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    req.add_header("User-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
    req.add_header("Content-Type","application/x-www-form-urlencoded; charset=UTF-8")
    req.add_header("Host","www.ticaihui.com")
    req.add_header("Origin","http://www.ticaihui.com")
    req.add_header("Referer","http://www.ticaihui.com/")
    resp = urllib2.urlopen(req)

#抓取订单参数
def get_form_params():
    url = 'http://www.ticaihui.com/application/LandlordServices/LandlordServices/add_YDOrder.jsp?IPaddr=&macaddr='
    req = urllib2.Request(url)
    req.add_header("User-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
    req.add_header("Host","www.ticaihui.com")
    req.add_header("Upgrade-Insecure-Requests","1")
    page = urllib2.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html,'lxml',from_encoding='gbk')
    forms= soup.find('form').find('table').find_all('input')
    params = {}
    for p in forms:
        params.update({p["name"]:p["value"].encode('gbk')}) 
    return params

#发起购买订单
def do_commit(params,lottery, postpack):
    """
        *仅支持单一彩种定单
        @params: 系统分配的订单参数
        @lottery: 要订购的彩种信息
        @postpack: 订购数量(包)
    """
    url = 'http://www.ticaihui.com/application/LandlordServices/LandlordServices/saveAddOrder.jsp?command=save'
    #订单总金额
    params['ENTIREAMOUNT'] = int(postpack)*int(lottery['packnum'])*int(lottery['price'])
    #订单总包数
    params['ENTIRENUM'] = postpack 
    #单一彩种订单信息
    params.update({'strProductsName':lottery.get('name'),
                   'strNum':postpack,
                   'strSort':lottery.get('unit'),
                   'strNorm':lottery.get('packnum'),
                   'strUnit':lottery.get('price'),
                   'strshul':0.00,
                   'product_ID':lottery['product_ID'],
                   'productsnum':postpack,
                   'totalprice':0.00})
    req = urllib2.Request(url)
    params = urllib.urlencode(params)
    resp = urllib2.urlopen(req,params)
    return resp.read()

#抓取在售彩种库存情况
def lottery_carwler():
    url = 'http://www.ticaihui.com/application/LandlordServices/LandlordServices/selectLottery.jsp?productcategory=3'
    page = urllib2.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html,'lxml',from_encoding='gbk')
    lottery_list = []
    for tb in soup.find_all('table')[2:3]: #第三个table
        for tr in tb.find_all('tr')[1:]:#过滤第一个tr
            tds = tr.find_all('td')
            id = tds[1].contents[0].encode('utf-8')
            product_ID = tds[1].find('input')['value']
            name = tds[2].contents[0].encode('utf-8')
            unit = tds[3].contents[0].encode('utf-8')
            package = int(tds[4].contents[0].encode('utf-8'))
            price = int(tds[5].contents[0].encode('utf-8'))
            num = int(tds[6].contents[0].encode('utf-8'))
            lottery_list.append({'id':id,
                                 'product_ID':product_ID,
                                 'name':name,
                                 'unit':unit,
                                 'package':package,
                                 'price':price,
                                 'num':num})
    return lottery_list

if __name__ == '__main__':
    lst =  lottery_carwler()
    for l in lst:
        res=[]
	for k,v in l.iteritems():
            res.append(k+":"+str(v))
        print ' '.join(res)

"""
[订单列表]:
彩票编码    彩票名称    数量    单位    包装数量    单价
316         小蛋糕      2       包      150         2 
213         采蘑菇      1       包      120         5    

[抓包数据]:
docID:780156
SERIALNUMBER:545
ENTIRENUM:3                              #订单总包数
SINGLESYSTEMDATE:2016-01-06 01:22:47
mobile:18118782328
website:(unable to decode value)
car_ID:1
DOCCODING:DD1601060545
ENTIREAMOUNT:1200                        #订单总金额
DOCSTATUS:0
CUSTOMERS:(unable to decode value)
CUSTOMERSID:26029
IVTCODING:4402026029
WAREHOUSE:3
OCCURREDDATE:2016-01-06
REMARK:
product_ID:554                          #小蛋糕数据           
productsnum:2                          
totalprice:0.00
strProductsName:(unable to decode value)
strNum:
strSort:(unable to decode value)
strNorm:150
strUnit:2
strshul:
product_ID:307                         #采蘑菇数据
productsnum:1
totalprice:0.00
strProductsName:(unable to decode value)
strNum:
strSort:(unable to decode value)
strNorm:120
strUnit:5
strshul:
"""
