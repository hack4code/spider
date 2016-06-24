FROM python:3.5

ADD . /www/
WORKDIR /www

RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' www
RUN mkdir /var/log/www/
RUN chown www:www /var/log/www
RUN mkdir /var/run/www/
RUN chown www:www /var/run/www
RUN sed -i "s;mongodb://[0-9.]\+;mongodb://mongodb;;" app.py
RUN sed -i "s;http://[0-9.]\+;http://spider;;" app.py
