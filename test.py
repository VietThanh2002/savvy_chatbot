from actions.functions.db_connect import dbConnect

db = dbConnect()

# query = """SELECT p.name, i.quantity  FROM products p
#         JOIN inventory i ON i.product_id = p.id WHERE i.quantity >= 0"""

# query = "SELECT count(id) FROM products"

# query = "SELECT name FROM categories"

# query = "SELECT name FROM sub_categories"

# query = "SELECT shipping_fee FROM shipping_cost"

# query = "select count(id) from discount_coupons where status = 1"
query = """SELECT o.id, o.status 
            FROM orders o
            JOIN users u ON o.user_id = u.id 
            WHERE u.email = 'vthanh2410@gmail.com'
        """



 
db.execute_query(query) 