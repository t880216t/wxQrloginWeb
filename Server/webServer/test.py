from app.common.common import *
from app.common._redis import Redis
import json,time

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

if __name__ == '__main__':
    # uid = getUnquieUUID()
    # setTime = int(round(time.time() * 1000))
    # print(uid)
    # # 初始创建缓存数据
    # setUUIDStatus(uid, 0, None, setTime)
    # print('command:', Redis.hget('loginRequest', uid))
    print('command:', Redis.hgetall('loginRequest'))
