SHELL := /bin/bash
kill := /bin/kill

redis:
	pgrep redis &>/dev/null || sudo rc-service redis start

mongodb:
	pgrep mongod &> /dev/null || sudo rc-service mongodb start

run: redis mongodb
	bash -c "source env/bin/activate; \
	celery multi start spiderjob -A task.spider --pidfile=run/spider.pid --logfile=run/spider.log --loglevel=INFO; \
	uwsgi --ini-paste uwsgi.ini; \
	deactivate"

update:
	bash -c 'source env/bin/activate; \
	cat requirements.txt | cut -d= -f1 | while read package; do \
		pip install -U $${package}; \
	done; \
	deactivate'

stop:
	@echo "kill celery"
	@if [[ -e /run/spider.pid ]]; then \
		ps -ef | grep [c]elery | awk '{print $$2}' | xargs ${kill}; \
	fi
	@echo "kill uwsgi"
	@if [[ -e /run/uwsgi-spider.pid ]]; then \
		${kill} -INT $$(cat /run/uwsgi-spider.pid); \
		rm /run/uwsgi-spider.pid; \
	fi
	# @sudo rc-service mongodb stop
	# @sudo rc-service redis stop
	
	

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	rm *.pid

# docker

docker-run:
	su -m spider -c "celery multi start spiderjob -A task.spider --pidfile=spider.pid --logfile=/run/spider.log --loglevel=INFO"
	su -m spider -c "uwsgi --ini-paste uwsgi.ini"

docker-stop:
	ps -ef | grep [c]elery | awk '{print $$2}' | xargs kill
	kill -INT $$(cat uwsgi.pid) 
	rm *.pid

.PHONY: clean update run stop redis mongodb docker-run docker-stop
