FROM python


RUN mkdir /www/

COPY requirements.txt /www/
COPY uwsgi.ini /www/
COPY src /www/src
COPY protos /www/protos

RUN apt-get update -y

WORKDIR /www/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I protos/ --python_out=src/ --grpc_python_out=src/ spider.proto
