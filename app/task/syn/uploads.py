# -*- coding:utf-8 -*-
import os, sys, json, threading, time
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app import MongoDB
from app.admin.drive import models as driveModels
from app.admin.drive import logic as driveLogic
import requests
import config
from app import common

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
    for item in data_list:
        if item.chief == "0":
            dbRes = collection.find_one({"name": fileName, "path": remotePath})
            if str(item.id) in dbRes["syn_disk"]:
                common.send_socket(drive_id, "{} | 开始同步 {} 到 [ {} ] 网盘".format(time.strftime('%Y-%m-%d %H:%M:%S'), fileName, item.title))
                if item.chief == "0":
                    filesize = os.path.getsize(os.getcwd() + "/temp_uploads/syn_temp/" + str(drive_id) + "/" + fileName)
                    if filesize > 4194304:
                        res = putfilebig(item.id, drive_id, fileName, remotePath)
                    else:
                        res = putfilesmall(item.id, drive_id, fileName, remotePath)
                common.send_socket(drive_id, "{} | 同步 {} 到 [ {} ] 网盘完成".format(time.strftime('%Y-%m-%d %H:%M:%S'), fileName, item.title))
    common.send_socket(drive_id, "{} | {} 所有网盘同步完成，删除缓存文件".format(time.strftime('%Y-%m-%d %H:%M:%S'), fileName))
    target_filename = os.getcwd()+"/temp_uploads/syn_temp/" + str(drive_id) + "/" + fileName
    os.remove(target_filename)  # 删除文件



"""
    put Small File
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    disk_id: disk id
    dirve_id: dirve id
    fileName: file name
    remotePath: remote path
"""
def putfilesmall(disk_id, dirve_id, fileName, remotePath):
    if remotePath == "None":
        remotePath = "/"
    data_list = driveModels.disk.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    if data_list.types == 1:
        app_url = config.app_url
    else:
        app_url = config.China_app_url
    url = app_url + '/v1.0/me/drive/items/root:{}/{}:/content'.format(remotePath, fileName)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"])}
    pull_res = requests.put(url, headers=headers, data=open(os.getcwd()+"/temp_uploads/syn_temp/" + str(dirve_id) + "/" + fileName, 'rb'))
    pull_res = json.loads(pull_res.text)
    if 'error' in pull_res.keys():
        common.reacquireToken(disk_id)
        putfilesmall(disk_id, dirve_id, fileName, remotePath)
        return True
    # print("putfilesmall: {}".format(pull_res))


"""
    put Big File
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    disk_id: disk id
    dirve_id: dirve id
    fileName: file name
    remotePath: remote path
"""
def putfilebig(disk_id, dirve_id, fileName, remotePath):
    crsession = CreateUploadSession(disk_id, fileName, remotePath)
    filesize = os.path.getsize(os.getcwd() + "/temp_uploads/syn_temp/" + str(dirve_id) + "/" + fileName)
    length = 10 * 1024 * 1024
    offset = 0
    status = ""
    if crsession:
        while (status == ""):
            res = _uploadPart(disk_id, dirve_id, fileName, filesize, length, offset, crsession['uploadUrl'])
            if res["code"] == 2:
                offset = res['offset']
            else:
                status = 0

    # print("putfilebig: {}".format(fileName))
    return True




def CreateUploadSession(disk_id, fileName, remotePath):
    if remotePath == "None":
        remotePath = "/"
    data_list = driveModels.disk.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    if data_list.types == 1:
        app_url = config.app_url
    else:
        app_url = config.China_app_url
    url = app_url + '/v1.0/me/drive/root:{}/{}:/createUploadSession'.format(remotePath,fileName)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"]), 'Content-Type': 'application/json'}
    data = {
        "item": {
            "@microsoft.graph.conflictBehavior": "fail",
        }
    }
    try:
        pull_res = requests.post(url, headers=headers, data=json.dumps(data))
        if pull_res.status_code == 409:
            return False
        else:
            pull_res = json.loads(pull_res.text)
            if 'error' in pull_res.keys():
                common.reacquireToken(disk_id)
                return CreateUploadSession(disk_id, fileName, remotePath)
            else:
                    return pull_res
    except Exception as e:
        return False



"""
    upload Part
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    disk_id: disk id
    dirve_id: dirve id
    filesize: file size
    length: 
    offset: 
    uploadUrl: upload url
"""
def _uploadPart(disk_id, dirve_id, fileName, filesize, length, offset, uploadUrl='', trytime=1):
    length = int(length) if int(offset) + int(length) < filesize else filesize - int(offset)
    endpos = int(offset) + length - 1 if int(offset) + length < filesize else filesize - 1
    data = _file_seek(dirve_id, fileName, offset, length)
    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(length),
        'Content-Range': 'bytes {}-{}/{}'.format(offset,endpos,filesize)
    }
    pull_res = requests.put(uploadUrl, headers=headers, data=data)
    # pull_res = json.loads(pull_res.text)
    if pull_res.status_code == 202:
        pull_res = json.loads(pull_res.text)
        offset = pull_res['nextExpectedRanges'][0].split('-')[0]
        return {"code":2, "offset":offset}
    else:
        return {"code": 0}



"""
    file seek
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    dirve_id: dirve id
    fileName: file name
    filesize: file size
    startlength: start 
    length: 
"""
def _file_seek(dirve_id, fileName, startlength, length):
    filePath = os.getcwd()+"/temp_uploads/syn_temp/" + str(dirve_id) + "/" + fileName
    startlength = int(startlength) if startlength == "0" else startlength
    with open(filePath, 'rb') as f:
        f.seek(int(startlength))
        content = f.read(length)
    return content