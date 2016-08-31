
/* password admin */
var admin_pwd="admin"

var db = null

/* connect to mongodb */
var conn = new Mongo();

/* create admin user */
db = conn.getDB("admin")
db.createUser({user: "admin",
	       pwd: admin_pwd,
	       roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]})
