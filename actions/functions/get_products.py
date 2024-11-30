from .db_connect import dbConnect

class ProductInfo:
    
    def __init__(self):
        self.db = dbConnect()
        
    def get_products_all(self):
        query = "select name, price from products"
        return self.db.execute_query(query)
    
    # Lấy sản phẩm bán chạy nhất
    def get_best_selling_products(self):
        query = """SELECT p.name, p.slug, p.price, SUM(oi.qty) AS total_sold,
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
        return self.db.execute_query(query)
    
    # Lấy sản phẩm giá thấp nhất
    def get_cheapest_product(self):
        query = """SELECT p.name, p.slug, p.price,
                    (SELECT pi.image
                        FROM product_images pi
                        WHERE pi.product_id = p.id
                        ORDER BY pi.id ASC
                        LIMIT 1) AS first_image
                    FROM products p  
                    WHERE p.price > 0
                    ORDER BY p.price ASC
                    LIMIT 2;
                 """
        return self.db.execute_query(query)

    # Lấy sản phẩm giá cao nhất
    def get_most_expensive_product(self):
        query = """SELECT p.name, p.slug, p.price,
                    (SELECT pi.image
                        FROM product_images pi
                        WHERE pi.product_id = p.id
                        ORDER BY pi.id ASC
                        LIMIT 1) AS first_image
                    FROM products p  
                    WHERE p.price > 0
                    ORDER BY p.price DESC
                    LIMIT 1;
                 """
        return self.db.execute_query(query)
    
    # Lấy sản phẩm được yêu thích nhất
    def get_most_favorited_product(self):
        query = """SELECT p.name, p.slug, p.price, COUNT(w.product_id) AS total_wishlist,
                    (SELECT pi.image
                        FROM product_images pi
                        WHERE pi.product_id = p.id
                        ORDER BY pi.id ASC
                        LIMIT 1) AS first_image
                    FROM products p
                    LEFT JOIN wishlists w ON p.id = w.product_id
                    GROUP BY p.id, p.name, p.price
                    ORDER BY COUNT(w.product_id) DESC
                    LIMIT 1;
                 """
        return self.db.execute_query(query)
    
    
    def get_products_by_category_and_subcategory(self, category_name):
        query = """
                SELECT p.name, p.slug, p.price, 
                (SELECT pi.image 
                        FROM product_images pi 
                        WHERE pi.product_id = p.id 
                        ORDER BY pi.id ASC 
                        LIMIT 1) AS first_image,
                i.quantity 
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN sub_categories sc ON p.sub_category_id = sc.id
                LEFT JOIN inventory i ON i.product_id = p.id
                WHERE c.name LIKE %s OR sc.name LIKE %s
                """
        category_pattern = f"%{category_name}%"
        return self.db.execute_query(query, (category_pattern, category_pattern))

    def get_products_by_name(self, name):
        name = f"%{name}%"
        query = """ SELECT p.name, p.slug, p.price,
                    (SELECT pi.image 
                        FROM product_images pi 
                        WHERE pi.product_id = p.id 
                        ORDER BY pi.id ASC 
                        LIMIT 1) AS first_image,
                    i.quantity
                    FROM products p
                    LEFT JOIN inventory i ON i.product_id = p.id
                    WHERE p.name LIKE LOWER(%s)"""
        return self.db.execute_query(query, (name,))
    
    
    def get_products_by_category_and_name(self, category_name, product_name):
        query = """
                SELECT p.name, p.slug, p.price, c.name as category, COALESCE(sc.name, 'N/A') as subcategory,
                (SELECT pi.image 
                        FROM product_images pi 
                        WHERE pi.product_id = p.id 
                        ORDER BY pi.id ASC 
                        LIMIT 1) AS first_image,
                i.quantity
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN sub_categories sc ON p.sub_category_id = sc.id
                LEFT JOIN inventory i ON i.product_id = p.id
                WHERE (c.name LIKE %s OR sc.name LIKE %s OR %s IS NULL)
                AND (p.name LIKE %s OR %s IS NULL)
                """
        # Tạo pattern để khớp với tên danh mục và tên sản phẩm
        category_pattern = f"%{category_name}%" if category_name else None
        product_pattern = f"%{product_name}%" if product_name else None
        
        # Thực hiện truy vấn với thứ tự danh mục trước, sản phẩm sau
        return self.db.execute_query(query, (category_pattern, category_pattern, category_name, product_pattern, product_name))

    # def get_product_price(self, name):
    #     name = f"%{name}%"
    #     query = "select price from products where name like %s"
    #     result = self.db.execute_query(query, (name,))
    #     # Giả sử execute_query trả về danh sách các tuple
    #     return result[0][0] if result else None
    
        
if __name__ == "__main__":
    product_info = ProductInfo()
    product_info.get_products_by_name("Nhớt")
    # product_info.get_products_by_category_and_name("Lọc gió", "SH350")
    # product_info.get_products_by_category_and_subcategory("Nhớt xe số")