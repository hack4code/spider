FROM python

RUN mkdir /www/
ADD requirements.txt /www/requirements.txt

RUN apt-get update -y

WORKDIR /www/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
