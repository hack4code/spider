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
 * docker-compose exec mongodb mongo /script/init_admin.js
 * docker-compose exec mongodb mongo /script/init_db.js

### www
 * cd www/
 * docker-compose build

## RUN
### spider
 * cd spider/
 * docker-compose up

## www
 * cd www/
 * docker-compose up

