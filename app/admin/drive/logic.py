# -*- coding:utf-8 -*-
import os, sys, json, requests, threading
from app import MongoDB
from ... import common
import config
from ..drive import models

"""
    OneDrive 重新获取token
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    id: 网盘ID
"""
def reacquireToken(id):
    data_list = models.drive_list.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    redirect_url = "http://127.0.0.1/"
    ReFreshData = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = ReFreshData.format(client_id = data_list.client_id, redirect_uri = redirect_url, client_secret = data_list.client_secret,
                              refresh_token = token["refresh_token"])
    url = config.BaseAuthUrl+'/common/oauth2/v2.0/token'
    res = requests.post(url, data=data, headers=headers)
    models.drive_list.update({"id": id, "token": json.dumps(res.text)}) # 更新数据库的Token
    return res.text


"""
    获取OneDrive文件列表
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    token: 网盘ID
    path: 路径，如果为空则从根目录获取，否则从路径获取
"""
def get_one_file_list(id, path=''):
    data_list = models.drive_list.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    if path:
        BaseUrl = config.app_url + '/v1.0/me/drive/root:{}:/children?expand=thumbnails'.format(path)
    else:
        BaseUrl = config.app_url + '/v1.0/me/drive/root/children?expand=thumbnails'
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    try:
        get_res = requests.get(BaseUrl, headers=headers, timeout=30)
        get_res = json.loads(get_res.text)
        if 'error' in get_res.keys():
            reacquireToken(id)
            get_one_file_list(id, path)
        else:
            if 'value' in get_res.keys():
                return {'code': True, 'msg': '获取成功', 'data': get_res}
            else:
                get_one_file_list(id, path)
    except:
        get_one_file_list(id, path)


"""
    OneDrive 创建文件
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    id: 网盘ID
    path: 远程路径
    fileName: 文件夹名字
"""
def folder_create(id, path, fileName):
    data_list = models.drive_list.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    if path:
        parent_id = models.mongodb_find_parent_id(id, path)
        url = config.app_url + '/v1.0/me/drive/items/{}/children'.format(parent_id)
    else:
        url = config.app_url + '/v1.0/me/drive/root/children'
    headers = {'Authorization': 'bearer {}'.format(token["access_token"]), 'Content-Type': 'application/json'}
    payload = {
        "name": fileName,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename"
    }
    get_res = requests.post(url, headers=headers, data=json.dumps(payload))
    get_res = json.loads(get_res.text)
    if 'error' in get_res.keys():
        reacquireToken(id)
        folder_create(id, parent_id, fileName)
    else:
        return {'code': True, 'msg': '成功', 'data':''}


"""
    OneDrive 重命名文件
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    id: 网盘ID
    fileid: 源文件id
    new_name: 新文件名字
"""
def rename_files(id, fileid, new_name):
    data_list = models.drive_list.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    url = config.app_url + '/v1.0/me/drive/items/{}'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"]), 'Content-Type': 'application/json'}
    payload = {
        "name": new_name
    }
    get_res = requests.patch(url, headers=headers, data=json.dumps(payload))
    get_res = json.loads(get_res.text)
    if 'error' in get_res.keys():
        reacquireToken(id)
        rename_files(id, fileid, new_name)
    else:
        return {'code': True, 'msg': '成功', 'data':''}


"""
    OneDrive 删除文件
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    id: 网盘ID
    fileid: 源文件id
"""
def delete_files(id, fileid):
    data_list = models.drive_list.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    url = config.app_url + '/v1.0/me/drive/items/{}'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"]), 'Content-Type': 'application/json'}
    get_res = requests.delete(url, headers=headers)
    if get_res.status_code == 204:
        return {'code': True, 'msg': '成功', 'data':''}
    else:
        reacquireToken(id)
        delete_files(id, fileid)


"""
    MongoDB 更新缓存
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    drive_id: 驱动ID
    type: 更新类型，all全部，dif差异
"""
def update_cache(drive_id, type):
    driveinfo = models.drive_list.find_by_drive_id(drive_id)
    threads = []
    for i in driveinfo:
        command = "python3 {}/app/task/cuteTask.py {} {}".format(os.getcwd(), i.id, type)  # 后台任务文件路
        t = threading.Thread(target=common.run_command, args=(command,))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()


"""
    推送上传任务
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    task_id: 任务id
    drive_id: 驱动id
    fileName: 文件名称
    remotePath: 远程路径
"""
def pull_uploads(task_id, drive_id, fileName, remotePath):
    command = "python3 {}/app/task/uploads.py {} {} '{}' {}".format(os.getcwd(), task_id, drive_id, fileName, remotePath)
    common.run_command(command)




"""
    推送主从同步任务
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    drive_id: 驱动id
"""
def startSynTask(drive_id):
    command = "python3 {}/app/task/syn/syn.py {}".format(os.getcwd(), drive_id)
    common.run_command(command)


"""
    判断是否有同步任务未完成
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    drive_id: 驱动id
"""
def ifSynTask(drive_id):
    drivename = "syn_drive_" + str(drive_id)
    collectionList = MongoDB.db.list_collection_names()
    if drivename in collectionList:  # 如果存在集合
        return True
    else:
        return False


"""
    检查是否有指定ID的主从同步进程
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    id: 驱动ID
"""
def isSynTask(id):
    try:
        command = "ps -ef | grep 'python3 {}/app/task/syn/syn.py {}' | grep -v grep | wc -l".format(os.getcwd(), id)
        process = os.popen(command).read()
        if process[0:1] == "0":
            return False
        else:
            return True
    except:
        return

"""
    强制结束指定ID的主从同步进程
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    id: 驱动ID
"""
def stopSynTask(id):
    try:
        pid = os.popen("ps -ef | grep 'python3 " + os.getcwd() + "/app/task/syn/syn.py " + str(id) + "' | grep -v grep |awk '{print $2}'").read()
        os.popen("kill -9 " + str(pid))
        return
    except:
        return
