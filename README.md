## [Spider]

### React
#### Bundle js with webpack
  * cd www/static/app/
  * docker run --rm -v `pwd`:/app/ -w /app/ node ./build.sh

### Init
 * docker-compose build

### Run
 * docker-compose up -d

### Mongodb

#### First time, should create users of mongodb
  * docker-compose exec mongodb mongo /script/init\_admin.js
  * docker-compose exec mongodb mongo /script/init\_db.js

### Cron job
 * curl -X POST -d "spiders=all" http://localhost/submit/crawl
