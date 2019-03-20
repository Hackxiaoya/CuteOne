# -*- coding:utf-8 -*-
import re, urllib.parse, json
from flask import render_template, request, make_response, redirect
from app.admin.drive import models as driveModels
from app.admin.system import models as systemModels
from ..index import index
from ..index import logic


# 基本配置
@index.context_processor
def webconfig():
    webconfig = systemModels.config.all()
    webconfig.pop('username')
    webconfig.pop('password')
    return dict(webconfig=webconfig)


# 驱动列表, 面包屑
@index.context_processor
def drive_list():
    drive_list = driveModels.drive.all("sort", 2)
    url_path = request.full_path
    testpath = url_path.find("path=")
    if testpath > 0:
        reres = re.findall('(.+?.+)path=(.+?.+)', url_path)[0]
        crumbs_url = reres[0]
        crumbs_list = re.split('[/]', reres[1])
        crumbs_list.pop(0)
        crumbs_list_data = []
        for i in range(len(crumbs_list)):
            crumbs_list[i] = urllib.parse.unquote(crumbs_list[i])
            name = urllib.parse.unquote(crumbs_list[i])
            if i:
                crumbs_list[i] = crumbs_list[i-1] + "/" + crumbs_list[i]

            crumbs_list_data.append({"path": crumbs_list[i], "name": name})
    else:
        crumbs_list = []
        crumbs_url = url_path
        crumbs_list_data = []
    return dict(drive_list=drive_list, crumbs_url=crumbs_url, crumbs_list_data=crumbs_list_data)


@index.route('/')  # 默认首页
def _index():
    drive = request.args.get('drive')
    disk = request.args.get('disk')
    # 优先进行条件查询
    if drive:
        driveurl = '/?drive={}'.format(drive)
        if disk:
            disk_id = disk
            driveurl = '{}&disk={}'.format(driveurl, disk)
        else:
            disk_id = driveModels.drive_list.find_by_chief(drive).id
            driveurl = '{}&disk={}'.format(driveurl, disk_id)

        if request.args.get('path'):
            path = request.args.get('path')
            data = logic.get_disk(disk_id, path)
            current_url = '{}&path={}'.format(driveurl, path)
        else:
            data = logic.get_disk(disk_id)
            current_url = '{}&path='.format(driveurl)
    else:
        activate = driveModels.drive.find_activate()
        drive = activate.id
        disk_id = driveModels.drive_list.find_by_chief(activate.id).id
        data = logic.get_disk(disk_id)
        current_url = '/?drive={}&disk={}&path='.format(activate.id, disk_id)

    return render_template('index/index.html', activity_nav='index', drive_id=drive, disk_id=disk_id, current_url=current_url, data=data)


@index.route('/video/<int:drive_id>/<int:disk_id>/<string:id>')
def video(drive_id, disk_id, id):
    data = logic.get_downloadUrl(drive_id, disk_id, id)
    share_url = "/video/{}/{}/{}".format(drive_id, disk_id, id)
    donw_url = "/down_file/{}/{}/{}".format(drive_id, disk_id, id)
    return render_template('index/video.html', share_url=share_url, donw_url=donw_url, data=data)


@index.route('/get_downloadUrl/<int:drive_id>/<int:disk_id>/<string:id>')
def get_downloadUrl(drive_id, disk_id, id):
    data = logic.get_downloadUrl(drive_id, disk_id, id)
    return json.dumps(data)


@index.route('/pop_video/<int:drive_id>/<int:disk_id>/<string:id>')
def pop_video(drive_id, disk_id, id):
    data = logic.get_downloadUrl(drive_id, disk_id, id)
    share_url = "/video/{}/{}/{}".format(drive_id, disk_id, id)
    donw_url = "/down_file/{}/{}/{}".format(drive_id, disk_id, id)
    return render_template('index/pop_video.html', share_url=share_url, donw_url=donw_url, data=data)


@index.route('/down_file/<int:drive_id>/<int:disk_id>/<string:id>')
def down_file(drive_id, disk_id, id):
    response = logic.down_file(drive_id, disk_id, id)
    data = make_response(redirect(response["url"]))
    data.headers["Content-Disposition"] = "attachment; filename={}".format(response["name"])
    return data