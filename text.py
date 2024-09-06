from actions.functions.db_connect import dbConnect

db = dbConnect()

query = "SELECT id, name, slug FROM products"

db.execute_query(query)