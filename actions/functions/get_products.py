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
    
    def get_products_by_name_and_category(self, product_name, category_name):
        query = """
                SELECT p.name, p.price, c.name as category, COALESCE(sc.name, 'N/A') as subcategory
                FROM products p
                JOIN categories c ON p.category_id = c.id
                LEFT JOIN sub_categories sc ON p.sub_category_id = sc.id
                WHERE (p.name LIKE %s OR %s IS NULL)
                AND (c.name LIKE %s OR sc.name LIKE %s OR %s IS NULL)
                """
        product_pattern = f"%{product_name}%" if product_name else None
        category_pattern = f"%{category_name}%" if category_name else None
        
        return self.db.execute_query(query, (product_pattern, product_name, category_pattern, category_pattern, category_name))
    
        
if __name__ == "__main__":
    product_info = ProductInfo()
    # product_info.get_products_by_name("AB")
    # product_info.get_products_by_name_and_category("AB", "Lọc gió")
    product_info.get_products_by_category_and_subcategory("Nhớt xe số")