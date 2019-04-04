# -*- coding:utf-8 -*-
import app

# 生产环境启用这段
app.socketio.run(app.app, host='0.0.0.0')

# 开发环境启动这段
# if __name__ == '__main__':
    # app.socketio.run(app.app, host='0.0.0.0', debug=True)