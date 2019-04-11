const user = "flask";
const passwd = "flask";

var conn = new Mongo();
var db = conn.getDB("scrapy");
db.auth(user, passwd);

var cursor = db.spider.find({start_urls: {$regex: regex}});
if (cursor.count() > 0) {
	while (cursor.hasNext()) {
		spider = cursor.next();
		printjson(spider);
		print(" ");
	}
}
else {
	var cursor = db.spider.find({name: {$regex: regex}});
	while (cursor.hasNext()) {
		spider = cursor.next();
		printjson(spider);
		print(" ");
	}
}
