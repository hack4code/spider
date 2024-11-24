/* password */
const scrapy_pwd="scrapy"
const flask_pwd="flask"

/* connect to admin */
var conn = new Mongo();
var db = null

db = conn.getDB("admin")
db.auth("admin", "admin")

/* create user scrapy */
db = conn.getDB("scrapy");
db.createUser(
	{
		user: "scrapy",
		pwd: scrapy_pwd,
		roles: [ { role: "readWrite", db: "scrapy" } ]
	}
)

/* create user flask */
db.createUser(
	{
		user: "flask",
		pwd: flask_pwd,
		roles: [ { role: "read", db: "scrapy" } ]
	}
)
