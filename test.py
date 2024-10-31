from actions.functions.db_connect import dbConnect

# db = dbConnect()

# query = """SELECT p.name, i.quantity  FROM products p
#         JOIN inventory i ON i.product_id = p.id WHERE i.quantity >= 0"""

# # query = "SELECT id FROM products"

# # query = "SELECT name FROM categories"

# # query = "SELECT name FROM sub_categories"

# # query = "SELECT shipping_fee FROM shipping_cost"

# # query = "select count(id) from discount_coupons where status = 1"
# # query = """SELECT o.id, o.status 
# #             FROM orders o
# #             JOIN users u ON o.user_id = u.id 
# #             WHERE u.email = 'vthanh2410@gmail.com'
# #         """

# # query = """ SELECT p.name, p.slug, p.price, 
# #        (SELECT pi.image 
# #         FROM product_images pi 
# #         WHERE pi.product_id = p.id 
# #         ORDER BY pi.id ASC 
# #         LIMIT 1) AS first_image
# #         FROM products p
# #         WHERE p.name  LIKE '%Áo giáp bảo hộ nam Alpinestar HONDA T-SP-1%'
# #         """


 
# db.execute_query(query) 
string = 'Áo giáp bảo hộ nam Alpinestar HONDA T-SP-1'

print(string.lower())