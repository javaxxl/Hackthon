# -*- coding: utf-8 -*-
"""
Created on 2018/1/12 - the current system date.

__auther__ = 'xiaoliang'
"""
import multiprocessing

from flask import Flask, jsonify, render_template
import time
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)

new_count = 0
old_count = 0
from sqlalchemy import create_engine

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
        import Features, EntitiesOptions, KeywordsOptions, SentimentOptions, EmotionOptions, ConceptsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
        username='53c57af7-1ee8-44a1-a524-27d71fd9fe30',
        password='6J1B4fZR0BdL',
        version='2017-02-27')

engine = create_engine("mysql+pymysql://root:passw0rd@127.0.0.1:3306/CIOHackthon",
                       connect_args={'charset':'utf8'},
                       max_overflow=5)

conn= engine.connect()

# 保存每次数据库查询的结果
# def save_count(n):
#     with open('static/count.txt', 'r+', encoding='utf8') as f:
#         f.write(str(n))
#
# def read_count():
#     count = 0
#     with open('static/count.txt', 'r+', encoding='utf8') as f:
#         count = int(f.readline())
#     return count
#
# def save_notice_flag(n):
#     with open('static/notice_flag.txt', 'r+', encoding='utf8') as f:
#         f.write(n)
#
# def read_notice_flag():
#     with open('static/notice_flag.txt', 'r+', encoding='utf8') as f:
#         notice = f.readline()
#         return notice

def update_score(id,scoreList):
    conn.execute("update ciohackthon.email set sentiment_score = %f,sadness = %f, joy = %f, fear = %f, disgust = %f, anger = %f, keywords = '%s'" % scoreList +" where id = %d" % id)
    # conn.execute("update ciohackthon.email set sentiment_score = %d " % scoreList +" where id = %d" % id)
    conn.execute("commit;")
    # conn.close()

def get_score(res):

    subject = ""
    emotion = {}
    item = {}
    keywords =""

    score = 0

    context = res[7] + res[1]

    # 如果没有分数，就调用watson API
    if res[6] == "" or res[6] is None or (res[6] == 0 and res[8] == 0 and res[10] == 0):
    # if res[6] is not None:
        try:
            response = natural_language_understanding.analyze(
                text=context,
                features=Features(
                    sentiment=SentimentOptions(
                    ),emotion=EmotionOptions(),keywords=KeywordsOptions()))
            score = response['sentiment']['document']['score']
            emotion = response['emotion']['document']['emotion']
            for i in range(len(response.get("keywords"))):
                keywords = keywords + response.get("keywords")[i].get("text")+','
            if len(keywords) > 0:
                keywords = keywords[0:-1]

        except Exception as e:
            print(e)
            # score = None
            # emotion = None
    # 如果有分数，直接赋值和判断
    # print(emotion['sadness'])

    # print(type(emotion))
    # print(emotion)

        item = {"id": res[0], "subject": res[7], "body": res[1], "sender": res[4],
                "cclist": res[2], "receievedTimestamp": res[3].strftime('%Y-%m-%d %H:%M:%S'),
                "senderRole": res[5], "sentimentScore": score,"keywords":keywords}
        # print(emotion)
        if len(emotion) > 0:
            item.setdefault('sadness', emotion['sadness'])
            item.setdefault('joy', emotion['joy'])
            item.setdefault('fear', emotion['fear'])
            item.setdefault('disgust', emotion['disgust'])
            item.setdefault('anger', emotion['anger'])

        else:
            item.setdefault('sadness', 0)
            item.setdefault('joy', 0)
            item.setdefault('fear', 0)
            item.setdefault('disgust', 0)
            item.setdefault('anger', 0)
        # print(context)

        update_score(res[0],(item['sentimentScore'],  item['sadness'],item['joy'], item['disgust'], item['anger'], item['fear'],item['keywords']))


    #如果数据库中有值，直接读取
    else:
        item = {"id": res[0], "subject": res[7], "body": res[1], "sender": res[4],
                "cclist": res[2], "receievedTimestamp": "2018-06-27 14:16:56",
                "senderRole": res[5], "sentimentScore": res[6],
                'joy':res[8],"sadness":res[9], "disgust":res[10], "anger":res[11], "fear":res[12],"keywords":res[13] }
    # print("============item================")
    print(item)
    return item

def get_records():

    emails = []

    result = []

    res_db = conn.execute("select * from email;")


    pool = multiprocessing.Pool(processes=4)

    for res in res_db:
        # print("=========database================")
        # print(res)
        result.append(pool.apply_async(get_score, (res,)))

    pool.close()
    pool.join()
    for r in result:
        emails.append(r.get())
        # print(r.get())
    # print(emails)
    # print(emails)
    return emails

"""
#-----------------------------------
#Query
#-----------------------------------
resultProxy=db.execute("select * from users")
resultProxy.close(), resultProxy 用完之后, 需要close
resultProxy.scalar(), 可以返回一个标量查询的值
ResultProxy 类是对Cursor类的封装(在文件sqlalchemy\engine\base.py),
ResultProxy 类有个属性cursor即对应着原来的cursor.
ResultProxy 类有很多方法对应着Cursor类的方法, 另外有扩展了一些属性/方法.
resultProxy.fetchall()
resultProxy.fetchmany()
resultProxy.fetchone()
resultProxy.first()
resultProxy.scalar()
resultProxy.returns_rows  #True if this ResultProxy returns rows.
resultProxy.rowcount  #return rows affected by an UPDATE or DELETE statement. It is not intended to provide the number of rows present from a SELECT.

****遍历ResultProxy时, 得到的每一个行都是RowProxy对象, 获取字段的方法非常灵活, 下标和字段名甚至属性都行. rowproxy[0] == rowproxy['id'] == rowproxy.id, 看得出 RowProxy 已经具备基本 POJO 类特性.  
"""



#
# def get_num():
#     num = 0
#     conn = engine.connect()
#     res = conn.execute("select count(*) from email;")
#     num = res.scalar()
#     conn.close()
#     return num


# df = pd.read_excel("C:\Rock\RockXu_060921\python\PythonExcercise\csv\eqlist.xls",skiprows=img,names=col_list)
# df = pd.read_excel("C:\Rock\RockXu_060921\python\PythonExcercise\csv\geo.xls",names=csv_list,encoding='utf8')


# tasks = [{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 2","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 4","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com,liaokai@cn.ibm.com","receievedTimestamp":"2017-01-10 12:00:06","senderRole":"user","sentimentScore":"0.35"},{"id":1,"subject":"test subject 10","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.85"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.47"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"-0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"-0.65"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.35"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.45"},{"id":1,"subject":"test subject 1","body":"test email body 1","sender":"jmyu@cn.ibm.com","cclist":" whxuxl@cn.ibm.com liaokai@cn.ibm.com","receievedTimestamp":"2017-01-11 12:00:06","senderRole":"user","sentimentScore":"0.47"}]

@app.route('/emails', methods=['GET'])
def get_tasks():

    emails = get_records()
    # print("===========emails type==========")
    # print(type(emails))

    return jsonify(emails)

@app.route('/count', methods=['GET'])
# def get_count():
#
#     new_count = get_num()
#     print("new_count: ",new_count)
#     old_count = read_count()
#     print("old_count: ",old_count)
#     notice_content = read_notice_flag()
#     if old_count < new_count and notice_content.split("{}")[0] == "Y":
#
#         flag = "Y"
#         # res_db = conn.execute("select * from ciohackthon.email where id in ( select max(id) from ciohackthon.email);")
#         # for i in res_db:
#         #     print(i)
#
#
#     else:
#         flag = "N"
#     print("notice_content:",notice_content.split("{}")[1])
#     save_count(new_count)
#     save_notice_flag("")
#     return jsonify({"flag":flag,"body":notice_content.split("{}")[1]})


# @app.route('/')
# def index():
#
#     print("index")
#     localtime = time.asctime(time.localtime(time.time()))
#     print(localtime)
#     return render_template('index.html')
#     # return render_template('index2.html')

@app.route('/')
def index_ian():

    print("index-Ian2")
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)
    return render_template('index-Ian2.html')
    # return render_template('index2.html')







if __name__ == '__main__':
    app.debug = True
    ip = '0.0.0.0'
    app.run(host='0.0.0.0')