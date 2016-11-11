# Blog Spider

## IMAGES
* rabbitmq
* redis
* python
* nginx
* mongo

## INIT
 * docker-compose build

## RUN
 * docker-compose up -d

## mongodb
First time, should create users of mongodb
 * docker-compose exec mongodb mongo /script/init_admin.js
 * docker-compose exec mongodb mongo /script/init_db.js

## TODO
### spider
  * tag: html2txt
