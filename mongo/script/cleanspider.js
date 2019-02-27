

const user = "scrapy";
const passwd = "scrapy";

var conn = new Mongo();
var db = conn.getDB("scrapy");
db.auth(user, passwd);

var cursor = db.scrapecount.aggregate(
	[
		{$match: {}},
		{$group: {_id: "$spider", total: {$sum: "$count"}}},
		{$sort: {total: 1}}
	]
)

var removedSpider = []
while (cursor.hasNext()) {
	spider = cursor.next();
	if (0 == spider["total"]) {
		removedSpider.push(spider["_id"]);
	}
}

removedSpider.forEach(function(item, index, array) {
	cursor = db.spider.find({_id: ObjectId(item)});
	if (cursor.hasNext()) {
		spider = cursor.next();
		db.discardspider.insert(spider);
		printjson(spider);
		db.spider.remove({_id: ObjectId(item)}, {justOne: true});
	};
	db.scrapecount.remove({spider: item}, {justOne: false});}
)
