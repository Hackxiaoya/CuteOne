# -*- coding:utf-8 -*-
import time, json, random, os, hashlib
from flask import render_template, request, redirect, url_for, make_response
from flask_login import current_user
from flask_login import login_user, logout_user
from app.admin.users import models as usersModels
from app.admin.author import models as authorModels
from app.admin.files import models as filesModels
from app.admin.system import models as systemModels
from app import MysqlDB
from app.main import index
from ..users import logic
from app import common
import config
THEMES = 'themes/'+ config.THEMES +'/'




@index.route('/users/login', methods=['GET', 'POST'])  # Login
def login():
    if request.method == 'GET':
        return render_template(THEMES + 'users/login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        password = common.hashPwd(password)
        res = usersModels.users.checkpassword(username, password, request.remote_addr)
        if res["code"]:
            model = usersModels.users()  # 实例化一个对象，将查询结果逐一添加给对象的属性
            model.id = res["msg"].id
            model.username = res["msg"].username
            model.avatar = res["msg"].avatar
            model.nickname = res["msg"].nickname
            model.score = res["msg"].score
            if res["msg"].group:
                model.group = authorModels.authGroup.find_by_id(res["msg"].group).title
            else:
                model.group = "普通会员"
            login_user(model)
            return json.dumps({"code": 0, "msg": "登陆成功！"})
        else:
            return json.dumps({"code": 1, "msg": res["msg"]})


@index.route('/users/register', methods=['GET', 'POST'])  # Register
def register():
    username = request.form['username']
    password = request.form['password']
    nickname = request.form['nickname']
    if len(password) < 6:
        return json.dumps({"code": 1, "msg": "密码格式错误"})
    password = common.hashPwd(password)
    res = usersModels.users.check_username(username)
    if res:
        return json.dumps({"code": 1, "msg": "用户名已存在"})
    else:
        files_disk_id = '0' if systemModels.config.get_config('files_disk_id') == None else systemModels.config.get_config('files_disk_id').value
        # 初始化role 并插入数据库
        role = usersModels.users(
            username = username,
            password = password,
            nickname = nickname,
            email = '',
            description = '',
            avatar = "/static/uploads/avatar/{}.png".format(random.randint(1, 10)),
            sex = 3,
            login_num = 0,
            score = 0,
            group = 0,
            status = 1,
            files_disk_id = files_disk_id,
            register_ip = request.remote_addr,
            birthday = '0001-01-01 00:00:00',
            reg_time = time.strftime('%Y-%m-%d %H:%M:%S'),
            update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        )
        MysqlDB.session.add(role)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "注册成功！"})


@index.route("/users/logout")
def logout():
    logout_user()
    return redirect(url_for('/._index'))


@index.route('/users/users_list', methods=['GET', 'POST'])
@index.route('/users/users_list/', methods=['GET', 'POST'])
def users_list():
    page_number = '1' if request.args.get('page') is None else request.args.get('page')
    result = logic.get_users_list(page_number, 12)
    return render_template(THEMES+'users/users_list.html', data=result)


@index.route('/users/personal/<int:id>', methods=['GET', 'POST'])
def personal(id):
    result = usersModels.users.find_by_id(id)
    if result.group == 0:
        result.group = "普通会员"
    else:
        result.group = authorModels.authGroup.find_by_id(result.group).title
    return render_template(THEMES+'users/personal.html', data=result)


@index.route('/users/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'GET':
        if current_user.get_id() is not None:
            result = usersModels.users.find_by_id(current_user.id)
            return render_template(THEMES + 'users/setting.html', data=result)
        else:
            return redirect(url_for('/._index'))
    else:
        if current_user.get_id() is not None:
            from_data = request.form
            from_data = from_data.to_dict()
            from_data['id'] = current_user.id
            if int(from_data['formtype']) == 1:
                from_data.pop('formtype')
                # 是否修改密码
                if from_data['password']:
                    from_data['password'] = common.hashPwd(from_data['password'])
                else:
                    from_data.pop('password')  # 不修改密码，删除键值
                usersModels.users.update(from_data)
                return json.dumps({"code": 0, "msg": "完成！"})
        else:
            return json.dumps({"code": 1, "msg": "未登陆！"})


@index.route('/users/upload', methods=['POST'])
def upload_avatar():
    if current_user.get_id() is not None:
        file = request.files.get('file')
        fileName = hashlib.sha1(file.read()).hexdigest()
        file.seek(0)
        file_path = "/app/static/uploads/avatar/{}.{}".format(fileName, file.filename.rsplit('.',1)[1])
        src_path = "/static/uploads/avatar/{}.{}".format(fileName, file.filename.rsplit('.',1)[1])
        file.save(os.getcwd()+file_path)
        return json.dumps({"code": 0, "msg": "", "data": {"src": src_path}})
    else:
        return json.dumps({"code": 1, "msg": "未登陆！"})


@index.route('/users/files_list', methods=['GET', 'POST'])
@index.route('/users/files_list/', methods=['GET', 'POST'])
def files_list():
    if current_user.get_id() is not None:
        page_number = '1' if request.args.get('page') is None else request.args.get('page')
        result = logic.get_users_files_list(1, page_number, 12)
        files_disk_id = usersModels.users.find_by_id(current_user.id).files_disk_id
        return render_template(THEMES + 'users/files_list.html', files_disk_id=files_disk_id, data=result)
    else:
        return redirect(url_for('/._index'))


@index.route('/users/get_files_downloadUrl/<int:uid>/<int:disk_id>/<string:files_id>')
def get_files_downloadUrl(uid, disk_id, files_id):
    data = logic.file_url(uid, disk_id, files_id)
    return json.dumps(data)


@index.route('/users/users_pop_video/<int:uid>/<int:disk_id>/<string:files_id>')
def users_pop_video(uid, disk_id, files_id):
    data = logic.file_url(uid, disk_id, files_id)
    share_url = "/users/users_video/{}/{}/{}".format(uid, disk_id, files_id)
    donw_url = "/users/down_users_file/{}/{}/{}".format(uid, disk_id, files_id)
    data["uid"] = uid
    data["disk_id"] = disk_id
    data["files_id"] = files_id
    return render_template(THEMES+'users/users_pop_video.html', share_url=share_url, donw_url=donw_url, data=data)


@index.route('/users/users_video/<int:uid>/<int:disk_id>/<string:files_id>')
@index.route('/users/users_video/<int:uid>/<int:disk_id>/<string:files_id>/')
def users_video(uid, disk_id, files_id):
    data = logic.file_url(uid, disk_id, files_id)
    share_url = "/users/users_video/{}/{}/{}".format(uid, disk_id, files_id)
    donw_url = "/users/down_users_file/{}/{}/{}".format(uid, disk_id, files_id)
    data["uid"] = uid
    data["disk_id"] = disk_id
    data["files_id"] = files_id
    return render_template(THEMES+'users/users_video.html', share_url=share_url, donw_url=donw_url, data=data)


@index.route('/users/down_users_file/<int:uid>/<int:disk_id>/<string:files_id>')
@index.route('/users/down_users_file/<int:uid>/<int:disk_id>/<string:files_id>/')
def down_users_file(uid, disk_id, files_id):
    response = logic.file_url(uid, disk_id, files_id)
    data = make_response(redirect(response["url"]))
    data.headers["Content-Disposition"] = "attachment; filename={}".format(response["name"].encode().decode('latin-1'))
    return data



@index.route('/users/file_uploads_small/<int:files_disk_id>', methods=['GET']) # 小文件上传
@index.route('/users/file_uploads_small/<int:files_disk_id>/', methods=['GET'])
def file_uploads_small(files_disk_id):
    if current_user.get_id() is not None:
        # path = request.args.get('path')
        return render_template(THEMES+'users/file_uploads_small.html', files_disk_id=files_disk_id)
    else:
        return redirect(url_for('/._index'))


@index.route('/users/file_uploads_big/<int:files_disk_id>', methods=['GET']) # 大文件上传
@index.route('/users/file_uploads_big/<int:files_disk_id>/', methods=['GET'])
def file_uploads_big(files_disk_id):
    if current_user.get_id() is not None:
        # path = request.args.get('path')
        return render_template(THEMES+'users/file_uploads_big.html', files_disk_id=files_disk_id)
    else:
        return redirect(url_for('/._index'))


@index.route('/users/file_uploads', methods=['POST'])
def file_uploads():
    if current_user.get_id() is not None:
        md5value = request.form['md5value']
        chunk = request.form['chunk']
        files_disk_id = request.form['files_disk_id']
        file = request.files['file']
        uid = current_user.id
        file_path = "{}/temp_uploads/users_files_temp/{}/{}/{}".format(os.getcwd(), files_disk_id, uid, md5value)
        isExists = os.path.exists(file_path)
        if not isExists:
            # 如果不存在则创建目录
            os.makedirs(file_path)
        file.save(file_path + "/" + chunk)
        return json.dumps({})
    else:
        return redirect(url_for('/._index'))



@index.route('/users/file_uploads_check', methods=['GET', 'POST'])
def file_uploads_check():
    if current_user.get_id() is not None:
        md5 = request.form['md5']
        uid = current_user.id
        files_disk_id  = request.form['files_disk_id']
        # 通过MD5唯一标识找到缓存文件
        file_path = "{}/temp_uploads/users_files_temp/{}/{}/{}".format(os.getcwd(), files_disk_id, uid, md5)
        if os.path.exists(file_path):
            block_info = os.listdir(file_path)
            return json.dumps({'block_info': block_info})
        else:
            return json.dumps({})
    else:
        return redirect(url_for('/._index'))


@index.route('/users/file_uploads_success', methods=['GET', 'POST'])
def file_uploads_success():
    files_disk_id = request.form['files_disk_id']
    md5 = request.form['md5']
    fileName = request.form['fileName']
    uid = current_user.id
    target_filename = "{}/temp_uploads/users_files_temp/{}/{}/{}".format(os.getcwd(), files_disk_id, uid, md5)    # 获取上传文件的文件名
    ok_file = "{}/temp_uploads/users_files_temp/{}/{}/{}".format(os.getcwd(), files_disk_id, uid, fileName)
    chunk = 0
    with open(ok_file, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = target_filename + "/" + str(chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片
    if os.path.exists(target_filename):
        os.rmdir(target_filename)   # 删除文件夹

    # 初始化role 并插入数据库
    role = filesModels.files(uid=uid, disk_id=files_disk_id, type='usersUploads', name=fileName, file='', size='', files_id='', status=0)
    MysqlDB.session.add(role)
    MysqlDB.session.flush()
    MysqlDB.session.commit()
    # 推送到上传任务
    logic.pull_uploads(role.id, current_user.id, files_disk_id, fileName, '/')
    return json.dumps({"code": 0, "msg": "完成！"})