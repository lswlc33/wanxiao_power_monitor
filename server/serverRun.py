from flask import Flask
from flask import request
from flask_cors import CORS
from waitress import serve


from tools.wanxiao_api import getRoomState
from tools.allRoomList import getRoomFullId
from tools.db import WanxiaoDB

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/api/checkOk", methods=["POST", "GET"])
def checkOk():
    return {"msg": "ok"}


@app.route("/api/getRoomState", methods=["POST", "GET"])
def getRoomStateApi():
    roomId = request.args.get("roomId")
    if roomId is None:
        return {"msg": "请输入房间"}
    RoomFullId = getRoomFullId(roomId)
    if RoomFullId is None:
        return {"msg": "请输入正确的房间"}
    power = getRoomState(RoomFullId)
    if power is None:
        return {"msg": "获取失败,请检查"}
    return {"msg": power}


@app.route("/api/getRoomStateRecent", methods=["POST", "GET"])
def getRoomStateRecent():
    roomId = request.args.get("roomId")
    num = request.args.get("num")
    db = WanxiaoDB()
    sql = f"SELECT recordTime, roomState FROM powerData WHERE roomName = '{roomId}' ORDER BY recordTime DESC LIMIT {num};"
    data = db.getData(sql)
    return {"data": data}


@app.route("/api/getDangerRoom", methods=["POST", "GET"])
def getDangerRoom():
    db = WanxiaoDB()
    sql = """
SELECT
	* 
FROM
	( SELECT roomName, roomState FROM powerData ORDER BY recordTime DESC LIMIT 2200 ) AS latest 
WHERE
	roomState BETWEEN 0.01 
	AND 100 
GROUP BY
	roomName 
ORDER BY
	roomState ASC LIMIT 10;"""
    data = db.getData(sql)
    return {"data": data}


@app.route("/api/getDiedRoom", methods=["POST", "GET"])
def getDiedRoom():
    db = WanxiaoDB()
    sql = """
SELECT
	* 
FROM
	( SELECT roomName, roomState FROM powerData ORDER BY recordTime DESC LIMIT 2200 ) AS latest 
WHERE
	roomState BETWEEN -0.01 
	AND -100 
GROUP BY
	roomName 
ORDER BY
	roomState ASC;"""
    data = db.getData(sql)
    return {"data": data}


@app.route("/api/getRoomStateRank", methods=["POST", "GET"])
def getRoomStateRank():
    db = WanxiaoDB()

    types = [
        "WHERE diff < 0 ORDER BY diff",  # 耗电之王
        "WHERE diff < 0 ORDER BY diff DESC",  # 省电之星
        "WHERE diff > 0 ORDER BY diff DESC",  # 充电神壕
    ]
    type = types[int(request.args.get("type"))]

    # 耗电排行
    sql = f"""
    SELECT
    a.roomName,
    ROUND(a.roomState - b.roomState, 2) AS diff
    FROM
    (
        SELECT
        roomName,
        roomState,
        MAX(recordTime) AS maxRecordTime
        FROM
        powerData 
        WHERE
        recordTime >= date('now', 'localtime', 'start of day') 
        AND recordTime < date('now', 'localtime', 'start of day', '+1 day') 
        GROUP BY
        roomName
    ) AS a
    JOIN
    (
        SELECT
        roomName,
        roomState,
        MAX(recordTime) AS maxRecordTime
        FROM
        powerData 
        WHERE
        recordTime >= date('now', 'localtime', '-1 day', 'start of day') 
        AND recordTime < date('now', 'localtime', 'start of day') 
        GROUP BY
        roomName
    ) AS b ON a.roomName = b.roomName
    {type} LIMIT 10;
    """

    data = db.getData(sql)
    return {"data": data}


if __name__ == "__main__":
    # app.run(host='0.0.0.0',debug=False,threaded=True)
    serve(app, host='0.0.0.0', port=5000)
