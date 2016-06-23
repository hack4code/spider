#! /bin/bash

SPIDER_SETTING="spider/mydm/settings.py"
WWW_SETTING="www/app.py"
NGINX_SETTING="nginx/www.conf"

function get_container_ip() {
	ip=""
	while [[ -z "$ip" ]]; do
		ip=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' "$1");
		sleep 1;
	done

	echo "$ip"
}


function start_spider() {
	# start mongodb
	docker start mongodb

	# start redis
	docker start redis

	# start spider
	MONGO_IP=$(get_container_ip mongodb)
	REDIS_IP=$(get_container_ip redis)
	sed -i "s;mongodb://[0-9.]\+;mongodb://$MONGO_IP;;" "$SPIDER_SETTING"
	sed -i "s;redis://[0-9.]\+;redis://$REDIS_IP;;" "$SPIDER_SETTING"
	docker start spider

	# start www
	SPIDER_IP=$(get_container_ip spider)
	sed -i "s;mongodb://[0-9.]\+;mongodb://$MONGO_IP;;" "$WWW_SETTING"
	sed -i "s;http://[0-9.]\+;http://$SPIDER_IP;;" "$WWW_SETTING"
	docker start www

	# start nginx
	WWW_IP=$(get_container_ip www)
	sed -i "s;server [0-9.]\+;server $WWW_IP;;" "$NGINX_SETTING"
	docker start nginx
}

function stop_spider() {
	docker stop nginx www spider mongodb redis
}

case "$1" in
	start)
		start_spider
		;;
	stop)
		stop_spider
		;;
	restart)
		stop_spider
		start_spider
		;;
esac
