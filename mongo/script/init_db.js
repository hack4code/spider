
/* password */
var scrapy_pwd="scrapy"
var flask_pwd="flask"

/* connect to admin */
var conn = new Mongo();
var db = null

db = conn.getDB("admin")
db.auth("admin", "admin")

/* articles db user */
db = conn.getDB("scrapy");
db.createUser({user: "scrapy",
	       pwd: scrapy_pwd,
	       roles: [ { role: "readWrite", db: "scrapy" } ]})

db.createUser({user: "flask",
	       pwd: flask_pwd,
	       roles: [ { role: "read", db: "scrapy" } ]})

/* score db user */
db = conn.getDB("score");
db.createUser({user: "flask",
	       pwd: flask_pwd,
	       roles: [ { role: "readWrite", db: "score" } ]})
