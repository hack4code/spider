FROM python

RUN mkdir /spider/
COPY requirements.txt /spider/

RUN apt-get update -y --fix-missing
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev python3-setuptools
# RUN apt-get install -y libffi-dev libxml2-dev libxslt1-dev libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libopenjp2-7-dev libpng-dev

WORKDIR /spider/
RUN pip install --upgrade pip
# RUN pip install pillow --global-option="build_ext" --global-option="--enable-zlib" --global-option="--enable-jpeg" --global-option="--enable-tiff" --global-option="--enable-freetype" --global-option="--enable-webp" --global-option="--enable-jpeg2000"
RUN pip install pillow
RUN pip install -r requirements.txt
