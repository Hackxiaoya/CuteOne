# -*- coding:utf-8 -*-
import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app import MongoDB
from app.admin.drive import models as driveModels
from app import common
from app.task import uploadcom

"""
    推送脚本
"""

"""
    推送任务
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    drive_id: 驱动id
    fileName: 文件名称
    remotePath: 远程路径
"""
def upProcess(drive_id, fileName, remotePath):
    data_list = driveModels.disk.find_by_drive_id(drive_id)
    collection = MongoDB.db["syn_drive_" + str(drive_id)]
    filesize = os.path.getsize(os.getcwd() + "/temp_uploads/syn_temp/" + str(drive_id) + "/" + fileName)
    filePath = os.getcwd() + "/temp_uploads/syn_temp/" + str(drive_id) + "/"
    for item in data_list:
        if int(item.chief) == 0:
            dbRes = collection.find_one({"name": fileName, "path": remotePath})
            if str(item.id) in dbRes["syn_disk"]:
                common.send_socket(drive_id, "{} | 开始同步 {} 到 [ {} ] 网盘".format(time.strftime('%Y-%m-%d %H:%M:%S'), fileName, item.title))
                if filesize > 4194304:
                    res = uploadcom.putfilebig(item.id, drive_id, filePath, fileName, remotePath)
                else:
                    res = uploadcom.putfilesmall(item.id, drive_id, filePath, fileName, remotePath)
                common.send_socket(drive_id, "{} | 同步 {} 到 [ {} ] 网盘完成".format(time.strftime('%Y-%m-%d %H:%M:%S'), fileName, item.title))
    common.send_socket(drive_id, "{} | {} 所有网盘同步完成，删除缓存文件".format(time.strftime('%Y-%m-%d %H:%M:%S'), fileName))
    target_filename = filePath + fileName
    os.remove(target_filename)  # 删除文件