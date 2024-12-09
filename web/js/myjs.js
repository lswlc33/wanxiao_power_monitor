// 后端API地址
var API_URL = `/`;
// API_URL = 'http://localhost:5000/';
// API_URL = 'http://zzw1.wch1.top:22100/';

// 判断页面进行初始化
window.onload = function () {
    let page = document.querySelector("mdui-navigation-bar").value
    fetch(API_URL + "api/checkOk")
        .then(response => response.json())
        .then(data => {
            if (data['msg'] != "ok") {
                dialogOpen(document.querySelector("mdui-dialog"), "出错啦！", "后端连接失败，请检查")
            }
        })

    if (page == "item-1") {
        initIndexPage()
    } else if (page == "item-2") {
        initSearchPage()
    } else {
        initMyPage()
    }
}

let initIndexPage = () => {
    fetch(API_URL + 'api/getDangerRoom')
        .then(response => response.json())
        .then(data => {
            let dangerRoom = document.getElementById("dangerRoom");
            let roomid = data['data'].map(item => (item[0]));
            let power = data['data'].map(item => (parseFloat(item[1])));
            setChart(dangerRoom, roomid, power, 1);
        });

    //  添加计时器缓解后端压力
    setTimeout(() => {
        fetch(API_URL + 'api/getDiedRoom')
            .then(response => response.json())
            .then(data => {
                let diedRoom = document.getElementById("diedRoom");
                let roomid = data['data'].map(item => (item[0]));
                let power = data['data'].map(item => (parseFloat(item[1])));
                setChart(diedRoom, roomid, power, 1);
            });
    }, 500);
    setTimeout(() => {
        fetch(API_URL + 'api/getRoomStateRank?type=2')
            .then(response => response.json())
            .then(data => {
                let richRoom = document.getElementById("richRoom");
                let roomid = data['data'].map(item => (item[0]));
                let power = data['data'].map(item => (parseFloat(item[1])));
                setChart(richRoom, roomid, power, 1);
            })
    }, 1000);
    setTimeout(() => {
        fetch(API_URL + 'api/getRoomStateRank?type=0')
            .then(response => response.json())
            .then(data => {
                let wasteRoom = document.getElementById("wasteRoom");
                let roomid = data['data'].map(item => (item[0]));
                let power = data['data'].map(item => (parseFloat(item[1])));
                setChart(wasteRoom, roomid, power, 1);
            })
    }, 1500);
    setTimeout(() => {
        fetch(API_URL + 'api/getRoomStateRank?type=1')
            .then(response => response.json())
            .then(data => {
                let saveRoom = document.getElementById("saveRoom");
                let roomid = data['data'].map(item => (item[0]));
                let power = data['data'].map(item => (parseFloat(item[1])));
                setChart(saveRoom, roomid, power, 1);
            })
    }, 2000);
}

let initSearchPage = () => { }

let initMyPage = () => {
    document.querySelector("#alert_setting_save").addEventListener("click", () => {
        dialogOpen(document.querySelector("mdui-dialog"), "抱歉！", "该功能还没写出来 TAT")
    });
}

let setChart = (dom, x, y, type) => {
    let chart = echarts.init(dom);

    let needInverse = y[0] < 0; // 是否需要反转

    // 横条形图
    let option1 = {
        grid: {
            top: '5%',
            bottom: '5%',
            left: '3%',
            right: '10%',
            containLabel: true
        },
        xAxis: {
            inverse: needInverse,
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: x.reverse()
        },
        series: [{
            data: y.reverse(),
            type: 'bar',
            barWidth: '60%',
            barGap: '-100%',
            itemStyle: {
                normal: {
                    barBorderRadius: [0, 10, 10, 0]
                }
            },
            label: {
                show: true,
                position: 'outside',
                formatter: '{c}'
            }
        }]
    };

    // 竖折线图
    let option2 = {
        grid: {
            top: '10%',
            bottom: '10%',
            left: '3%',
            right: '4%',
            containLabel: true
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: y,
            axisLabel: {
                formatter: function (value) {
                    var date = new Date(value);
                    return (date.getMonth() + 1) + '-' + date.getDate();
                }
            }
        },
        yAxis: {
            type: 'value',
            min: value => value.min - 1,
            max: value => value.max + 1,
        },
        series: [{
            type: 'line',
            data: x
        }]
    }

    // 根据类型设置图表
    if (type == 1) {
        chart.setOption(option1);
    } else if (type == 2) {
        chart.setOption(option2);
    }
}

// 查询按钮点击事件
let getPower = () => {
    document.getElementById("current_power").innerHTML = '<mdui-circular-progress></mdui-circular-progress>';
    document.getElementById('recentdaypower').innerHTML = '<mdui-circular-progress></mdui-circular-progress>';
    document.getElementById('recentmopower').innerHTML = '<mdui-circular-progress></mdui-circular-progress>';
    let room_id = document.getElementById("room_id").value;

    fetch(API_URL + `api/getRoomState?roomId=${room_id}`)
        .then(res => res.json()).then(res => {
            document.getElementById("current_power").innerHTML = res['msg'];
        })
    setTimeout(() => {
        fetch(API_URL + `api/getRoomStateRecent?roomId=${room_id}&num=24`)
            .then(data => data.json()).then(data => {
                let times = data['data'].map(item => (item[0]));
                let power = data['data'].map(item => (parseFloat(item[1])));
                setChart(document.getElementById('recentdaypower'), power, times, 2);
            })

    }, 500);
    setTimeout(() => {
        fetch(API_URL + `api/getRoomStateRecent?roomId=${room_id}&num=500`)
            .then(data => data.json()).then(data => {
                let times = data['data'].map(item => (item[0]));
                let power = data['data'].map(item => (parseFloat(item[1])));
                setChart(document.getElementById('recentmopower'), power, times, 2);
            })
    }, 500);


}

// mdui的提示框
let dialogOpen = (dom, headline, description) => {
    dom.headline = headline;
    dom.description = description;
    dom.open = true;
}