FROM python:2.7

# ENV http_proxy http://103.55.27.122:8888
# ENV https_proxy http://103.55.27.122:8888

RUN mkdir /spider/
ADD ./requirements.txt /spider/requirements.txt
WORKDIR /spider

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev python-setuptools
RUN apt-get install -y libffi-dev libxml2-dev libxslt1-dev libtiff5 libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' spider
RUN mkdir /var/log/spider
RUN chown spider:spider /var/log/spider
RUN mkdir /var/run/spider
RUN chown spider:spider /var/run/spider
