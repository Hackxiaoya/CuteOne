# -*- coding:utf-8 -*-
import os, json, requests
from . import models
import config



"""
    OneDrive 重新获取token
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    id: 网盘ID
"""
def reacquireToken(id):
    data_list = models.filesDisk.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    redirect_url = "http://127.0.0.1/"
    ReFreshData = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = ReFreshData.format(client_id = data_list.client_id, redirect_uri = redirect_url, client_secret = data_list.client_secret,
                              refresh_token = token["refresh_token"])
    url = config.BaseAuthUrl+'/common/oauth2/v2.0/token'
    res = requests.post(url, data=data, headers=headers)
    models.filesDisk.update({"id": id, "token": json.dumps(res.text)}) # 更新数据库的Token
    return res.text


"""
    获取OneDrive文件列表
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-06
    token: 网盘ID
    path: 路径，如果为空则从根目录获取，否则从路径获取
"""
def get_one_file_list(id, path=''):
    data_list = models.filesDisk.find_by_id(id)
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