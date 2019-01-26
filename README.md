# Blog Spider

## Init

### javascript
  * docker container run --rm -v \`pwd\`/www/static/app/:/app/ -w /app/ node ./build.sh

### mongodb
  * docker container run --rm -d --name tmp-mongo -v \`pwd\`/mongo/script/:/script -v \`pwd\`/mongo/data:/data/db/ mongo --auth --storageEngine wiredTiger
  * docker container exec -w /script/ tmp-mongo mongo init\_admin.js
  * docker container exec -w /script/ tmp-mongo mongo init\_db.js
  * docker container stop tmp-mongo
  * sudo chown -R $USER:$USER mongo/data/

## Run
 * docker-compose up --build -d

## Cron Job
 * curl -X POST -d "spiders=all" `http://127.0.0.1:8080/submit/crawl`
