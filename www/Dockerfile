FROM python

RUN mkdir /www/
ADD requirements.txt /www/requirements.txt
WORKDIR /www/

RUN apt-get update -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
