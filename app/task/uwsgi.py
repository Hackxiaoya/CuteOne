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
    child = subprocess.Popen(["pgrep", "-f", "uwsgi"], stdout=subprocess.PIPE, shell=False)
    pid = child.communicate()[0]
    if pid:
        respid = pid.decode(encoding='utf-8').split('\n')
        respid.remove('')   # 删除最后一个空数值
        for xpid in respid:
            os.system("kill -9 " + xpid)
    subprocess.Popen("uwsgi --ini {}/uwsgi.ini".format(os.getcwd()), shell=True)
    return


if __name__ =='__main__':
    killProcess()