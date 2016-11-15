const user = "flask";
const passwd = "flask";

const conn = new Mongo();
const db = conn.getDB("articles");
db.auth(user, passwd);

const cursor = db.feed.find({});
while (cursor.hasNext()) {
	printjson(cursor.next());
}




