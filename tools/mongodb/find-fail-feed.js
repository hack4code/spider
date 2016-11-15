const user = "flask";
const passwd = "flask";

const conn = new Mongo();
var db = conn.getDB("articles");
db.auth(user, passwd);

var cursor = db.feed.find({});
while (cursor.hasNext()) {
	printjson(cursor.next());
}




