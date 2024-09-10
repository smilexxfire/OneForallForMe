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
  -e heartbeat_host=xxxxxxxx \
  -e heartbeat_port=5006 \
  -e heartbeat_open=false \
  --restart=always \
  smilexxfire/oneforall