# -*-coding:utf-8-*-
from flask import Flask, session, request, Blueprint, make_response, jsonify
from app.common.captcha import CaptchaTool
from app.common.common import *
from app.common.qrcode import *
from app.tables.User import *
import os, hashlib, re, binascii
import time

login = Blueprint('login', __name__)

@login.route('/getCaptcha', methods=["GET"])
def test_get_captcha():
    """
    获取图形验证码
    :return:
    """
    new_captcha = CaptchaTool()
    # 获取图形验证码
    img, code = new_captcha.get_verify_code()
    # 存入session
    session["code"] = code
    return make_response(jsonify({'code': 0, 'content': {'captchCode': img.decode('utf-8')}, 'msg': ''}))

@login.route('/accountLogin', methods=["POST"])
def accountLogin():
    userName = request.json.get('userName')
    password = request.json.get('password')
    captchaCode = request.json.get('captcha')
    # 获取session中的验证码
    s_code = session.get("code", None)
    if not all([captchaCode, s_code]):
        return make_response(jsonify({'code': 10002, 'content': {}, 'msg': '验证码错误'}))
    if s_code != captchaCode:
        return make_response(jsonify({'code': 10002, 'content': {}, 'msg': '验证码错误'}))
    data = User.query.filter_by(username=userName).first()
    if data == None:
        return make_response(jsonify({'code': 10002, 'msg': u'错误的用户名或者密码!'}))
    if encrypt_password(password, data.salt)[0] == data.hash_password:
        session['username'] = data.username
        session['user_id'] = data.id
        currentAuthority = "admin" if data.account_type == 1 else "user"
        return make_response(jsonify({'code': 0, 'msg': u'登录成功', 'userID': data.id, 'userName': data.username,
                                      "currentAuthority": currentAuthority}))
    else:
        return make_response(jsonify({'code': 10002, 'msg': u'错误的用户名或者密码!'}))

@login.route("/qrlogin", methods=["GET", "POST"])
def qrlogin():
    uid = getUnquieUUID()
    setTime = int(round(time.time() * 1000))
    # 初始创建缓存数据
    setUUIDStatus(uid, 0, None, setTime)
    qrcode_str = set_qrcode(url="{0}".format(uid))
    return make_response(jsonify({'code': 0, 'content': {'loginCode': qrcode_str.decode('utf-8'), 'loginId': uid}, 'msg': ''}))

@login.route("/getCodeStatus", methods=["POST"])
def getCodeStatus():
    uuid = request.json.get('loginId')
    uuInfo = getUUIDInfo(uuid)
    if not uuInfo:
        return make_response(jsonify({'code': 10003, 'content': {}, 'msg': '别偷东西！'}))
    if uuInfo['status'] == 1:
        return make_response(jsonify({'code': 0, 'content': {'userName': uuInfo['userName']}, 'msg': '登录成功！'}))
    nowTime = int(round(time.time() * 1000))
    if nowTime - uuInfo['setTime'] > 300000:
        return make_response(jsonify({'code': 10003, 'content': {}, 'msg': '验证码已失效，请刷新重新扫描！'}))
    return make_response(jsonify({'code': 10002, 'content': {}, 'msg': '等待验证！'}))

@login.route("/accpetLogin", methods=["GET", "POST"])
def accpetLogin():
    uuid = request.json.get('uuid')
    userName = request.json.get('userName')
    uuInfo = getUUIDInfo(uuid)
    if not uuInfo:
        return make_response(jsonify({'code': 10002, 'content': {}, 'msg': '别偷东西！'}))
    nowTime = int(round(time.time() * 1000))
    if nowTime - uuInfo['setTime'] > 300000:
        return make_response(jsonify({'code': 10002, 'content': {}, 'msg': '验证码已失效，请刷新重新扫描！'}))
    setUUIDStatus(uuid, 1, userName, nowTime)
    return make_response(jsonify({'code': 0, 'content': {}, 'msg': '登录成功！'}))

def encrypt_password(name, salt=None, encryptlop=30):
  if not salt:
    salt = binascii.hexlify(os.urandom(32)).decode()  # length 32
  for i in range(encryptlop):
    name = hashlib.sha1(str(name + salt).encode('utf-8')).hexdigest()  # length 64
  return name, salt

@login.route('/register',methods=['POST'])
def register():
  username = request.json.get("username")
  password = request.json.get("password")
  email = request.json.get("email")
  zhmodel = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
  match = zhmodel.search(username)
  if match:
    return make_response(jsonify({'code': 10002, 'msg': u'用户名不能包含中文!'}))
  data = User.query.filter_by(username=username).first()
  if data:
    return make_response(jsonify({'code': 10002, 'msg': u'用户名已存在!'}))
  hash_password, salt = encrypt_password(password)
  data = User(username,hash_password,salt,email,0,1)
  db.session.add(data)
  db.session.commit()
  return make_response(jsonify({'code': 0, 'msg': u'注册成功'}))

@login.route('/logout')
def logout():
    session.clear()
    return make_response(jsonify({'code': 0, 'msg': u'退出登录'}))

