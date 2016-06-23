#! /bin/bash

function init() {
	[ -z "$PROXY" ] && {
		pip install -r requirements.txt
	} || {
		pip install --proxy http://${PROXY} -r requirements.txt
	}
	adduser --disabled-password --gecos '' spider
	touch /var/log/spider.log && chown spider:spider /var/log/spider.log
}

function start_spider() {
	id spider &>/dev/null || init
	su -m spider -c "celery multi start spiderjob -A task.spider --pidfile=spider.pid --logfile=/var/log/spider.log --loglevel=INFO"
	su -m spider -c "uwsgi --ini-paste uwsgi.ini"
}

function stop_spider() {
	ps -ef | grep [c]elery | awk '{print $2}' | xargs kill
	[ -f spider.pid ] && kill -INT $(cat uwsgi.pid) && rm *.pid
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
