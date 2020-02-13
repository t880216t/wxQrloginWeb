# -*-coding:utf-8-*-
from flask import Flask, session, request, Blueprint, make_response, jsonify
from app.common.captcha import CaptchaTool
from app.common.common import *
from app.common.qrcode import *
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
    return img

@login.route('/verifyCaptcha', methods=["POST"])
def test_verify_captcha():
    """
    验证图形验证码
    :return:
    """
    obj = request.get_json(force=True)
    # 获取用户输入的验证码
    code = obj.get('code', None)
    # 获取session中的验证码
    s_code = session.get("code", None)
    print(code, s_code)
    if not all([code, s_code]):
        return "参数错误"
    if code != s_code:
        return "验证码错误"
    return "验证成功"

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
        return make_response(jsonify({'code': 10002, 'content': {}, 'msg': '别偷东西！'}))
    if uuInfo['status'] == 1:
        return make_response(jsonify({'code': 0, 'content': {'userName': uuInfo['userName']}, 'msg': '登录成功！'}))
    nowTime = int(round(time.time() * 1000))
    if nowTime - uuInfo['setTime'] > 300000:
        return make_response(jsonify({'code': 10002, 'content': {}, 'msg': '验证码已失效，请刷新重新扫描！'}))
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

