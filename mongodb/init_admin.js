var conn = new Mongo();
var db = null

/* admin */
db = conn.getDB("admin")
db.createUser({user: "admin",
	       pwd: "admin",
	       roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]})
