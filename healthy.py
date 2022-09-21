# 时间 2022/09/21 20:00:00
# 作者 ByteSys
# 声明 该程序仅供学习交流，请自觉遵守中华人民共和国网络安全法

import os
import requests
import json
from time import sleep
from hashlib import md5

def notice(key,title,msg):
  #推送通知消息
  url = 'https://sctapi.ftqq.com/%s.send' % key
  body = { 'title':'每日打卡运行日志-%s' % title ,'desp':msg }
  res = requests.post(url,data=body)
  text = json.loads(res.text)
  if text['code'] != 0:
    print("[SCTPUSH]Error: " + text['info'])
    return
  pushid = text['data']['pushid']
  readkey = text['data']['readkey']
  print("[SCTPUSH]Info: 推送成功,PushId=%sReadKey=%s" % (pushid,readkey))
  
  #查询推送状态
  sleep(30) #推送需要时间
  url = 'https://sctapi.ftqq.com/push?id=%s&readkey=%s' % (pushid,readkey)
  res = requests.get(url)
  text = json.loads(res.text)
  if text['data'] == None:
    print("[SCTPUSH]Error: 未查询到有任何信息")
    return
  data = text['data']
  print("[SCTPUSH]Info: [用户ID]:%s , [标题]:%s , [内容]:%s , [建立时间]:%s" % (data['uid'],data['title'],data['desp'],data['created_at']))
  
if __name__ == "__main__":
  push = os.environ["push"]
  username = os.environ["username"]
  password = os.environ["password"]
  if len(username) == 0 and len(password) == 0:
    print("[Process]Error: 用户名或密码未设置！！！")
    exit(0)
  if len(push) == 0:
    print("[Process]Info: 未设置PUSH_KEY，无法使用Server酱推送运行日志！！！")
  print("[Process]Info: 用户名与密码设置成功，正在开始执行后续代码...")
  
  #登录账号
  request = requests.session()
  header = {"User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"}
  p = md5(password.encode()).hexdigest()
  password = p[:5] + "a" + p[5:9] + "b" + p[9:30]
  body = { "uname" : username , "pd_mm" : password }
  url = 'http://xggl.hnqczy.com/website/login'
  res = request.post(url,headers=header,data=body)
  text = json.loads(res.text)
  if res.status_code == 200 and text.get('error',0) == True:
    print(text['msg'])
    print("[Process]Error: 服务器返回错误，程序终止...")
    exit(0)
  print("[Process]Info: 登录成功，开始打卡...")
  
  #开始打卡
