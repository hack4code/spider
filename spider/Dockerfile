FROM python:2.7

ADD . /spider
WORKDIR /spider

RUN pip install --proxy http://103.55.27.122:8888 -r requirements.txt
RUN adduser --disabled-password --gecos '' spider
RUN mkdir /var/log/spider
RUN chown spider:spider /var/log/spider
RUN mkdir /var/run/spider
RUN chown spider:spider /var/run/spider
# RUN sed -i "s;mongodb://[0-9.]\+;mongodb://mongodb;;" mydm/settings.py
# RUN sed -i "s;redis://[0-9.]\+;redis://redis;;" mydm/settings.py
