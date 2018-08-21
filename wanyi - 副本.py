#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''网易考拉签到,功能已经实现，现在出现问题，1，由于vps在国外，所以导致只要放到vps上就会弹出验证码
2，要做出classs类

'''
# print r2.content.decode('utf-8').encode('gb2312')
import requests
import re
import hashlib
import rsa
import binascii
import json
import base64
import time


def haspw(password,servertime,nonce,pubkey):#密码加密
    RSAKey = rsa.PublicKey(int(pubkey,16),65537) #创建公钥
    codeStr = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #根据js拼接方式构造明文
    pwd = rsa.encrypt(codeStr.encode('utf-8'), RSAKey)  #使用rsa进行加密
    return binascii.b2a_hex(pwd)
    
def dataprogress(s,su):#预登录数据处理
    pre_url = "https://login.sina.com.cn/sso/prelogin.php?entry=openapi&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url +su+"&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="+str(int(time.time()*1000))
    r1=s.get(pre_url,headers=headers)#获取预登录数据

    servertime = re.compile('"servertime":\d{10}')
    servertime=servertime.findall(r1.content)
    servertime=servertime[0].replace('"servertime":','')
    nonce = re.compile('"nonce":".{6}')
    nonce=nonce.findall(r1.content)
    nonce=nonce[0].replace('"nonce":"','')
    rsakv = re.compile('"rsakv":"\d{10}')
    rsakv=rsakv.findall(r1.content)
    rsakv=rsakv[0].replace('"rsakv":"','')
    pubkey = re.compile('"pubkey":".{256}')
    pubkey=pubkey.findall(r1.content)
    pubkey=pubkey[0].replace('"pubkey":"','')
    yanzhen=download(s,pcid)
    sp=haspw('密码',servertime,nonce,pubkey)#进入加密模块——输入密码，加密密码
    return login(s,su,servertime,nonce,rsakv,sp)#返回到正式登录

def download(s,pcid):#下载验证码进行处理
    # url='https://login.sina.com.cn/cgi/pin.php?r=36944441&s=0&p='+pcid
    # yanzhen=s.get(url)
    # with open('D:\\BaiduNetdiskDownload\\1.png', "wb") as file:
       # for data in yanzhen.content:
           # file.write(data)
    im=Image.open ('D:\\BaiduNetdiskDownload\\1.png')
    img=im.convert('RGBA')
    pix = img.load()
    for y in range(img.size[1]):  # 二值化处理，这个阈值为R=95，G=95，B=95
        for x in range(img.size[0]):
            if (pix[x, y][0] == 101 and pix[x, y][1] == 101) or (pix[x, y][0] and pix[x, y][2] == 101) or (pix[x, y][1] and pix[x, y][2] == 101):
                pix[x, y] = (255, 255, 255, 255)
            # elif pix[x, y][0] < 255 or pix[x, y][1] < 255 or pix[x, y][2] < 255:
                # pix[x, y] = (0, 0, 0, 255)
    img.save('D:\\BaiduNetdiskDownload\\2.png', 'png')
    print pytesser.image_file_to_string('D:\\BaiduNetdiskDownload\\2.png')#图片识别，效度堪忧
    
def login(s,su,servertime,nonce,rsakv,sp):#正式登陆数据处理
    postdata={
        'entry': 'openapi',
        'gateway': '1',
        'from':'',
        'savestate': '0',
        'userticket': '1',
        'pagerefer':'',
        'ct': '1800',
        'pcid':pcid,#验证码图片编码,
        's':'1',
        'vsnf': '1',
        'vsnval': '',
        'door':yanzhen,#验证码内容
        'appkey':'52laFx',
        'su':su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv' : rsakv,
        'sp': sp,
        'sr':'1920*1080',
        'encoding': 'UTF-8',
        'cdult':'2',
        'domain':'weibo.com',
        'prelt':'2140',
        'returntype': 'TEXT'
        }

    get_ticket_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_='+str(int(time.time()*1000))+'&openapilogin=qrcode'
    proxies ={
    "http":"http://127.0.0.1:1080",
    }
    r2=s.post(get_ticket_url,headers=headers,data=postdata,proxies=proxies)
    print r2.content
    ticket = re.compile('"ticket":".{68}')
    ticket=ticket.findall(r2.content)
    ticket=ticket[0].replace('"ticket":"','')
    uid = re.compile('"uid":"\d{10}')
    uid=uid.findall(r2.content)
    uid=uid[0].replace('"uid":"','')
    return denglu(s,ticket)#进入考拉登录模块
    
def denglu (s,ticket):#考拉登录
    data2={
            'action':'login',
            'display':'default',
            'withOfficalFlag':'0',
            'quick_auth':'false',
            'withOfficalAccount':'',
            'scope':'',
            'ticket':ticket,
            'isLoginSina':'',
            'response_type':'code',
            'regCallback':'https%3A%2F%2Fapi.weibo.com%2F2%2Foauth2%2Fauthorize%3Fclient_id%3D469534363%26response_type%3Dcode%26display%3Ddefault%26redirect_uri%3Dhttps%253A%252F%252Freg.163.com%252FouterLogin%252Foauth2%252Fsina_connect.do%253Furl%253Dhttp%25253A%25252F%25252Fglobal.163.com%25252Furs%25252Fredirect.html%25253Ftarget%25253Dhttps%2525253A%2525252F%2525252Fwww.kaola.com%2525252Fopener_callback.html%2526amp%253Burl2%253Dhttp%25253A%25252F%25252Fglobal.163.com%25252Furs%25252Fredirect.html%2526amp%253Bproduct%253Dkaola%2526amp%253Bdomains%253Dglobal.163.com%2526amp%253Burs_tg%253D3%26from%3D%26with_cookie%3D',
            'redirect_uri':'https://reg.163.com/outerLogin/oauth2/sina_connect.do?url=http%3A%2F%2Fglobal.163.com%2Furs%2Fredirect.html%3Ftarget%3Dhttps%253A%252F%252Fwww.kaola.com%252Fopener_callback.html&url2=http%3A%2F%2Fglobal.163.com%2Furs%2Fredirect.html&product=kaola&domains=global.163.com&urs_tg=3',
            'client_id':'469534363',
            'appkey62':'KE0k3',
            'state':'',
            'verifyToken':'null',
            'from':'',
            'switchLogin':'0',
            'userId':'',
            'passwd':''
            }
    newheader={
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Referer':'https://api.weibo.com/oauth2/authorize?client_id=469534363&redirect_uri=https%3A%2F%2Freg.163.com%2FouterLogin%2Foauth2%2Fsina_connect.do%3Furl%3Dhttp%253A%252F%252Fglobal.163.com%252Furs%252Fredirect.html%253Ftarget%253Dhttps%25253A%25252F%25252Fwww.kaola.com%25252Fopener_callback.html%26url2%3Dhttp%253A%252F%252Fglobal.163.com%252Furs%252Fredirect.html%26product%3Dkaola%26domains%3Dglobal.163.com%26urs_tg%3D3&response_type=code&forcelogin=true'
    }
    denglu=s.post('https://api.weibo.com/oauth2/authorize',headers=newheader,data=data2)
    pattern = re.compile(r'dataKey.{46}')
    datakey=pattern.findall(denglu.content)
    datakey=datakey[0].replace('dataKey=','')

    params5={
        'dataKey':datakey,
    }
    r6=s.get('http://www.kaola.com/urs/setUrsCookie.html',params=params5)

    idurl='https://www.kaola.com/personal/my_sign.html?riskToken=2_5c0d3d037dfb420aba3a3047246abc1f_Es6xHkL3bGw8YifKLblGtZt2egWLzJTY_R1Bi6IPBSF4AKx2RIXk%2Bjw%3D%3D'
    qiandao=s.get(idurl)#签到页面
    print qiandao.content.decode('utf-8').encode('gb2312')#正确反馈200：签到成功，错误反馈401，已经签到


#头文件
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'DNT':'1'
    }
s= requests.session()#合并session共用cookie等数据
su = base64.b64encode('你的用户名'.encode("utf-8"))#用户名编码，此处输入用户名
dataprogress(s,su)#数据处理















