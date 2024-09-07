from .db_connect import dbConnect

class CategoriesInfo:
    
    def __init__(self):
        self.db = dbConnect()
        
    def get_categories(self):
        query = "select name from categories"
        return self.db.execute_query(query)
    
# Sử dụng class ProductInfo
if __name__ == "__main__":
    categories_info =  CategoriesInfo()
    categories_info.get_categories()