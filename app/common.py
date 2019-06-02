# -*- coding:utf-8 -*-
import importlib
import datetime, os, time, requests, json, math
import functools
from flask import redirect, session, render_template
from app import MongoDB
from socketIO_client import SocketIO, BaseNamespace
import hashlib, subprocess
from app.admin.system import models as systemModels
from app.admin.hooks import models as hooksModels
from app.admin.model import models as modelModels
from app.admin.plugin import models as pluginModels
from app.admin.drive import models as driveModels, logic as driveLogic
import config


"""
    版本信息
"""
SystemInfo = {
    "name": "CuteOne",
    "versionType": "Free",
    "versions": "3.0.5",
    "server": ""
}




"""
    公共方法
    
"""

"""
    权限修饰器
    定义一个装饰器用于拦截用户登录
    func是使用该修饰符的地方是视图函数
    @Time: 2019-03-16
"""
def login_require(func):
    @functools.wraps(func)  #自定义python装饰器时一定要使用@functools.wraps(func)修饰wrapper
    def decorator(*args,**kwargs):
        #获取session
        is_login = session.get('is_login')
        #判断用户名等于admin
        if is_login:
            return func(*args,**kwargs)
        else:
            #如果没有就重定向到登录页面
            return redirect("admin/index/login")
    return decorator


"""
    模块、插件 是否开启修饰器
"""
def mq_require(func):
    print(1)



"""
    加密密码
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    data: 明文密码
"""
def hashPwd(data):
    pwd_temp = hashlib.sha1(data.encode('utf-8')).hexdigest()
    pwd_temp = hashlib.md5(("cuteone" + pwd_temp).encode('utf-8')).hexdigest()
    return pwd_temp


"""
    UTC时间转本地时间（+8: 00）
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
"""
def utc_to_local(utc):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utcTime = datetime.datetime.strptime(utc, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    return localtime


"""
    b转KB MB 尺寸转换
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
"""
def size_cov(size):
    if size / (1024 * 1024 *1024) >= 1:
        size = str(round(size / (1024 * 1024 * 1024), 2)) + " G"
    elif size / (1024 * 1024) >= 1:
        size = str(round(size / (1024 * 1024), 2)) + " MB"
    else:
        size = str(round(size / 1024, 2)) + " KB"
    return size


"""
    执行shell指令
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    command: shell指令
"""
def run_command(command):
    subprocess.Popen(command, shell=True)


"""
    判断进程是否存在
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
"""
def isRunning(process_name):
    try:
        process = len(os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines())
        if process >= 1:
            return 1
        else:
            return
    except:
        return


"""
    获取域名
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-17
"""
def get_web_site():
    return systemModels.config.get_web_site()


"""
    Socket 通知
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-04
    id: ID
    msg: 内容
"""
def send_socket(id, msg):
    socket = SocketIO('127.0.0.1', 5000)
    chat = socket.define(BaseNamespace, '/websocket')
    chat.emit('synProcessEvent', {'data': {'id': id, 'msg': msg}})
    data = {
        "drive_id": id,
        "type": "syn",
        "content": msg
    }
    add_log(data)


"""
    日志操作
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-04
    data: { "drive_id": id, "type": "syn", "content": msg}
"""
def add_log(data):
    collection = MongoDB.db["log"]
    dic = data
    dic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S')
    collection.insert_one(dic)


"""
    restart web
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-02
"""
def restart():
    command = "python3 {}/app/task/restart.py".format(os.getcwd())
    run_command(command)


"""
    获取驱动列表
"""
def get_drive_list():
    drive_list = driveModels.drive.all()
    return drive_list


"""
    获取指定驱动的网盘列表
"""
def find_drive_disk_list(drive_id):
    disk_list = driveModels.disk.find_by_drive_id(drive_id)
    return disk_list


"""
    获取指定驱动的主盘信息
"""
def find_drive_chief(drive_id):
    chief = driveModels.disk.find_by_chief(drive_id)
    return chief


"""
    OneDrive 重新获取token
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    id: 网盘ID
"""
def reacquireToken(id):
    data_list = driveModels.disk.find_by_id(id)
    token = json.loads(json.loads(data_list.token))
    redirect_url = "https://127.0.0.1/auth"
    ReFreshData = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = ReFreshData.format(client_id = data_list.client_id, redirect_uri = redirect_url, client_secret = data_list.client_secret,
                              refresh_token = token["refresh_token"])
    if data_list.types == 1:
        url = config.BaseAuthUrl + '/common/oauth2/v2.0/token'
    else:
        url = config.ChinaAuthUrl + '/common/oauth2/token'
        data = "{}&resource=https://{}-my.sharepoint.cn/".format(data, data_list.other)
    res = requests.post(url, data=data, headers=headers)
    driveModels.disk.update({"id": id, "token": json.dumps(res.text)}) # 更新数据库的Token
    return res.text


"""
    get_model_info  获取模型信息
    name    模型名称
"""
def get_model_info(name):
    return modelModels.model.find_by_name(name)

"""
    更新模型信息
    value   是个list
"""
def updete_model_info(value):
    modelModels.model.update_by_name(value)


"""
    get_plugin_info  获取插件信息
    name    模型名称
"""
def get_plugin_info(name):
    return pluginModels.plugin.find_by_name(name)

"""
    更新插件信息
    value   是个list
"""
def updete_plugin_info(value):
    pluginModels.plugin.update_by_name(value)


"""
    获取钩子信息
    name   是个list
"""
def get_hooks_info(name):
    data_list = hooksModels.hooks.find_by_title(name)
    return data_list

"""
    Hooks 钩子渲染
    position： 位置
    公共位置：
        registered  注册钩子
        slide   幻灯钩子
        global  全局钩子
"""
def hooks(position):
    try:
        data_list = hooksModels.hooks.find_by_position(position)
        html_res = ""
        for i in data_list:
            if i.type == 0:
                result = importlib.import_module("app.model." + i.source + ".hook")
            else:
                result = importlib.import_module("app.plugin." + i.source + ".hook")
            html_res += getattr(result, i.method)()
        return html_res
    except Exception as e:
        print("钩子渲染出现错误：{}".format(e))
        print("钩子渲染出现错误：" + position)
        pass


"""
    Hooks 钩子方法，给数据钩子，调钩子方法
    types 钩子类型 model or plugin
    name 钩子名称 
    method  钩子方法
    kwargs 参数
"""
def hooks_give(types, name, method, **kwargs):
    try:
        if types == "model":
            result = importlib.import_module("app.model." + name + ".hook")
        else:
            result = importlib.import_module("app.plugin." + name + ".hook")
        return getattr(result, method)(**kwargs)
    except Exception as e:
        print("钩子调用出现错误：类型|{}，名称|{}，方法|{}，参数|kwargs".format(types, name, method, kwargs))
        pass



# 错误提示回调
def error_tip(value):
    return render_template('error/error.html', data=value), 500


"""
    types: model为模块，plugin为插件;
    name: 名称
    position: admin为后台，front为前台;
    themes_path: 模板路径；
    kwargs: 参数变量；
    @Time: 2019-5-22
"""
# 定义模板渲染
def themes_rendering(types, name, position, themes_path, **kwargs):
    if types == "model":    # 模型
        if position == "admin":
            try:
                themes_path = "model/{}/admin/{}".format(name, themes_path)
                return render_template(themes_path, **kwargs)
            except Exception as e:
                return error_tip("模板不存在！")
        else:
            try:
                # 优先渲染主题文件夹里的模板
                THEMES = "themes/{}/{}/{}".format(config.THEMES, name, themes_path)
                if os.path.isfile("{}/app/templates/{}".format(os.getcwd(), THEMES)):
                    return render_template(THEMES, **kwargs)
                else:
                    # 主题文件不存在模板，则渲染默认模板
                    themes_path = "model/{}/front/{}".format(name, themes_path)
                    if os.path.isfile("{}/app/templates/{}".format(os.getcwd(), themes_path)):
                        return render_template(themes_path, **kwargs)
                    else:
                        return error_tip("模板不存在！")
            except Exception as e:
                return error_tip(e)
    else:   # 插件
        if position == "admin":
            try:
                themes_path = "plugin/{}/admin/{}".format(name, themes_path)
                return render_template(themes_path, **kwargs)
            except Exception as e:
                return error_tip("模板不存在！")
        else:
            try:  # 优先渲染主题文件夹里的模板
                THEMES = "themes/{}/{}/{}".format(config.THEMES, name, themes_path)
                if os.path.isfile("{}/app/templates/{}".format(os.getcwd(), THEMES)):
                    return render_template(THEMES, **kwargs)
                else:
                    # 主题文件不存在模板，则渲染默认模板
                    themes_path = "plugin/{}/front/{}".format(name, themes_path)
                    if os.path.isfile("{}/app/templates/{}".format(os.getcwd(), themes_path)):
                        return render_template(themes_path, **kwargs)
                    else:
                        return error_tip("模板不存在！")
            except Exception as e:
                return error_tip(e)


"""
    公共分页方法函数
    count：全部数据
    limit：条数
    offset：页码
    items：当前页数据
"""
def paginates(count, limit, offset, items):
    all_page = list(range(1, math.ceil(count/limit)+1))
    if len(all_page) > 7:
        if offset > 5:
            if offset+3 >= math.ceil(count / limit):
                if offset-3 >= math.ceil(count / limit):
                    all_page = [1, "...", offset, offset+1, offset+2, math.ceil(count / limit)]
                else:
                    all_page = [1]
                    all_page.append("...")
                    all_page.extend(list(range(offset-1, math.ceil(count/limit)+1)))
            else:
                all_page = [1, "...", offset - 1, offset, offset + 1, offset + 2, offset + 3, "...", math.ceil(count / limit)]

        else:
            all_page = list(range(1, 7))
            all_page.append("...")
            all_page.append(math.ceil(count / limit))
    else:
        all_page = list(range(1, math.ceil(count / limit) + 1))
    return {"data": items, "pagination": {"count": count, "page": all_page, "now_page": offset}}


"""
    获取文件缓存下载地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-5-31
    drive_id: 驱动id
    disk_id: 网盘id
    res_id: 资源id
"""
def file_real_url(drive_id, disk_id, id):
    drivename = "disk_" + str(disk_id)
    collection = MongoDB.db[drivename]
    result = collection.find_one({"id": id})
    if result:
        if int(result["timeout"]) <= int(time.time()):
            get_res = get_downloadUrl(drive_id, disk_id, id)
            return {"name": get_res["name"], "url": get_res["downloadUrl"]}
        else:
            return {"name": result["name"], "url": result["downloadUrl"]}
    else:
        get_res = get_downloadUrl(drive_id, disk_id, id)
        return {"name": get_res["name"], "url": get_res["downloadUrl"]}


"""
    从新拉取真实地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-5-31
    drive_id: 驱动id
    disk_id: 网盘id
    res_id: 资源id
"""
def get_downloadUrl(drive_id, disk_id, id):
    data_list = driveModels.disk.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    if data_list.types == 1:
        BaseUrl = "{}v1.0/me/drive/items/{}".format(config.app_url, id)
    else:
        BaseUrl = "https://{}-my.sharepoint.cn/_api/v2.0/me/drive/items/{}".format(data_list.other, id)
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    get_res = requests.get(BaseUrl, headers=headers, timeout=30)
    get_res = json.loads(get_res.text)
    if 'error' in get_res.keys():
        reacquireToken(disk_id)
        return get_downloadUrl(drive_id, disk_id, id)
    else:
        if '@microsoft.graph.downloadUrl' in get_res.keys():
            downloadUrl = get_res["@microsoft.graph.downloadUrl"]
        else :
            downloadUrl = get_res["@content.downloadUrl"]
        drivename = "disk_" + str(disk_id)
        collection = MongoDB.db[drivename]
        result = collection.find_one({"id": get_res["id"]})
        if result:
            collection.update_one({"id":get_res["id"]}, {"$set": {"downloadUrl":downloadUrl,"timeout":int(time.time())+300}})
        else:
            dic = {
                "id": get_res["id"],
                "parentReference": get_res["parentReference"]["id"],
                "name": get_res["name"],
                "file": get_res["file"]["mimeType"],
                "path": get_res["parentReference"]["path"].replace("/drive/root:", ""),
                "size": get_res["size"],
                "createdDateTime": utc_to_local(get_res["fileSystemInfo"]["createdDateTime"]),
                "lastModifiedDateTime": utc_to_local(get_res["fileSystemInfo"]["lastModifiedDateTime"]),
                "downloadUrl": downloadUrl,
                "timeout": int(time.time()) + 300
            }
            collection.insert_one(dic)
        return {"name": get_res["name"], "downloadUrl": downloadUrl}