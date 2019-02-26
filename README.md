# Blog Spider

## Run
 * docker-compose up --build -d

## Cron Job

### run all spiders to crawl data
 * curl -X POST -H "Content-Type: application/json" -d '{"spiders": ["all"]}' `http://127.0.0.1:8080/submit/crawl`

### mongodb collections backup
  * docker-compose exec mongodb mongodump -u scrapy -p scrapy -d scrapy -c spider --gzip --archive=/dump/spider.gz
  * docker-compose exec mongodb mongodump -u scrapy -p scrapy -d scrapy -c category --gzip --archive=/dump/category.gz

### javascript
  * docker container run --rm -v \`pwd\`/www/src/static/app/:/app/ -w /app/ node ./build.sh
