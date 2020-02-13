from pyDes import des, CBC, PAD_PKCS5
import binascii, uuid
from app import app
from app.common._redis import Redis
import json

def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    secret_key = app.config['KEY']
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)

def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    secret_key = app.config['KEY']
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    try:
        deStr = str(de,encoding='utf-8')
    except:
        deStr = de.encode("utf-8")
    return deStr

def get_uuid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid

def setUUIDStatus(uuid, status, userName, setTime):
    data = {
        'status': status,
        'userName': userName,
        'setTime': setTime,
    }
    Redis.hset("loginRequest", uuid, json.dumps(data))

def getUnquieUUID():
    uid = get_uuid()
    if Redis.isExits(uid):
        getUnquieUUID()
    return uid

def getUUIDInfo(uuid):
    if Redis.isExits(uuid):
        return None
    return json.loads(Redis.hget('loginRequest',uuid))
