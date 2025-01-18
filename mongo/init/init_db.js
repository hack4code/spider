/* connect to admin */
var conn = new Mongo();

var admin_db = conn.getDB("admin")
admin_db.auth("admin", "admin")

var scrapy_db = conn.getDB("scrapy");
scrapy_db.createUser(
	{
		user: "scrapy",
		pwd: "scrapy",
		roles: [ { role: "readWrite", db: "scrapy" } ]
	}
)

scrapy_db.createUser(
	{
		user: "flask",
		pwd: "flask",
		roles: [ { role: "read", db: "scrapy" } ]
	}
)
