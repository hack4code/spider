# Blog Spider

## IMAGES
* mongo
* redis
* python
* nginx

## INIT
### spider
 * cd spider/
 * docker-compose build

### www
 * cd www/
 * docker-compose build

## RUN
### spider
 * cd spider/
 * docker-compose up -d

## www
 * cd www/
 * docker-compose up -d

## mongodb
First time, should create users of mongodb
 * docker-compose exec mongodb mongo /script/init_admin.js
 * docker-compose exec mongodb mongo /script/init_db.js
