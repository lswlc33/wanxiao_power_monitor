from tools.wanxiao_api import getRoomState
from datetime import datetime
from tools.db import WanxiaoDB
from tools.allRoomList import all_room_list
import time
from tools.usFun import getCurrentTime, log

mydb = WanxiaoDB()


def getAllRoomDataAndWrite():
    startTime = time.time()
    insert_data_list = []
    for build in all_room_list:
        for level in build["list"]:
            log(f"正在获取 {build['name']} {level['name']} 的房间数据")
            for roomid in level["list"]:
                power = getRoomState(roomid["id"])
                insert_data = (
                    getCurrentTime(),
                    int(build["id"]),
                    int(level["id"]),
                    roomid["id"],
                    build["name"],
                    level["name"],
                    roomid["name"],
                    power,
                )
                mydb.insertData(insert_data)
                insert_data_list.append(insert_data)
            time.sleep(1)
        time.sleep(60)
    log(f"获取结束，共耗时{time.time() - startTime}秒")
    return True


if __name__ == "__main__":
    while True:
        isOk = getAllRoomDataAndWrite()
        if isOk:
            time.sleep(60 * 60)
        else:
            break
