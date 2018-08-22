#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import request
from flask import Flask
app = Flask(__name__)
@app.route('/',methods=['GET'])
def hell_world():
    url='https://login.sina.com.cn/cgi/pin.php?r=36944441&s=0&p=gz-d41fcfe9796b3de96abf3adb97d9d78f8fb1'
    return '<form action="/" method="post"><img src="%s"><br><input name="yanzhen"><br><button type="submit">提交</button></form>'%url


@app.route('/',methods=['POST'])
def yanzhen():
        l=request.form['yanzhen']
        return request.form['yanzhen']
app.run()
