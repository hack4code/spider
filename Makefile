
clean:
	find . -iname '*.pyc' -exec rm {} \;

update:
	docker pull nginx
	docker pull redis
	docker pull mongo
	docker pull python
	docker pull python:2.7
