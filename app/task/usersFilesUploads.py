# -*- coding:utf-8 -*-
import os, sys, json, threading, time
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app import MongoDB, common
from app.admin.files import models as filesModels
from app.main.users import logic as usersLogic
import requests
import config

"""
    推送脚本
"""

"""
    推送任务
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    id: file id
    uid: uid
    files_disk_id: files disk id
    fileName: 文件名称
    remotePath: 远程路径
"""
def upProcess(id, uid, files_disk_id, fileName, remotePath):
    drivename = "files_disk_" + str(files_disk_id)
    collection = MongoDB.db[drivename]
    filesize = os.path.getsize(os.getcwd() + "/temp_uploads/users_files_temp/" + str(files_disk_id) + "/" + str(uid) + "/" + fileName)
    if filesize > 4194304:
        res = putfilebig(id, uid, files_disk_id, fileName, remotePath)
        dic = {
            "id": res["id"],
            "parentReference": res["parentReference"]["id"],
            "name": res["name"],
            "file": "folder",
            "path": res["parentReference"]["path"].replace("/drive/root:", ""),
            "size": res["size"],
            "createdDateTime": common.utc_to_local(res["fileSystemInfo"]["createdDateTime"]),
            "lastModifiedDateTime": common.utc_to_local(res["fileSystemInfo"]["lastModifiedDateTime"]),
            "downloadUrl": res["@content.downloadUrl"],
            "timeout": int(time.time()) + 300
        }
    else:
        res = putfilesmall(id, uid, files_disk_id, fileName, remotePath)
        dic = {
            "id": res["id"],
            "parentReference": res["parentReference"]["id"],
            "name": res["name"],
            "file": "folder",
            "path": res["parentReference"]["path"].replace("/drive/root:", ""),
            "size": res["size"],
            "createdDateTime": common.utc_to_local(res["fileSystemInfo"]["createdDateTime"]),
            "lastModifiedDateTime": common.utc_to_local(res["fileSystemInfo"]["lastModifiedDateTime"]),
            "downloadUrl": res["@microsoft.graph.downloadUrl"],
            "timeout": int(time.time()) + 300
        }
    collection.insert_one(dic)

    target_filename = os.getcwd()+"/temp_uploads/users_files_temp/" + str(files_disk_id) + "/" + str(uid) + "/" + fileName
    os.remove(target_filename)  # 删除文件
    updateres = {"id":id, "file":res["file"]["mimeType"], "size":res["size"], "files_id":res["id"], "status":1}
    filesModels.files.update(updateres) # 更新任务状态


"""
    put Small File
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    id: file id
    uid: uid
    files_disk_id: files disk id
    fileName: 文件名称
    remotePath: 远程路径
"""
def putfilesmall(id, uid, files_disk_id, fileName, remotePath, times=1):
    if int(times) > 3:
        return
    else:
        times += 1
    if remotePath == "None":
        remotePath = "/"
    data_list = filesModels.filesDisk.find_by_id(files_disk_id)
    token = json.loads(json.loads(data_list.token))
    url = config.app_url + '/v1.0/me/drive/items/root:/{}/{}/{}:/content'.format(uid, remotePath, fileName)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"])}
    pull_res = requests.put(url, headers=headers, data=open(os.getcwd()+"/temp_uploads/users_files_temp/" + str(files_disk_id) + "/" + str(uid) + "/" + fileName, 'rb'))
    pull_res = json.loads(pull_res.text)
    if 'error' in pull_res.keys():
        usersLogic.reacquireToken(files_disk_id)
        putfilesmall(id, uid, files_disk_id, fileName, remotePath, times)
    else:
        return pull_res


"""
    put Big File
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    id: file id
    uid: uid
    files_disk_id: files disk id
    fileName: 文件名称
    remotePath: 远程路径
"""
def putfilebig(id, uid, files_disk_id, fileName, remotePath):
    crsession = CreateUploadSession(files_disk_id, fileName, remotePath)
    filesize = os.path.getsize(os.getcwd() + "/temp_uploads/users_files_temp/" + str(files_disk_id) + "/" + str(uid) + "/" + fileName)
    length = 10 * 1024 * 1024
    offset = 0
    status = ""
    if crsession:
        while (status == ""):
            res = _uploadPart(uid, files_disk_id, fileName, filesize, length, offset, crsession['uploadUrl'])
            if res["code"] == 2:
                offset = res['offset']
            else:
                status = 0
                return res['data']




def CreateUploadSession(files_disk_id, fileName, remotePath):
    if remotePath == "None":
        remotePath = "/"
    data_list = filesModels.filesDisk.find_by_id(files_disk_id)
    token = json.loads(json.loads(data_list.token))
    url = config.app_url + '/v1.0/me/drive/root:/{}/{}/{}:/createUploadSession'.format(uid, remotePath,fileName)
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
                usersLogic.reacquireToken(files_disk_id)
                CreateUploadSession(files_disk_id, fileName, remotePath)
            else:
                return pull_res
    except Exception as e:
        return False



"""
    upload Part
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    uid: uid
    files_disk_id: files_disk_id
    filesize: file size
    length: 
    offset: 
    uploadUrl: upload url
"""
def _uploadPart(uid, files_disk_id, fileName, filesize, length, offset, uploadUrl='', trytime=1):
    length = int(length) if int(offset) + int(length) < filesize else filesize - int(offset)
    endpos = int(offset) + length - 1 if int(offset) + length < filesize else filesize - 1
    data = _file_seek(uid, files_disk_id, fileName, offset, length)
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
        return {"code": 0, "data": json.loads(pull_res.text)}



"""
    file seek
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-01
    uid: dirve id
    files_disk_id: files_disk_id
    fileName: file name
    filesize: file size
    startlength: start 
    length: 
"""
def _file_seek(uid, files_disk_id, fileName, startlength, length):
    filePath = os.getcwd()+"/temp_uploads/users_files_temp/" + str(files_disk_id) + "/" + str(uid) + "/" + fileName
    startlength = int(startlength) if startlength == "0" else startlength
    with open(filePath, 'rb') as f:
        f.seek(int(startlength))
        content = f.read(length)
    return content



if __name__ =='__main__':
    id = sys.argv[1]  # file id
    uid = sys.argv[2]  # uid
    files_disk_id = sys.argv[3]  # files_disk_id
    fileName = sys.argv[4]  # 文件名字
    remotePath = sys.argv[5]  # 上传路径
    upProcess(id, uid, files_disk_id, fileName, remotePath)