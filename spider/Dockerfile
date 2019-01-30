FROM python:3.6

RUN mkdir /spider/
ADD requirements.txt /spider/requirements.txt
ADD wait-for-it.sh /spider/wait-for-it.sh
WORKDIR /spider/

RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev python3-setuptools
RUN apt-get install -y libffi-dev libxml2-dev libxslt1-dev libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libopenjp2-7-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod a+x wait-for-it.sh