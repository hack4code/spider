/* password */
const scrapy_pwd="scrapy"

/* connect to admin */
var conn = new Mongo();

var admin_db = conn.getDB("admin")
admin_db.auth("admin", "admin")

/* create user scrapy */
var scrapy_db = conn.getDB("scrapy");
scrapy_db.createUser(
	{
		user: "scrapy",
		pwd: scrapy_pwd,
		roles: [ { role: "readWrite", db: "scrapy" } ]
	}
)
