

const user = "scrapy";
const passwd = "scrapy";

var conn = new Mongo();
var db = conn.getDB("scrapy");
db.auth(user, passwd);

db.spider.remove({_id: ObjectId(spid)})
