

import os
from typing import OrderedDict
import pandas as pd
import json
import numpy as nd
import requests
import csv
from pandas_profiling import ProfileReport
from mlxtend.frequent_patterns import apriori
from apyori import apriori
from mlxtend.frequent_patterns import association_rules
from flask import Flask, flash, jsonify, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, false, null
from mlxtend.preprocessing import TransactionEncoder

x5 = 1
shop = ""
cc1 = 1


def Sort_Tuple(tup):
    return(sorted(tup, key=lambda x: x[1], reverse=True))


t2 = ""
a3 = []
s6 = set()
results = []
df = []


def dataframe(l):
    global df, results

    lines = str(l)[2:len(str(l))-2].split('\\r\\n')
    reader = csv.reader(lines)
    parsed_csv = list(reader)
    df = parsed_csv
    # print(df)
    print(len(df))
    T = []
    for i in df:
        T.append([str(i[j]) for j in range(0, len(i)) if str(i[j]) != ''])
    rules = apriori(T, min_support=0.003, min_confidence=0.002,
                    min_lift=1.1, min_length=2)
    results = list(rules)
    # print(results)


def ml(s2):
    global t2
    global x5
    t3 = ""
    pair = []
    s4 = str(s2)
    print("results_len=", len(results))
    for i in results:
        t3 = '<div class="linedraw">'
        for j in i[2]:
            s5 = str(j[0])
            if s4[2:len(s4)-2] == s5[12:len(s5)-3]:
                s6 = j[1]
                s7 = j[2]*100
                for k in s6:
                    c1 = 1
                    for l in a3:
                        if str(l) == str(k):
                            t3 = t3 + \
                                '<a href="#" class="recombtn" onclick="check('+str(
                                    c1)+')" >'+str(k)+'</a><br>'
                            break
                        c1 = c1+1
                t3 = t3+"</div><br>"
                pair.insert(len(pair), (t3, s7))
                break
    pair = Sort_Tuple(pair)
    t3 = ""
    for a, b in pair:
        t3 = t3+str(a)
    t2 = t3


a1 = set()
a2 = ""
q1 = 1
c1 = 1
a5 = []
p1 = []
s1 = []
i1 = ""


def selectshop():
    global i1
    i1 = ""
    user = userdata.query.filter_by(index=x5).all()
    # i1=jsonify(user)

    for i in user:
        i1 = i1+str(i)+'<br>'
    print(i1)


shopname = ""


def f12():
    global a2, c1, df, x5, a1, a3, a5, a3, s1, t2, shopname
    # print(x5+2)
    shopname = ""
    ufile = shopdata.query.filter_by(id=x5+1).first()
    dataframe(ufile.data)
    print(ufile.filename)
    shopname = str(ufile.filename)
    a2 = ""
    c1 = 1
    t2 = ""
    a1 = set()
    a1.clear()
    a3.clear()
    p1.clear()
    a5.clear()
    s1.clear()
    for i in df:
        for j in range(0, len(i)):
            if str(i[j]) != '':
                a1.add(i[j])
    a1 = sorted(a1)
    for i in a1:
        a3.insert(len(a3), str(i))
        a2 = a2+'<a href="#" class="displaybtn" onclick=check('+str(c1)+') id='+str(
            c1-1)+'>'+str(i)+'</a><br>'
        # a3.insert(len(a3),str(i))
        # a5.insert(len(a3),str(i))
        c1 = c1+1


chartdata = []
piechart = []
linechart = []
shopnames = []


def sendchartdata():

    # storing latest customer data
    global chartdata, x5, piechart, linechart, shopnames, s1
    itemnames = "\r\n"
    for i in s1:
        itemnames = itemnames+i+","

    print(s1)
    itemupdate = shopdata.query.filter_by(id=x5+1).first()
    # itemupdate.data = bytes(str(df), encoding='utf8')
    itemupdate.data = itemupdate.data+(bytes(itemnames, encoding='utf8'))
    db.session.commit()

    dataframe(itemupdate.data)

    lenx = shopdata.query.all()
    chartdata.clear()
    piechart.clear()
    linechart.clear()
    shopnames.clear()
    chartdata.insert(len(chartdata), ['Shop', 'Total Customers'])
    piechart.insert(
        len(piechart), ['Items', 'Number of customer who purchased item till now'])
    # linechart.insert(len(linechart), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(1, len(lenx)+1):
        ufile = shopdata.query.filter_by(id=i).first()
        shopnames.insert(len(shopnames), str(ufile.filename))
        ufile1 = userdata.query.filter_by(index=i-1).all()
        chartdata.insert(
            len(chartdata), [str(ufile.filename), len(ufile1)])
    temp = {}
    for i in df:
        # r1 = r1+len(i)
        for j in range(0, len(i)):
            if str(i[j]) != '':
                if (i[j] in temp):
                    temp[i[j]] += 1
                else:
                    temp[i[j]] = 1
    # temp = Sort_Tuple(temp)
    temp = dict(OrderedDict(
        sorted(temp.items(), key=lambda te: te[1], reverse=True)))
    sum = 0
    cc1 = 1
    for key, value in temp.items():
        piechart.insert(len(piechart), [key, value])
        cc1 = cc1+1
        sum = sum+value
        if cc1 == 11:
            break
    cc1 = 0
    cc2 = 1
    for i in range(1, 11):
        v1 = []
        v1.clear()
        v1.insert(len(v1), i)
        for j in range(1, len(lenx)+1):
            v1.insert(len(v1), 0)
        linechart.insert(len(linechart), v1)

    for i in range(1, len(lenx)+1):
        ufile = shopdata.query.filter_by(id=i).first()
        l = ufile.data
        lines = str(l)[2:len(str(l))-2].split('\\r\\n')
        reader = csv.reader(lines)
        parsed_csv = list(reader)
        dftemp = parsed_csv
        cc1 = 0
        for j in range(len(dftemp)-10, len(dftemp)):
            l2 = 0
            for k in range(0, len(dftemp[j])):
                if str(dftemp[j][k]) != '':
                    l2 = l2+1
            linechart[cc1][cc2] = l2
            cc1 = cc1+1
        cc2 = cc2+1


def shopupdate():
    lenx = shopdata.query.all()
    global shop
    shop = ""
    for i in range(1, len(lenx)+1):
        ufile = shopdata.query.filter_by(id=i).first()
        shop = shop + \
            '<a href="#" onclick=check('+str(i)+')>'+str(ufile.filename)+'</a>'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = false
app.secret_key = "abc"
db = SQLAlchemy(app)


class userdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=false)

    def __repr__(self) -> str:
        return f"{self.username}"


class shopdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

# f12()


@app.route('/')
def homepage():
    shopupdate()
    return render_template("homepage.html", shop=shop)


@app.route('/bar_chart', methods=["GET", "POST"])
def bar_chart():
    if request.method == 'POST':
        sendchartdata()
    return render_template("bar_chart.html", df2=chartdata, df3=piechart, linechart=linechart, shopnames=shopnames, itembuy=s1)


@app.route('/home/', methods=["GET", "POST"])
def home():
    return render_template("f.html", T=a2, T2=t2, p1=p1)


@app.route('/user')
def user():
    return render_template("userpage.html", index=i1)


@app.route('/desc', methods=["GET", "POST"])
def desc():
    return render_template("desc.html", shop=shop)


@app.route('/upload/', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if str(file.filename)[len(str(file.filename))-4:len(str(file.filename))] == '.csv':
            # print(file.read())
            uploadfile = shopdata(filename=str(file.filename)[
                                  0:len(str(file.filename))-4], data=file.read())
            db.session.add(uploadfile)
            db.session.commit()
            shopupdate()
        else:
            flash("File is not csv Upload again...")
    return render_template("upload.html", shop=shop)


@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html", shop=shop)


@app.route('/sendusername/<string:userInfo2>', methods=['POST'])
def sendusername(userInfo2):
    global a2, t2, p1
    userInfo2 = json.loads(userInfo2)
    print('success')
    x6 = userInfo2['y2']
    username = userdata.query.filter_by(username=x6, index=x5).first()
    if username is None:
        t = userdata(username=x6, index=x5)
        db.session.add(t)
        db.session.commit()
    print(db.session.query(userdata).all())
    selectshop()
    print(x5)
    return "success"


@app.route('/refreshhome', methods=['POST'])
def refreshhome():
    f12()
    return jsonify({'stuff': t2, 'T': a2, 'selected': p1, 'shopname': shopname})


@app.route('/send_github/<string:userInfo1>', methods=['POST'])
def send_github(userInfo1):
    userInfo1 = json.loads(userInfo1)
    print('success')
    global x5, i1
    x5 = userInfo1['y2']
    x5 = x5-1
    selectshop()
    return redirect(url_for('user'))


@app.route('/processUserInfo/<string:userInfo>', methods=['POST'])
def processUserInfo(userInfo):
    userInfo = json.loads(userInfo)
    print()
    global s1, a2, p1
    print('success')
    x4 = userInfo['y2']-1
    print(userInfo)
    f = 0
    for i in range(0, len(s1)):
        if s1[i] == a3[x4]:
            s1.pop(i)
            p1.pop(i)
            f = -1
            break
    if f == 0:
        s1.insert(len(s1)-1, a3[x4])
        p1.insert(len(p1)-1, x4)
    for i in s1:
        print(i)
    c1 = 1
    a2 = ""
    for i in p1:
        a2 = a2+'<a href="#" class="displaybtn" onclick=check('+str(i+1)+') id='+str(
            i)+'>'+str(a3[i])+'</a><br>'
    for i in a3:
        f = 0
        for j in p1:
            if j+1 == c1:
                f = -1
                break
        if f == 0:
            a2 = a2+'<a href="#" class="displaybtn" onclick=check('+str(c1)+') id='+str(
                c1-1)+'>'+str(i)+'</a><br>'
            # a3.insert(len(a3),str(i))
            # a5.insert(len(a3),str(i))
        c1 = c1+1
    ml(s1)
    # pyautogui.hotkey('f5')
    print('------')
    return "Asdaw"


@app.route('/sendprocessUserInfo/', methods=['POST'])
def sendprocessUserInfo():
    return jsonify({'stuff': t2, 'T': a2, 'selected': p1, 'shopname': shopname})


port = int(os.environ.get('PORT', 33507))
if __name__ == "__main__":
    app.run(debug=True, port=port)
