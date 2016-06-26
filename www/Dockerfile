FROM python:3.5

ADD . /www/
WORKDIR /www

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' www
RUN mkdir /var/log/www/
RUN chown www:www /var/log/www
RUN mkdir /var/run/www/
RUN chown www:www /var/run/www
