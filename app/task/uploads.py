# -*- coding:utf-8 -*-
import os, sys, json, threading
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app.admin.drive import models as driveModels
from app.admin.task import models as taskModels
import requests
import config

"""
    推送脚本
"""

"""
    推送任务
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    task_id: 任务id
    dirve_id: 驱动id
    fileName: 文件名称
    remotePath: 远程路径
"""
def upProcess(task_id, dirve_id, fileName, remotePath):
    data_list = driveModels.drive_list.find_by_drive_id(dirve_id)
    if data_list:
        for item in data_list:
            res = putfile(dirve_id, item.id, fileName, remotePath)
    target_filename = os.getcwd()+"/temp_uploads/" + str(dirve_id) + "/" + fileName
    os.remove(target_filename)  # 删除文件
    taskModels.task.update({"id": task_id, "status":1}) # 更新任务状态


def putfile(dirve_id, id, fileName, remotePath):
    if remotePath == "None":
        remotePath = "/"
    data_list = driveModels.drive_list.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    url = config.app_url + '/v1.0/me/drive/items/root:{}/{}:/content'.format(remotePath, fileName)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"])}
    pull_res = requests.put(url, headers=headers, data=open(os.getcwd()+"/temp_uploads/" + str(dirve_id) + "/" + fileName, 'rb'))
    pull_res = json.loads(pull_res.text)
    # print(pull_res)
    if 'error' in pull_res.keys():
        return False
    else:
        return True




if __name__ =='__main__':
    task_id = sys.argv[1]  # 任务id
    dirve_id = sys.argv[2]  # 驱动ID
    fileName = sys.argv[3]  # 文件名字
    remotePath = sys.argv[4]  # 上传路径
    upProcess(task_id, dirve_id, fileName, remotePath)