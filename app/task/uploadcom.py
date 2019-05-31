# -*- coding:utf-8 -*-
import os, json
from app.admin.drive import models as driveModels
import requests
import config
from app import common


"""
    put Small File
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    disk_id: disk id
    drive_id: drive id
    fileName: file name
    remotePath: remote path
"""
def putfilesmall(disk_id, drive_id, filePath, fileName, remotePath, times=1):
    if int(times) > 3:
        return
    else:
        times += 1
    if remotePath == "None":
        remotePath = "/"
    data_list = driveModels.disk.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    if data_list.types == 1:
        url = config.app_url + '/v1.0/me/drive/items/root:{}/{}:/content'.format(remotePath, fileName)
    else:
        url = 'https://{}-my.sharepoint.cn/_api/v2.0/me/drive/items/root:{}/{}:/content'.format(data_list.other, remotePath, fileName)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"])}
    pull_res = requests.put(url, headers=headers, data=open(filePath + fileName, 'rb'))
    pull_res = json.loads(pull_res.text)
    if 'error' in pull_res.keys():
        common.reacquireToken(disk_id)
        return putfilesmall(disk_id, drive_id, filePath, fileName, remotePath, times)
    else:
        return pull_res


"""
    put Big File
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    disk_id: disk id
    drive_id: drive id
    fileName: file name
    remotePath: remote path
"""
def putfilebig(disk_id, drive_id, filePath, fileName, remotePath):
    crsession = CreateUploadSession(disk_id, fileName, remotePath)
    fileSize = os.path.getsize(filePath + fileName)
    length = 10 * 1024 * 1024
    offset = 0
    status = ""
    if crsession:
        while (status == ""):
            res = _uploadPart(disk_id, drive_id, filePath, fileName, fileSize, length, offset, crsession['uploadUrl'])
            if res["code"] == 2:
                offset = res['offset']
            else:
                status = 0




def CreateUploadSession(disk_id, fileName, remotePath):
    if remotePath == "None":
        remotePath = "/"
    data_list = driveModels.disk.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    if data_list.types == 1:
        url = config.app_url + '/v1.0/me/drive/root:{}/{}:/createUploadSession'.format(remotePath,fileName)
    else:
        url = 'https://{}-my.sharepoint.cn/_api/v2.0/me/drive/root:{}/{}:/createUploadSession'.format(data_list.other, remotePath, fileName)
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
    drive_id: drive id
    filesize: file size
    length: 
    offset: 
    uploadUrl: upload url
"""
def _uploadPart(disk_id, drive_id, filePath, fileName, filesize, length, offset, uploadUrl='', trytime=1):
    length = int(length) if int(offset) + int(length) < filesize else filesize - int(offset)
    endpos = int(offset) + length - 1 if int(offset) + length < filesize else filesize - 1
    data = _file_seek(drive_id, filePath, fileName, offset, length)
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
def _file_seek(dirve_id, filePath, fileName, startlength, length):
    filePath = filePath + fileName
    startlength = int(startlength) if startlength == "0" else startlength
    with open(filePath, 'rb') as f:
        f.seek(int(startlength))
        content = f.read(length)
    return content