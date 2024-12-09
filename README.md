# 电力监控面板

## 特性

-   查询当前电量
-   查看历史电量趋势图
-   查询全校电量 TOP10 信息

## 未完成

-   用户管理
-   电量预警提醒

## 环境配置

### 准备环境

-   python 3.12
-   windows 10 +

### 克隆项目

```bash
git clone https://github.com/lswlc33/wanxiao_power_monitor.git
```

### 安装依赖

```bash
pip install requests
pip install flask
pip install flask_cors
pip install waitress
```

### 启动爬虫

> 请保证你在项目根目录!
> cd wanxiao_power_monitor

确保请求配置符合你的学校情况  
修改 `server/tools/wanxiao_api.py` 中  
`getRoomState` 函数的 `data` 字段

```bash
python server/spiderRun.py
```

### 启动后端

> 修改端口，修改 server/serverRun.py 最后
> serve(app, host='0.0.0.0', port=5000)

```bash
python server/serverRun.py
```

### 启动前端

配置后端接口
修改 `web/js/myjs.js` 开头的 `API_URL`

直接运行网页或者使用 `nginx` 部署网页

## 致谢

Material Design User Interface [https://www.mdui.org/](https://www.mdui.org/)  
Apache ECharts [https://echarts.apache.org/](https://echarts.apache.org/)  
Flask [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)  
waitress [https://docs.pylonsproject.org/projects/waitress/en/latest/](https://docs.pylonsproject.org/projects/waitress/en/latest/)
