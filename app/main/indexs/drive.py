# -*- coding:utf-8 -*-
import re, urllib.parse, json
from app import app, common
from flask import render_template, request, make_response, redirect, session, url_for
from flask_login import current_user
from app.admin.drive import models as driveModels
from app.main import index
from ..indexs import logic
import config
THEMES = 'themes/'+ config.THEMES +'/'



# Whether there is a string
def thereisStr(str,arg):
    result = str.find(arg)
    if result > 0:
        return True
    else:
        return False

env = app.jinja_env
env.filters['thereisStr'] = thereisStr  #注册自定义过滤器


def hook(position):
    return common.hooks(position)
    # return position
app.add_template_global(hook, 'hook')



def author_judge_at():
    drive = request.args.get('drive')
    path = '' if request.args.get('path') is None else request.args.get('path')
    if drive:
        if current_user.get_id() is not None:
            return logic.author_judge(drive, current_user.id, path)
            # author = logic.author_judge(drive, 1, path)
        else:
            return logic.author_judge(drive, '', path)



# 驱动列表, 面包屑
# @index.context_processor
def drive_list(id):
    url_path = request.full_path
    drive = request.args.get('drive')
    path = request.args.get('path')
    if drive:
        drive_id = drive
    else:
        activate = driveModels.drive.find_by_id(id)
        drive_id = activate.id
    disk_list = driveModels.disk.find_by_drive_id(drive_id)
    load_disk_list = []
    for item in disk_list:
        load_disk_list.append({
            "id": item.id,
            "title": item.title
        })
    if path:
        reres = re.findall('(.+?.+)path=(.+?.+)', url_path)[0]
        crumbs_url = reres[0]
        crumbs_list = re.split('[/]', path)
        crumbs_list.pop(0)
        crumbs_list_data = []
        for i in range(len(crumbs_list)):
            crumbs_list[i] = urllib.parse.unquote(crumbs_list[i])
            name = urllib.parse.unquote(crumbs_list[i])
            if i:
                crumbs_list[i] = crumbs_list[i-1] + "/" + crumbs_list[i]

            crumbs_list_data.append({"path": crumbs_list[i], "name": name})
    else:
        crumbs_url = "/?drive={}".format(drive_id)
        crumbs_list_data = []

    return dict(crumbs_url=crumbs_url, crumbs_list_data=crumbs_list_data, load_disk_list=load_disk_list)


# 当前排序的key
@index.context_processor
def tableSort():
    sortTable = 'lastModifiedDateTime' if request.args.get('sortTable') is None else request.args.get('sortTable')
    sortType = 'more' if request.args.get('sortType') is None else request.args.get('sortType')
    return dict(sortTable=sortTable, sortType=sortType)



@index.route('/drive/')
def drive(id=0):
    drive = request.args.get('drive')
    disk = request.args.get('disk')
    path = '' if request.args.get('path') is None else request.args.get('path')
    search = request.args.get('search')
    page_number = '1' if request.args.get('page') is None else request.args.get('page')
    sortTable = 'lastModifiedDateTime' if request.args.get('sortTable') is None else request.args.get('sortTable')
    sortType = 'more' if request.args.get('sortType') is None else request.args.get('sortType')

    drive_other_info =drive_list(id)
    author = author_judge_at()
    if author:
        return render_template(THEMES + 'drive/author.html', drive_id=drive, path=path)

    # 优先进行条件查询
    if drive:
        driveurl = '/drive/?drive={}'.format(drive)
        if disk:
            disk_id = disk
            driveurl = '{}&disk={}'.format(driveurl, disk)
        else:
            disk_id = driveModels.disk.find_by_chief(drive).id
            driveurl = '{}&disk={}'.format(driveurl, disk_id)

        if path:
            data = logic.get_data(disk_id, path, search, sortTable, sortType, page_number)
            current_url = '{}&path={}'.format(driveurl, path)
        else:
            data = logic.get_data(disk_id, '', search, sortTable, sortType, page_number)
            current_url = '{}&path='.format(driveurl)
    else:
        activate = driveModels.drive.find_by_id(id)
        drive = activate.id
        disk_id = driveModels.disk.find_by_chief(activate.id).id
        data = logic.get_data(disk_id, '', search, sortTable, sortType, page_number)
        current_url = '/drive/?drive={}&disk={}&path='.format(activate.id, disk_id)
    return render_template(THEMES+'drive/index.html', activity_nav='index', drive_id=drive, disk_id=disk_id, current_url=current_url, crumbs_url=drive_other_info["crumbs_url"], crumbs_list_data=drive_other_info["crumbs_list_data"], load_disk_list=drive_other_info["load_disk_list"], data=data["data"], pagination=data["pagination"])


@index.route('/drive/video/<int:drive_id>/<int:disk_id>/<string:id>/')
@index.route('/drive/video/<int:drive_id>/<int:disk_id>/<string:id>/<int:load>/<int:source_disk_id>/<string:source_id>')
def video(drive_id, disk_id, id, load=None, source_disk_id=0, source_id=0):
    # 负载切换
    if load:
        data = logic.get_load(drive_id, disk_id, source_disk_id, source_id)
        return redirect(url_for('/.video', drive_id=drive_id, disk_id=disk_id, id=data), 301)
    else:
        data = logic.get_downloadUrl(drive_id, disk_id, id)
        share_url = "/drive/video/{}/{}/{}".format(drive_id, disk_id, id)
        donw_url = "/drive/down_file/{}/{}/{}".format(drive_id, disk_id, id)
        data["drive_id"] = drive_id
        data["disk_id"] = disk_id
        data["id"] = id
        return render_template(THEMES+'drive/video.html', share_url=share_url, donw_url=donw_url, data=data)


@index.route('/drive/get_downloadUrl/<int:drive_id>/<int:disk_id>/<string:id>')
def get_downloadUrl(drive_id, disk_id, id):
    data = logic.file_url(drive_id, disk_id, id)
    return json.dumps(data)


@index.route('/drive/pop_video/<int:drive_id>/<int:disk_id>/<string:id>/')
@index.route('/drive/pop_video/<int:drive_id>/<int:disk_id>/<string:id>/<int:load>/<int:source_disk_id>/<string:source_id>')
def pop_video(drive_id, disk_id, id, load=None, source_disk_id=0, source_id=0):
    # 负载切换
    if load:
        data = logic.get_load(drive_id, disk_id, source_disk_id, source_id)
        return redirect(url_for('/.pop_video',drive_id=drive_id, disk_id=disk_id, id=data), 301)
    else:
        data = logic.file_url(drive_id, disk_id, id)
        share_url = "/drive/video/{}/{}/{}".format(drive_id, disk_id, id)
        donw_url = "/drive/down_file/{}/{}/{}".format(drive_id, disk_id, id)
        data["drive_id"] = drive_id
        data["disk_id"] = disk_id
        data["id"] = id
        return render_template(THEMES+'drive/pop_video.html', share_url=share_url, donw_url=donw_url, data=data)


@index.route('/drive/down_file/<int:drive_id>/<int:disk_id>/<string:id>')
@index.route('/drive/down_file/<int:drive_id>/<int:disk_id>/<string:id>/')
def down_file(drive_id, disk_id, id):
    response = logic.file_url(drive_id, disk_id, id)
    data = make_response(redirect(response["url"]))
    data.headers["Content-Disposition"] = "attachment; filename={}".format(response["name"].encode().decode('latin-1'))
    return data


@index.route('/drive/approve', methods=['POST'])    # 认证密码，写入session
def approve():
    drive_id = request.form['drive_id']
    path = request.form['path']
    password = request.form['password']
    res = logic.author_password(drive_id, path, password)
    if res:
        session[path] = password
        return json.dumps({"code": 0, "msg": "密码正确！"})
    else:
        return json.dumps({"code": 1, "msg": "密码错误！"})