# -*- coding:utf-8 -*-
import time, json, requests, os
import config
from app import MongoDB
from app.admin.users import models as usersModels
from app.admin.author import models as authorModels
from app.admin.files import models as filesModels
from app.admin.drive import logic as driveLogic
from ... import common





"""
    获取用户列表
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-06
    page: 页码
    limit: 条数
"""
def get_users_list(page="1", limit="12"):
    result = usersModels.users.get_pages(page, limit)
    for item in result:
        if item.group == 0:
            item.group = "普通会员"
        else:
            item.group = authorModels.authGroup.find_by_id(item.group).title
    return result


"""
    获取用户文件列表
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    uid: uid
    page: 页码
    limit: 条数
"""
def get_users_files_list(uid, page="1", limit="50"):
    result = filesModels.files.get_pages(uid, page, limit)
    return result


"""
    OneDrive 重新获取token
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    id: 网盘ID
"""
def reacquireToken(id):
    data_list = filesModels.filesDisk.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    redirect_url = "http://127.0.0.1/"
    ReFreshData = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = ReFreshData.format(client_id = data_list.client_id, redirect_uri = redirect_url, client_secret = data_list.client_secret,
                              refresh_token = token["refresh_token"])
    url = config.BaseAuthUrl+'/common/oauth2/v2.0/token'
    res = requests.post(url, data=data, headers=headers)
    filesModels.filesDisk.update({"id": id, "token": json.dumps(res.text)}) # 更新数据库的Token
    return res.text

"""
    获取文件下载地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    uid: 驱动id
    disk_id: 网盘id
    files_id: 资源id
"""
def file_url(uid, disk_id, files_id):
    drivename = "files_disk_" + str(disk_id)
    collection = MongoDB.db[drivename]
    result = collection.find_one({"id": files_id})
    if int(result["timeout"]) <= int(time.time()):
        get_res = get_downloadUrl(uid, disk_id, files_id)
        return {"name": get_res["name"], "url": get_res["downloadUrl"]}
    else:
        return {"name": result["name"], "url": result["downloadUrl"]}

"""
    获取数据真实地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    uid: 驱动id
    disk_id: 网盘id
    files_id: 资源id
"""
def get_downloadUrl(uid, disk_id, files_id):
    data_list = filesModels.filesDisk.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    BaseUrl = config.app_url + 'v1.0/me/drive/items/' + files_id
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    get_res = requests.get(BaseUrl, headers=headers, timeout=30)
    get_res = json.loads(get_res.text)
    if 'error' in get_res.keys():
        reacquireToken(disk_id)
        get_downloadUrl(uid, disk_id, files_id)
    else:
        if '@microsoft.graph.downloadUrl' in get_res.keys():
            drivename = "files_disk_" + str(disk_id)
            collection = MongoDB.db[drivename]
            collection.update_one({"id":get_res["id"]}, {"$set": {"downloadUrl":get_res["@microsoft.graph.downloadUrl"],"timeout":int(time.time())+300}})
            return {"name": get_res["name"], "downloadUrl": get_res["@microsoft.graph.downloadUrl"]}
        else:
            get_downloadUrl(uid, disk_id, files_id)


"""
    推送上传任务
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-07
    id: file id
    uid: uid
    files_disk_id: files_disk_id
    fileName: 文件名称
    remotePath: 远程路径
"""
def pull_uploads(id, uid, files_disk_id, fileName, remotePath):
    command = "python3 {}/app/task/usersFilesUploads.py {} {} {} '{}' '{}'".format(os.getcwd(), id, uid, files_disk_id, fileName, remotePath)
    common.run_command(command)