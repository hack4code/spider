FROM python:3.5

# RUN export http_proxy="http://103.55.27.122:8888"

RUN mkdir /www/
ADD ./requirements.txt /www/requirements.txt
WORKDIR /www
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' www
RUN mkdir /var/log/www/
RUN chown www:www /var/log/www
RUN mkdir /var/run/www/
RUN chown www:www /var/run/www
