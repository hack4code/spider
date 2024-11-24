# Blog Spider

## Run
 * docker compose up --build -d

## Cron Job

### run spiders
 * curl -X POST -H "Content-Type: application/json" -d '{"spiders": ["all"]}' `http://127.0.0.1:8080/submit/crawl`

### backup mongo
  * docker-compose exec mongodb mongodump -u scrapy -p scrapy -d scrapy -c spider --gzip --archive=/dump/spider.gz

## React JS Build
  * docker container run --rm -v \`pwd\`/www/src/static/:/static/ -w /static/app/ node ./build.sh
