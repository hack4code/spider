
clean:
	find . -iname '*.pyc' -exec sudo rm {} \;
	sudo rm -rf /var/cache/nginx

update:
	docker pull nginx
	docker pull redis
	docker pull mongo
	docker pull python
	docker pull rabbitmq
