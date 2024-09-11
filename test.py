from actions.functions.db_connect import dbConnect

db = dbConnect()

query = "SELECT name FROM products"

# query = "SELECT name FROM categories"

# query = "SELECT name FROM sub_categories"

db.execute_query(query)