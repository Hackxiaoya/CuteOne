# -*- coding:utf-8 -*-
import os, time, subprocess


"""
    refresh Web
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-02
"""
def restart_web():
    try:
        subprocess.Popen("killall -9 uwsgi", shell=True)
        time.sleep(2)
        subprocess.Popen("pgrep -f uwsgi", shell=True)
    except Exception as e:
        pass
    time.sleep(1)
    subprocess.Popen("nohop uwsgi --ini uwsgi.ini &", shell=True)


if __name__ =='__main__':
    restart_web()