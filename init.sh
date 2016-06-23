#! /bin/bash

function get_container_ip() {
	ip=""
	while [[ -z "$ip" ]]; do
		ip=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' "$1");
		sleep 1;
	done
	echo "$ip"
}

SPIDER_SETTING="spider/mydm/settings.py"
WWW_SETTING="www/app.py"
NGINX_SETTING="nginx/www.conf"

MONGODB_PATH="$(pwd)/mongodb/"
SPIDER_PATH="$(pwd)/spider/"
WWW_PATH="$(pwd)/www/"
NGINX_PATH="$(pwd)/nginx/"

# init mongodb
echo "mongodb init ..."
docker run -v $MONGODB_PATH:/mongodb/ -w /mongodb --name mongodb -d mongo --auth &>/dev/null
echo "mongodb init users setting"
docker exec mongodb mongo init_admin.js
docker exec mongodb mongo init_db.js

# init redis
echo "redis init ..."
docker run --name redis -d redis &> /dev/null

# init spider
echo "init spider ..."
MONGO_IP=$(get_container_ip mongodb)
echo "mongodb ip is $MONGO_IP"
REDIS_IP=$(get_container_ip redis)
echo "redis ip is $REDIS_IP"
sed -i "s;mongodb://[0-9.]\+;mongodb://$MONGO_IP;;" "$SPIDER_SETTING"
sed -i "s;redis://[0-9.]\+;redis://$REDIS_IP;;" "$SPIDER_SETTING"
docker run -v $SPIDER_PATH:/spider/ -w /spider/ --name spider -d python:2.7 ./run.sh start &>/dev/null

# init www
echo "init www ..."
SPIDER_IP=$(get_container_ip spider)
echo "spider ip is $SPIDER_IP"
sed -i "s;mongodb://[0-9.]\+;mongodb://$MONGO_IP;;" "$WWW_SETTING"
sed -i "s;http://[0-9.]\+;http://$SPIDER_IP;;" "$WWW_SETTING"
docker run -v $WWW_PATH:/www/ -w /www/ --name www -d python:3.5 ./run.sh start &>/dev/null

# start nginx
echo "init nginx ..."
WWW_IP=$(get_container_ip www)
echo "www ip is $WWW_IP"
sed -i "s;server [0-9.]\+;server $WWW_IP;;" "$NGINX_SETTING"
docker run -v $NGINX_PATH:/etc/nginx/conf.d/ -p 80:8000 --name nginx -d nginx &>/dev/null
