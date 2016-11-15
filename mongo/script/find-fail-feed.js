const user = "flask";
const passwd = "flask";

var conn = new Mongo();
var db = conn.getDB("articles");
db.auth(user, passwd);


function find_feed_spider(url) {
	var cursor = db.spider.find({start_urls: {$in: [url,]}});
	return cursor.hasNext() ? true : false;
}

var cursor = db.feed.find({});
while (cursor.hasNext()) {
	const feed = cursor.next();
	const url = feed["url"];
	if (!find_feed_spider(url)) {
		print(url);
	}
}




