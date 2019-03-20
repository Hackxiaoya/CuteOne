# -*- coding:utf-8 -*-
import os, sys, subprocess
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

"""
    安装任务
"""

"""
    杀死自己，然后启动自己，哈哈哈
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-20
"""
# 杀死进程
def killProcess():
    try:
        subprocess.Popen("killall -9 uwsgi", shell=True)
    except Exception as e:
        pass
    subprocess.Popen("nohup uwsgi --ini {}/uwsgi.ini".format(os.getcwd()), shell=True)
    return


if __name__ =='__main__':
    killProcess()