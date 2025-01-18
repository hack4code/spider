# Blog Spider

## Cron Job

### run spiders
 * curl -X POST -H "Content-Type: application/json" -d '{"spiders": ["all"]}' `http://127.0.0.1:8080/submit/crawl`

### backup mongo
  * docker-compose exec mongodb mongodump --username scrapy --password scrapy --db scrapy --collection spider --gzip --archive=/dump/spider.gz

### restore mongo
  * docker compose exec mongodb mongorestore --gzip --archive=/dump/spider.gz --db scrapy --collection spider --username scrapy --password scrapy
