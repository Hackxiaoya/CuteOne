# -*- coding:utf-8 -*-
import threading,sys
import requests
import time
import os

class MulThreadDownload(threading.Thread):
    def __init__(self,url,startpos,endpos,f):
        super(MulThreadDownload,self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        print("start thread:%s at %s" % (self.getName(), time.time()))
        headers = {"Range":"bytes=%s-%s"%(self.startpos,self.endpos)}
        res = requests.get(self.url,headers=headers)
        # res.text 是将get获取的byte类型数据自动编码，是str类型， res.content是原始的byte类型数据
        # 所以下面是直接write(res.content)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        print("stop thread:%s at %s" % (self.getName(), time.time()))
        self.fd.close()

    def run(self):
        self.download()

"""
    下载文件到本地
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    url: 下载地址
    fileName: 文件名称
    drive_id: 驱动ID
"""
def down_file(url, fileName, drive_id):
    # 获取文件的大小和文件名
    filename = "{}/temp_uploads/syn_temp/{}/{}".format(os.getcwd(), drive_id, fileName)
    if not os.path.exists("{}/temp_uploads/syn_temp/{}".format(os.getcwd(), drive_id)):
        # 如果不存在则创建目录
        os.makedirs("{}/temp_uploads/syn_temp/{}".format(os.getcwd(), drive_id))
    try:
        filesize = int(requests.head(url).headers['Content-Length'])
    except:
        down_file(url, fileName)
    print("%s filesize:%s" % (filename, filesize))

    # 线程数
    threadnum = 5
    # 信号量，同时只允许10个线程运行
    threading.BoundedSemaphore(threadnum)
    # 默认3线程现在，也可以通过传参的方式设置线程数
    step = filesize // threadnum
    mtd_list = []
    start = 0
    end = -1

    # 请空并生成文件
    tempf = open(filename, 'w')
    tempf.close()
    # rb+ ，二进制打开，可任意位置读写
    with open(filename, 'rb+') as  f:
        fileno = f.fileno()
        # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
        while end < filesize - 1:
            start = end + 1
            end = start + step - 1
            if end > filesize:
                end = filesize
            # print("start:%s, end:%s"%(start,end))
            # 复制文件句柄
            dup = os.dup(fileno)
            # print(dup)
            # 打开文件
            fd = os.fdopen(dup, 'rb+', -1)
            # print(fd)
            t = MulThreadDownload(url, start, end, fd)
            t.start()
            mtd_list.append(t)

        for i in mtd_list:
            i.join()
    return True # 完成单个文件下载


# if __name__ == "__main__":
#     url = 'https://splogs-my.sharepoint.com/personal/test_my365_ws/_layouts/15/download.aspx?UniqueId=76f5ee8a-c0fc-48ac-ba27-9a2c50355d74&Translate=false&tempauth=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTBmZjEtY2UwMC0wMDAwMDAwMDAwMDAvc3Bsb2dzLW15LnNoYXJlcG9pbnQuY29tQGRlOWMyMzNkLTM3Y2MtNDQ2Yy1hNWVlLTI1ZjBmMDZhNGZiYiIsImlzcyI6IjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMCIsIm5iZiI6IjE1NTM0MDM1MDIiLCJleHAiOiIxNTUzNDA3MTAyIiwiZW5kcG9pbnR1cmwiOiJmRlg5dUc5UzFCRUpZbTM5MERhNUFNYkJmMmIveDhmRkVhRFlsZlQ3YnBJPSIsImVuZHBvaW50dXJsTGVuZ3RoIjoiMTQzIiwiaXNsb29wYmFjayI6IlRydWUiLCJjaWQiOiJObVZsWm1Nek1XRXROelppT0MwME1HVTJMVGd3TWprdE9UTTRNRFZrTkRZME5EUTUiLCJ2ZXIiOiJoYXNoZWRwcm9vZnRva2VuIiwic2l0ZWlkIjoiTUdaak9UbGxNekl0WTJSaFpTMDBOVFV6TFdJeVltWXRZV1U0WlRreU16VXdORGt4IiwiYXBwX2Rpc3BsYXluYW1lIjoidGVzdGFwcCIsImFwcGlkIjoiM2I3OWQ5NGYtYThiOC00ZWU0LWI3ZDctNDFlMjY5NzkwNjM4IiwidGlkIjoiZGU5YzIzM2QtMzdjYy00NDZjLWE1ZWUtMjVmMGYwNmE0ZmJiIiwidXBuIjoidGVzdEBteTM2NS53cyIsInB1aWQiOiIxMDAzMjAwMDQwNUQ2RTJBIiwiY2FjaGVrZXkiOiIwaC5mfG1lbWJlcnNoaXB8MTAwMzIwMDA0MDVkNmUyYUBsaXZlLmNvbSIsInNjcCI6ImFsbGZpbGVzLndyaXRlIiwidHQiOiIyIiwidXNlUGVyc2lzdGVudENvb2tpZSI6bnVsbH0.eFgzMHFFaXJUQkZ6bEt3bThGaFBQMlZsL01HUWdNR2wwbjdVQzNsOUZEQT0&ApiVersion=2.0'
#     fileName = 'douyintest1.mp4'
#     down_file(url, fileName)