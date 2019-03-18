# -*- coding:utf-8 -*-
"""
    权限修饰器
"""
import functools
from flask import redirect, session

#定义一个装饰器用于拦截用户登录
#func是使用该修饰符的地方是视图函数
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