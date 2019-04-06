# -*- coding:utf-8 -*-
import os


"""
    判断上传任务进度
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-06
    task_id: 任务id
"""
def isPullUploads(task_id):
    try:
        command = "ps -ef | grep 'python3 {}/app/task/uploads.py {}' | grep -v grep | wc -l".format(os.getcwd(), task_id)
        process = os.popen(command).read()
        if process[0:1] == "0":
            return False
        else:
            return True
    except:
        return