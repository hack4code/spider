FROM python

RUN mkdir /www/
COPY requirements.txt /www/

RUN apt-get update -y

WORKDIR /www/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
