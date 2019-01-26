# Blog Spider

## Init

### js
  * cd www/static/app/
  * docker run --rm -v `pwd`:/app/ -w /app/ node ./build.sh

### mongodb
  * mkdir mongo/data
  * docker run --rm -v `pwd`/mongo/script/:/script `pwd`/mongo/data:/data/db/ mongo cd /script/ && mongo init\_admin.js && mongo init\_db.js
  * sudo chown -R $USER:$USER mongo/data/

## Run
 * docker-compose up -d

## Cron job
 * curl -X POST -d "spiders=all" http://127.0.0.1/submit/crawl
