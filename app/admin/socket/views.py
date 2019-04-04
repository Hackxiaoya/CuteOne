# -*- coding:utf-8 -*-
import requests, json
import app


# websocket
@app.socketio.on('synClientEvent', namespace='/websocket')
def index_message(message):
    print(message)
    # app.socketio.emit('server_response', {'data': "enen"}, namespace='/websocket')


# 用作与进程通讯数据
@app.socketio.on('synProcessEvent', namespace='/websocket')
def send_message(data):
    app.socketio.emit('server_response_'+str(data['data']['id']), {'data': data['data']['msg']}, namespace='/websocket')