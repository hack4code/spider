FROM python

RUN mkdir /spider

COPY requirements.txt /spider/
COPY src /spider/src
COPY protos /spider/protos

RUN apt-get update -y --fix-missing
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev python3-setuptools
RUN apt-get install -y libwebp-dev libpng-dev

WORKDIR /spider/

RUN pip install --upgrade pip
# RUN pip install pillow --global-option="build_ext" --global-option="--enable-zlib" --global-option="--enable-jpeg" --global-option="--enable-webp" --global-option="--enable-jpeg2000"
RUN pip install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I protos/ --python_out=src/ --grpc_python_out=src/ spider.proto
