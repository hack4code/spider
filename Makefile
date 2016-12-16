
clean:
	find . -iname '*.pyc' -exec sudo rm {} \;

update:
	docker pull nginx
	docker pull redis
	docker pull mongo
	docker pull python
	docker pull rabbitmq
