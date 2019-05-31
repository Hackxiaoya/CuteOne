# -*- coding:utf-8 -*-
import os, json, requests, threading
from app import MongoDB
from ... import common
import config
from ..drive import models




"""
    获取OneDrive文件列表
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    token: 网盘ID
    path: 路径，如果为空则从根目录获取，否则从路径获取
"""
def get_one_file_list(id, path=''):
    data_list = models.disk.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    if data_list.types == 1:
        app_url = config.app_url+"/v1.0/me/drive"
    else:
        app_url = "https://{}-my.sharepoint.cn/_api/v2.0/me/drive".format(data_list.other)
    if path:
        BaseUrl = app_url + '/root:{}:/children?expand=thumbnails'.format(path)
    else:
        BaseUrl = app_url + '/root/children?expand=thumbnails'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(token["access_token"])}
    try:
        get_res = requests.get(BaseUrl, headers=headers, timeout=30)
        get_res = json.loads(get_res.text)
        if 'error' in get_res.keys():
            common.reacquireToken(id)
            return get_one_file_list(id, path)
        else:
            if 'value' in get_res.keys():
                result = get_res['value']
                if '@odata.nextLink' in get_res.keys():
                    pageres = get_one_file_list_page(token, get_res["@odata.nextLink"])
                    result+=pageres

                # 处理世纪互联的地址
                if data_list.types == 2:
                    for r in result:
                        if "folder" not in r:
                            r["thumbnails"].append({"large":{"url":r["@content.downloadUrl"]}})
                return {'code': True, 'msg': '获取成功', 'data': result}
            else:
                return get_one_file_list(id, path)
    except Exception as e:
        return {'code': False, 'msg': e, 'data': ''}
        pass
        # return get_one_file_list(id, path)


"""
    获取OneDrive文件列表 - 超过200个文件，分页获取
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    token: 网盘ID
    url: 分页url
"""
def get_one_file_list_page(token, url, total=[]):
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    get_res = requests.get(url, headers=headers, timeout=30)
    get_res = json.loads(get_res.text)
    if 'value' in get_res.keys():
        total += get_res['value']
        if '@odata.nextLink' in get_res.keys():
            get_one_file_list_page(token, get_res["@odata.nextLink"], total)
        return total



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
    data_list = models.disk.find_by_id(id)
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
        common.reacquireToken(id)
        return folder_create(id, path, fileName)
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
    data_list = models.disk.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    url = config.app_url + '/v1.0/me/drive/items/{}'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"]), 'Content-Type': 'application/json'}
    payload = {
        "name": new_name
    }
    get_res = requests.patch(url, headers=headers, data=json.dumps(payload))
    get_res = json.loads(get_res.text)
    if 'error' in get_res.keys():
        common.reacquireToken(id)
        return rename_files(id, fileid, new_name)
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
    data_list = models.disk.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    url = config.app_url + '/v1.0/me/drive/items/{}'.format(fileid)
    headers = {'Authorization': 'bearer {}'.format(token["access_token"]), 'Content-Type': 'application/json'}
    get_res = requests.delete(url, headers=headers)
    if get_res.status_code == 204:
        return {'code': True, 'msg': '成功', 'data':''}
    else:
        common.reacquireToken(id)
        return delete_files(id, fileid)


"""
    MongoDB 更新缓存
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    drive_id: 驱动ID
    type: 更新类型，all全部，dif差异
"""
def update_cache(drive_id, type):
    driveinfo = models.disk.find_by_drive_id(drive_id)
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
    command = "python3 {}/app/task/uploads.py {} {} '{}' '{}'".format(os.getcwd(), task_id, drive_id, fileName, remotePath)
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
    重载指定ID的同步任务
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    id: 驱动ID
"""
def reStartSynTask(id):
    try:
        drivename = "syn_drive_" + str(id)
        MongoDB.db[drivename].remove()  # 移除集合所有数据
        MongoDB.db[drivename].drop()  # 删除集合
        return
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
