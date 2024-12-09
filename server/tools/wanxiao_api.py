import json, time, requests


from tools.usFun import getCurrentTime, log, randomStudentId


headers = {"Content-Type": "application/json;charset=UTF-8"}


def getRoomState(roomFullId):
    url = "https://cloudpaygateway.59wanmei.com:8087/paygateway/smallpaygateway/trade"
    data = {
        "timestamp": getCurrentTime(),
        "method": "samllProgramGetRoomState",
        "bizcontent": '{"payproid":6250,"schoolcode":"609","roomverify":"'
        + roomFullId
        + '","businesstype":2,"idserial":"1111","businesstype":2,"idserial":"'
        + randomStudentId()
        + '"}',
        "sourceId": 1,
    }

    try:
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
    except:
        log("请求失败,尝试重试")
        return getRoomState(roomFullId)

    try:
        return response.json()["businessData"]["quantity"]
    except:
        if "频繁" in response.text:
            log("频繁请求，等待60s")
            time.sleep(60)
            return getRoomState(roomFullId)
        else:
            log(f"Header: {response.headers}")
            log(f"Data: {data}")
            log(f"Response: {response.text}")
            return None


if __name__ == "__main__":
    pass
