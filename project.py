# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import json
import pika
import sys
import logging
import os
import time
from flask import Flask,jsonify,request
#db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
#query = "SELECT * FROM chatrooms"
#cursor = db.cursor()
#cursor.execute(query)
#results =cursor.fetchall()
#print results
#db.close()
"""class MyDatabase:
      db = None
      def __init__(self):
          self.connect()
          return
      def connect(self):
          self.db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
          return"""
app = Flask(__name__)

@app.route('/iems5722/get_chatrooms',methods=['GET'])
def get_chatrooms():
    db = MySQLdb.connect("localhost","root","dhdj513758","iems5722",cursorclass = MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM chatrooms"
    cursor = db.cursor()
    cursor.execute(query)
    data =cursor.fetchall()
    db.close()
    return jsonify({"data":data},status="OK")

@app.route('/iems5722/get_messages')
def get_messages():
    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()
    db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
    chatroom_id = request.args.get("chatroom_id",0,type = int)
    page = request.args.get("page",0,type = int)
    query = "SELECT * FROM messages WHERE chatroom_id = %s"
    params = (chatroom_id,)
    cursor = db.cursor()
    cursor.execute(query,params)
    messages =cursor.fetchall()
    string_t = []
    if messages is None:
      db.close()
      return jsonify(message="<error message>",status="ERROR")
    else:
       for row in messages:
        roww = {}
        roww["message"]=row[4]
        roww["user_id"]=row[2]
        roww["name"]=row[3]
        roww["timestamp"]=str(row[5])
        string_t.append(roww)
       messages_num = cursor.execute(query,params)
       total_pages = messages_num / 5 + 1
       string_u = string_t[::-1]
       string = string_u[page * 5 - 5:page * 5]
       data = {
           "current_page":page,
           "messages":string,
           "total_pages":total_pages,
       }
       db.close()
       return jsonify(data=data,status="OK")
       
@app.route('/iems5722/send_message',methods=['GET','POST'])
def send_messages():
    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()
    db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
    name = request.form.get("name")
    query = "SELECT userid FROM users WHERE username = %s"
    params = (name,)
    cursor = db.cursor()
    cursor.execute(query,params)
    user_id_2 =cursor.fetchall()
    user_id_1 = user_id_2[0]
    user_id = user_id_1[0]

    message = request.form.get("message")
    chatroom_id = request.form.get("chatroom_id")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message_s =(name,user_id,message,chatroom_id,timestamp)
    if name == "":
        db.close()
        return jsonify(message="<error message>",status="ERROR")
    if user_id == "":
        db.close()
        return jsonify(message="<error message>",status="ERROR")
    if message == "":
        db.close()
        return jsonify(message="<error message>",status="ERROR")
    if chatroom_id == "":
        db.close()
        return jsonify(message="<error message>",status="ERROR")
    else:
        query = "INSERT INTO messages (name,user_id,message,chatroom_id,timestamp) VALUES (%s,%s,%s,%s,%s)"
        cursor = db.cursor()
        cursor.execute(query,message_s)
        query1 = "SELECT name FROM chatrooms WHERE id = %s"
        params1 = (chatroom_id,)
        cursor.execute(query1,params1)
        chatroom_name =cursor.fetchall()
        for row in chatroom_name:
                data = {
                     "chatroom":row[0],
                     "message":message
                }
                json_string = json.dumps(data)
                db.commit()

                connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host='localhost'))
                channel = connection.channel()

                channel.queue_declare(queue='test')
                channel.basic_publish(exchange='',
                        routing_key='test',
                        body=json_string
                        )
                print(" [x] Send %r" % json_string)
                connection.close()

                db.close()
                return jsonify(status="OK")

@app.route('/iems5722/submit_push_token',methods=['GET','POST'])
def submit_push_token():
        db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
        user_id = request.form.get("user_id")
        token = request.form.get("token")
        tokens =(user_id,token)
        query = "INSERT INTO push_tokens (user_id,token) VALUES (%s,%s)"
        cursor = db.cursor()
        cursor.execute(query,tokens)
        db.commit()
        db.close()
        return jsonify(status="OK")

@app.route('/iems5722/user_information',methods=['GET','POST'])
def registration():
        db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
        userid = request.form.get("userid")
        username = request.form.get("username")
        password = request.form.get("password")
        userlevel = 0
        exp = 0
        message_s =(userid,username,userlevel,exp,password)
        query = "SELECT username FROM users"
        cursor = db.cursor()
        cursor.execute(query)
        username_exist = cursor.fetchall()
        for x in xrange(0,len(username_exist)):
                username_exist2 = username_exist[x]
                if str(username) == str(username_exist2[0]):
                        a = 0
                else:
                        if userid == "":
                                a = 0
                        if username == "":
                                a = 0
                        if password == "":
                                a = 0
                        else:
                                a = 1
        if a == 1:
                query = "INSERT INTO users (userid,username,userlevel,exp,password) VALUES (%s,%s,%s,%s,%s)"
                cursor = db.cursor()
                cursor.execute(query,message_s)
                db.commit()
                db.close()
                return jsonify(status="OK")
        else:
                db.close()
                return jsonify(status="ERROR")


@app.route('/iems5722/log_in',methods=['GET','POST'])
def log_in():
    db = MySQLdb.connect("localhost","root","dhdj513758","iems5722",cursorclass = MySQLdb.cursors.DictCursor)
    username_log = request.form.get("username_log")
    password_log = request.form.get("password_log")

    query = "SELECT username FROM users"
    cursor = db.cursor()
    cursor.execute(query)
    username = cursor.fetchall()
    username_2 = []
    for row in username:
        username_1 = str(row['username'])
        username_2.append(username_1)

    for x in xrange(0,len(username_2)):
        if str(username_log) == str(username_2[x]):
                query = "SELECT password FROM users WHERE username = %s"
                params = (username_log,)
                cursor = db.cursor()
                cursor.execute(query,params)
                data = cursor.fetchall()
                password_1 = data[0]
                password = str(password_1['password'])
                if str(password_log) == password:
                        db.close()
                        return jsonify(status="OK")
                else:
                        db.close()
                        return jsonify(message = "<wrong password>",status="ERROR")
        else:
                b = 2
    if b == 2:

        db.close()
        return jsonify(message = "<wrong username>",status="ERROR")


@app.route('/iems5722/danmu',methods=['GET','POST'])
def danmu():
    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()
    db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
    chatroom_id = request.args.get("chatroom_id",0,type = int)
    page = request.args.get("page",0,type = int)
    time_receive = request.args.get("timestamp",0,type = int)
    query = "SELECT * FROM messages WHERE chatroom_id = %s"
    params = (chatroom_id,)
    cursor = db.cursor()
    cursor.execute(query,params)
    messages =cursor.fetchall()
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    times_num = time.mktime(time.strptime(times,"%Y-%m-%d %H:%M:%S"))
    string_t = []
    if messages is None:
      db.close()
      return jsonify(message="<error message>",status="ERROR")
    else:
       for row in messages:
        username = row[3]
        query = "SELECT userlevel FROM users WHERE username = %s"
        params = (username,)
        cursor = db.cursor()
        cursor.execute(query,params)
        userlevel =cursor.fetchall()
        level = userlevel[0]
        roww = {}
        timestamp = row[5]
        timestamp_num = time.mktime(time.strptime(str(timestamp),"%Y-%m-%d %H:%M:%S"))
        if timestamp_num < times_num+1 and timestamp_num > time_receive-1:
                        roww["message"] = row[4]
                        roww["level"] = level[0]
                        if level[0] < 5:
                            roww["color"] = "blue"
                        if level[0] > 4 and level[0] < 10:
                            roww["color"] = "yellow"
                        if level[0] > 9 and level[0] < 15:
                            roww["color"] = "red"
                        if level[0] > 14 and level[0] < 20:
                            roww["color"] = "pink"
                        if level[0] > 19:
                            roww["color"] = "green"
                        string_t.append(roww)

       db.close()
       return jsonify(data=string_t,time=times_num)



       
@app.route('/iems5722/likes',methods=['GET','POST'])
def likes():
    db = MySQLdb.connect("localhost","root","dhdj513758","iems5722")
    one = request.form.get("one")
    username = request.form.get("username")
    my_username = request.form.get("my_username")
    if one == "OK":
        query = "SELECT exp FROM users WHERE username = %s"
        params = (username,)
        cursor = db.cursor()
        cursor.execute(query,params)
        exp = cursor.fetchall()
        exp_1 = exp[0]
        exp_2 = exp_1[0]
        if my_username == "Albert":
            query = "UPDATE users SET exp = exp + 10 WHERE username = %s"
            params = (username,)
            cursor = db.cursor()
            cursor.execute(query,params)
            db.commit()
            db.close()
            exp_after = exp_2 + 10
            return jsonify(message=exp_after,status="OK")
        else:
            query = "UPDATE users SET exp = exp + 1 WHERE username = %s"
            params = (username,)
            cursor = db.cursor()
            cursor.execute(query,params)
            db.commit()
            db.close()
            exp_after = exp_2 + 1
            return jsonify(message=exp_after,status="OK")
    else:
        db.close()
        return jsonify(message="<error message>",status="ERROR")


@app.route('/iems5722/homepage',methods=['GET','POST'])
def homepage():
    db = MySQLdb.connect("localhost","root","dhdj513758","iems5722",cursorclass = MySQLdb.cursors.DictCursor)
    username = request.args.get("username")
    query = "SELECT exp FROM users WHERE username = %s"
    params = (username,)
    cursor = db.cursor()
    cursor.execute(query,params)
    exp =cursor.fetchall()
    exp_1 = exp[0]
    exp_2 = exp_1['exp']
    level = int(exp_2 / 10)
    query = "UPDATE users SET userlevel = %s WHERE username = %s"
    params = (level,username)
    cursor = db.cursor()
    cursor.execute(query,params)
    db.commit()
    db.close()
    return jsonify(exp=exp_2,userlevel=level,status="OK")


app.debug = True
if __name__ == '__main__':
    app.run(host = '0.0.0.0')
