# -*- coding:utf-8 -*-
import datetime
from app import app, MysqlDB
from app.main import index
from flask import request, render_template, json, make_response, redirect
from ...album import models, logic
import config
THEMES = 'themes/'+ config.THEMES +'/'


# Whether there is a string
def typeTitle(id):
    res = logic.get_tag_info(id)
    if res:
        result = res.title
    else:
        result = "默认"
    return result
app.jinja_env.filters['typeTitle'] = typeTitle  #注册自定义过滤器

def dateformat(value):
    result = datetime.datetime.strftime(value, '%Y-%m-%d')
    return result
app.jinja_env.filters['dateformat'] = dateformat



@index.route('/album/')  # 默认首页
@index.route('/album/index')
def album_index():
    classify = models.classify.find_by_types(0, 6)
    recommend_list = models.album.find_by_recommend(1, 5)
    host_url = request.host_url
    for i in recommend_list:
        i.img_src = "{}album/get_img/{}/{}".format(host_url, i.drive_id, i.img)
    recommend_index = recommend_list[0]
    recommend_index.img_src = "{}album/get_img/{}/{}".format(host_url, recommend_index.drive_id, recommend_index.img)

    news_list =  models.album.find_all(20, 1)["data"]
    for n in news_list:
        n.img_src = "{}album/get_img/{}/{}".format(host_url, n.drive_id, n.img)


    return render_template(THEMES + 'album/index.html', activity_nav='index', classify=classify, recommend_index=recommend_index, recommend_list=recommend_list, news_list=news_list)


@index.route('/album/classify/<int:id>')
def album_classify(id):
    host_url = request.host_url
    type_info = logic.get_tag_info(id)
    if type_info:
        type_info = {"id":type_info.id, "title":type_info.title, "img":type_info.img}
    else:
        type_info = {"id":0, "title":"默认", "img":""}
    type_list = models.classify.find_by_types(0)
    result = models.album.find_by_type(id, 20)
    if result["data"]:
        for n in result["data"]:
            n.img_src = "{}album/get_img/{}/{}".format(host_url, n.drive_id, n.img)
    return render_template(THEMES + 'album/classify.html', activity_nav='index', data=result["data"], type_list=type_list, type_info=type_info)


@index.route('/album/detail/<int:id>')
def album_detail(id):
    result =  models.album.find_by_id(id)
    models.album.update({"id":id, "views":result.views+1})
    result.img_src = "{}album/get_img/{}/{}".format("/", result.drive_id, result.img)
    result.pic_list = []
    pic_res = result.pic.split(",")
    if pic_res:
        for p in pic_res:
            result.pic_list.append("{}album/get_img/{}/{}".format("/", result.drive_id, p))
    return render_template(THEMES + 'album/detail.html', activity_nav='index', data=result)


@index.route('/album/ajax_data', methods=['GET', 'POST'])
def album_ajax_data():
    host_url = request.host_url
    from_data = request.form
    from_data = from_data.to_dict()
    html_result = ""
    if from_data["page"] == "index": # 首页,因为默认展示了20个，所以翻页要从第6页开始。
        result = models.album.find_all(4, 4+int(from_data["paged"]))["data"]
    elif from_data["page"] == "classify":
        result = models.album.find_by_type(from_data["query"], 4, 4 + int(from_data["paged"]))["data"]
    for i in result:
        type_title = logic.get_tag_info(i.type_id)
        if type_title:
            type_title = type_title.title
        else:
            type_title = "默认"
        html_result += logic.html_template(
            from_data["page"],
            id=i.id,
            title=i.title,
            img_src="{}album/get_img/{}/{}".format(host_url, i.drive_id, i.img),
            type_id=i.type_id,
            type_title=type_title,
            views=i.views,
            create_time=datetime.datetime.strftime(i.create_time, '%Y-%m-%d')
        )

    return html_result


@index.route('/album/get_img/<int:dirve_id>/<string:file_id>', methods=['GET', 'POST'])
def album_get_img(dirve_id, file_id):
    response = logic.get_downloadUrl(dirve_id, file_id)
    data = make_response(redirect(response["url"]))
    data.headers["Content-Disposition"] = "attachment; filename={}".format(response["name"].encode().decode('latin-1'))
    return data