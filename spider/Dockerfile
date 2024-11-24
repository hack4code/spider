FROM python

RUN mkdir /spider/
COPY requirements.txt /spider/

RUN apt-get update -y --fix-missing
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev python3-setuptools
RUN apg-get install -y libwebp libpng libjpeg

WORKDIR /spider/
RUN pip install --upgrade pip
RUN pip install pillow --global-option="build_ext" --global-option="--enable-zlib" --global-option="--enable-jpeg" --global-option="--enable-webp" --global-option="--enable-jpeg2000"
# RUN pip install pillow
RUN pip install -r requirements.txt
