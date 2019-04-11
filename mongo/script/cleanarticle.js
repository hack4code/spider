const user = "scrapy";
const passwd = "scrapy";

var conn = new Mongo();
var db = conn.getDB("scrapy");
db.auth(user, passwd);

var total = db.article.find({}).count();
print("total articles count: ", total);

var remove_article_ids = [];
var cursor = db.article.find({}, {spider: 1});
while (cursor.hasNext()) {
	article = cursor.next();
	article_id = article["_id"];
	spider_id = article["spider"];
	count = db.spider.find({_id: ObjectId(spider_id)}).count();
	if (0 == count) {
		remove_article_ids.push(article_id);
	}
}

size = remove_article_ids.length;
print("removed articles count: ", size);
for (var i=0; i < size; i++) {
	article_id = remove_article_ids[i];
	db.article.remove({_id: article_id}, {justOne: true});
}
