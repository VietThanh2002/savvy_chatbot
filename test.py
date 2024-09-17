from actions.functions.db_connect import dbConnect

db = dbConnect()

# query = "SELECT name FROM products"

# query = "SELECT name FROM categories"

# query = "SELECT name FROM sub_categories"

# query = "SELECT shipping_fee FROM shipping_cost"

query = "select count(id) from discount_coupons where status = 1"

db.execute_query(query) 