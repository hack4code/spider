FROM python:3.5

ADD . /www/
WORKDIR /www

RUN pip install --proxy http://103.55.27.122:8888 -r requirements.txt
RUN adduser --disabled-password --gecos '' www
RUN mkdir /var/log/www/
RUN chown www:www /var/log/www
RUN mkdir /var/run/www/
RUN chown www:www /var/run/www
# RUN sed -i "s;mongodb://[0-9.]\+;mongodb://mongodb;;" app.py
# RUN sed -i "s;http://[0-9.]\+;http://spider;;" app.py
