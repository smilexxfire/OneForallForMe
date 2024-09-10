# OneForallForMe
将oneforall工具集成到[分布式子域名扫描系统](https://github.com/smilexxfire/SubdomainScan)中，支持多个节点分布式部署

## 使用
推荐使用docker一键部署
```shell
docker run -d --name oneforallscan \
  -e rabbitmq_host=xxxxxxxxxx \
  -e rabbitmq_port=5672 \
  -e rabbitmq_username=xxxxxx \
  -e rabbitmq_password=xxxxxx \
  -e mongo_host=xxxxxxxxxxxx \
  -e mongo_port=27017 \
  -e mongo_username=xxxxxxxx \
  -e mongo_password=xxxxxxxx \
  -e mongo_database=src \
  --restart=always \
  smilexxfire/oneforall
```
心跳程序可选
```shell
  -e heartbeat_host=xxxxxxxx \
  -e heartbeat_port=5006 \
  -e heartbeat_open=false \
```
windows部署 :
修改`config/default.ini`
```cmd
pip install -r requirements.txt
python subdomain_worker.py
```