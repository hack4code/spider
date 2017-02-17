
clean:
	find . -iname '*.pyc' -exec sudo rm {} \;
	sudo rm -rf /var/cache/nginx

update:
	docker pull nginx:stable-alpine
	docker pull redis
	docker pull mongo
	docker pull python
	docker pull rabbitmq
