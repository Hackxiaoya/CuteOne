# -*- coding:utf-8 -*-
import os, sys, json
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app.admin.drive import models as driveModels
from app.admin.task import models as taskModels
from app.task import uploadcom

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
def upProcess(task_id, drive_id, fileName, remotePath):
    data_list = driveModels.disk.find_by_drive_id(drive_id)
    filesize = os.path.getsize(os.getcwd() + "/temp_uploads/" + str(drive_id) + "/" + fileName)
    filePath = os.getcwd()+"/temp_uploads/" + str(drive_id) + "/"
    for item in data_list:
        if filesize > 4194304:
            uploadcom.putfilebig(item.id, drive_id, filePath, fileName, remotePath)
        else:
            uploadcom.putfilesmall(item.id, drive_id, filePath, fileName, remotePath)
    target_filename = filePath + fileName
    os.remove(target_filename)  # 删除文件
    taskModels.uploads_list.update({"id": task_id, "status":1}) # 更新任务状态





if __name__ =='__main__':
    task_id = sys.argv[1]  # 任务id
    drive_id = sys.argv[2]  # 驱动ID
    fileName = sys.argv[3]  # 文件名字
    remotePath = sys.argv[4]  # 上传路径
    upProcess(task_id, drive_id, fileName, remotePath)