# -*- coding:utf-8 -*-
import datetime, os, re
import hashlib, subprocess
from app.admin.system import models as systemModels


"""
    版本信息
"""
SystemInfo = {
    "name": "CuteOne",
    "versionType": "Free",
    "versions": "1.2.0",
    "server": ""
}




"""
    公共方法
    
"""


"""
    加密密码
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    data: 明文密码
"""
def hashPwd(data):
    pwd_temp = hashlib.sha1(data.encode('utf-8')).hexdigest()
    pwd_temp = hashlib.md5(("cuteone" + pwd_temp).encode('utf-8')).hexdigest()
    return pwd_temp


"""
    UTC时间转本地时间（+8: 00）
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
"""
def utc_to_local(utc):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utcTime = datetime.datetime.strptime(utc, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    return localtime


"""
    b转KB MB 尺寸转换
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
"""
def size_cov(size):
    if size / (1024 * 1024 *1024) >= 1:
        size = str(round(size / (1024 * 1024 * 1024), 2)) + " G"
    elif size / (1024 * 1024) >= 1:
        size = str(round(size / (1024 * 1024), 2)) + " MB"
    else:
        size = str(round(size / 1024, 2)) + " KB"
    return size


"""
    执行shell指令
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    command: shell指令
"""
def run_command(command):
    subprocess.Popen(command, shell=True)


"""
    判断进程是否存在
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
"""
def isRunning(process_name):
    try:
        process = len(os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines())
        if process >= 1:
            return 1
        else:
            return
    except:
        return


"""
    获取域名
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-17
"""
def get_web_site():
    return systemModels.config.get_web_site()



"""
    restart web
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-02
"""
def restart():
    command = "python3 {}/app/task/restart.py".format(os.getcwd())
    run_command(command)
