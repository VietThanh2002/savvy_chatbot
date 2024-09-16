from .db_connect import dbConnect

class ProductInfo:
    
    def __init__(self):
        self.db = dbConnect()
        
    def get_products_all(self):
        query = "select name, price from products"
        return self.db.execute_query(query)
    
    def get_products_by_category_and_subcategory(self, category_name):
        query = """
                SELECT p.name, p.price 
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN sub_categories sc ON p.sub_category_id = sc.id
                WHERE c.name LIKE %s OR sc.name LIKE %s
                """
        category_pattern = f"%{category_name}%"
        return self.db.execute_query(query, (category_pattern, category_pattern))

    def get_products_by_name(self, name):
        name = f"%{name}%"
        query = "select name, price from products where name like %s"
        return self.db.execute_query(query, (name,))
    
    def get_products_by_category_and_subcategory(self, category_name):
        query = """
                SELECT p.name, p.price 
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN sub_categories sc ON p.sub_category_id = sc.id
                WHERE c.name LIKE %s OR sc.name LIKE %s
                """
        category_pattern = f"%{category_name}%"
        return self.db.execute_query(query, (category_pattern, category_pattern))
    
    def get_products_by_category_and_name(self, category_name, product_name):
        query = """
                SELECT p.name, p.price, c.name as category, COALESCE(sc.name, 'N/A') as subcategory
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN sub_categories sc ON p.sub_category_id = sc.id
                WHERE (c.name LIKE %s OR sc.name LIKE %s OR %s IS NULL)
                AND (p.name LIKE %s OR %s IS NULL)
                """
        # Tạo pattern để khớp với tên danh mục và tên sản phẩm
        category_pattern = f"%{category_name}%" if category_name else None
        product_pattern = f"%{product_name}%" if product_name else None
        
        # Thực hiện truy vấn với thứ tự danh mục trước, sản phẩm sau
        return self.db.execute_query(query, (category_pattern, category_pattern, category_name, product_pattern, product_name))

    def get_product_price(self, name):
        name = f"%{name}%"
        query = "select price from products where name like %s"
        result = self.db.execute_query(query, (name,))
        # Giả sử execute_query trả về danh sách các tuple
        return result[0][0] if result else None
        
if __name__ == "__main__":
    product_info = ProductInfo()
    # product_info.get_products_by_name("AB")
    product_info.get_products_by_category_and_name("bugi", "future")
    # product_info.get_products_by_category_and_subcategory("Nhớt xe số")