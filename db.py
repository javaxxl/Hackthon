# -*- coding: utf-8 -*-
"""
Created on 2018/6/26 - the current system date.

__auther__ = 'xiaoliang'
"""
from sqlalchemy import create_engine

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
    conn.execute("update ciohackthon.email set sentiment_score = %d,sadness = %d, joy = %d, fear = %d, disgust = %d, anger = %d" % scoreList +" where id = %d" % id)
    # conn.execute("update ciohackthon.email set sentiment_score = %d, sadness = %d " % score +" where id = %d" % id)
    conn.execute("commit;")
    conn.close()

update_score(1,(20,10,10,10,20,10))