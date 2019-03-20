# -*- coding:utf-8 -*-
import app

# 生产环境启用这段
app.app.run(host='0.0.0.0')

# 开发环境启动这段
# if __name__ == '__main__':
    # app.app.run(host='0.0.0.0')   # host='0.0.0.0'