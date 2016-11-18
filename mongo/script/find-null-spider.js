const user = "flask";
const passwd = "flask";

var conn = new Mongo();
var db = conn.getDB("articles");
db.auth(user, passwd);

function find_article(spid) {
	var cursor = db.article.find({spider: spid}).limit(1);
	return cursor.hasNext();
};

var cursor = db.spider.find({});
while (cursor.hasNext()) {
	const sp = cursor.next();
	const spid = sp["_id"].str;
	if (!find_article(spid)) {
		printjson(sp);
		print("----------------------");
	}
}
