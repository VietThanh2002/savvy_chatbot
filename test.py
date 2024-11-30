from actions.functions.db_connect import dbConnect

db = dbConnect()

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

# lấy sản phẩm bán chạy nhất
query = """SELECT p.id, p.name, p.slug, p.price, SUM(oi.qty) AS total_sold,
            (SELECT pi.image
            FROM product_images pi
            WHERE pi.product_id = p.id
            ORDER BY pi.id ASC
            LIMIT 1) AS first_image
            
            FROM products p
            JOIN order_details oi ON p.id = oi.product_id
            GROUP BY p.id, p.name, p.price
            ORDER BY total_sold DESC
            LIMIT 1;
         """

# sản phẩm giá thấp nhất
# query = """SELECT p.id, p.name, p.slug, p.price,
#             (SELECT pi.image
#                 FROM product_images pi
#                 WHERE pi.product_id = p.id
#                 ORDER BY pi.id ASC
#                 LIMIT 1) AS first_image
#             FROM products p  
#             WHERE p.price > 0
#             ORDER BY p.price ASC
#             LIMIT 1;
#           """

# sản phẩm giá cao nhất
# query = """SELECT p.id, p.name, p.slug, p.price,
#             (SELECT pi.image
#                 FROM product_images pi
#                 WHERE pi.product_id = p.id
#                 ORDER BY pi.id ASC
#                 LIMIT 1) AS first_image
#             FROM products p  
#             WHERE p.price > 0
#             ORDER BY p.price DESC
#             LIMIT 1;
#          """

# sản phẩm được yêu thích nhất
# query = """SELECT p.id, p.name, p.price, COUNT(w.product_id) AS total_wishlist,
#             (SELECT pi.image
#                 FROM product_images pi
#                 WHERE pi.product_id = p.id
#                 ORDER BY pi.id ASC
#                 LIMIT 1) AS first_image
#             FROM products p
#             LEFT JOIN wishlists w ON p.id = w.product_id
#             GROUP BY p.id, p.name, p.price
#             ORDER BY COUNT(w.product_id) DESC
#             LIMIT 1;
#             """
            
 
db.execute_query(query) 

# string = 'Áo giáp bảo hộ nam Alpinestar HONDA T-SP-1'

# print(string.lower())