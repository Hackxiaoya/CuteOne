# -*- coding:utf-8 -*-
import os, subprocess

"""
    更新脚本
"""

"""
    杀死自己，然后启动自己，哈哈哈
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-22
"""
# 杀死进程
def killProcess():
    try:
        subprocess.Popen("killall -9 uwsgi", shell=False)
    except Exception as e:
        pass
    return


# 启动进程
def startProcess():
    try:
        subprocess.Popen("uwsgi --ini {}/uwsgi.ini &".format(os.getcwd()), shell=True)
    except Exception as e:
        pass
    return


# 拉取更新
def pullUpdate():
    print("1")


# 解压压缩包



if __name__ =='__main__':
    killProcess()