# IP := $(shell ip -4 -o a s | awk '$$2!~/lo/ {print $$4; exit;}' | cut -d/ -f1)

nginx:
	@echo "start nginx..."
	@pgrep nginx &>/dev/null || sudo rc-service nginx start

mongodb:
	@echo "start mongodb..."
	@pgrep mongod &>/dev/null || sudo rc-service mongodb start
	@sleep 2

run: nginx mongodb
	bash -c "source env/bin/activate; \
	uwsgi --ini-paste uwsgi.ini; \
	deactivate"

test: mongodb
	bash -c "source env/bin/activate; \
	python test.py; \
	deactivate"

clean:
	find . -iname '*.pyc' -exec rm {} \;
	find . -iname "__pycache__" -exec rm -r {} \;

stop:
	@if [[ -e /run/uwsgi.pid ]]; then \
		kill -INT $$(cat /run/uwsgi.pid); \
		rm run/uwsgi.pid; \
	fi
	@if [[ -e /run/*.log ]]; then \
		@rm run/*.log; \
	fi
	@if (pgrep mongod &> /dev/null); then \
		sudo rc-service mongodb stop; \
	fi
	@if (pgrep nginx &> /dev/null); then \
		sudo rc-service nginx stop; \
	fi

update:
	bash -c 'source env/bin/activate; \
	cat requirements.txt | cut -d= -f1 | while read package; do \
		pip install -U $${package}; \
	done; \
	deactivate;'

.PHONY: run test clean stop update nginx mongodb
