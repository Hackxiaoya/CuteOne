# CuteOne
**CuteOne**是一款OneDrive多网盘挂载程序，提供多盘负载，在线查看文件等功能。

# 环境需求
* Linux
* Nginx
* Python3  ——[如何安装Python3](https://www.cnblogs.com/s-seven/p/9105973.html)

# 安装流程
* 前言
> 初次安装真的，我自己都觉得繁琐，但是一劳永逸；  
> 如果没有python3的，先安装python3 再执行下面的流程。
* 第一步，拉取代码  
```
git clone https://github.com/Hackxiaoya/CuteOne.git  
```
* 第二步，安装需求的库和创建uwsgi软连
```
pip3 install -r requirements.txt
ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi
```
* 第三步，启动网站后台运行  
```
nohup uwsgi --ini uwsgi.ini &
```
* 第四步，Nginx反代一下，端口是5000

* 第五步，访问安装路径
```
http://你的域名/install/
```
* 第六步，根据流程安装呗
```
等出现安装完成的字样就执行第七步
```
* 第七步，重启程序
```
killall -9 uwsgi && nohup uwsgi --ini uwsgi.ini &
```
* 第八步，添加驱动盘
```
http://你的域名/admin/
到驱动的位置添加个驱动，然后添加个网盘，然后更新一下缓存就可以了
```




# 常见问题
* 出现502 
> 大概是因为CuteOne没运行。
* 首次安装，访问报错
> 首次安装之后需要在后台先添加一个网盘才行。
* 启动了之后，访问报错
> 你大概是首次安装启动，请查看安装流程。



# 常见命令
* 查看uwsgi
```
pgrep -f uwsgi
```
* kill所有uwsgi
```
killall -9 uwsgi
```
* 启动网站
```
nohup uwsgi --ini uwsgi.ini &
```
