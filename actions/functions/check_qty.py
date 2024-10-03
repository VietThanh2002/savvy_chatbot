from .db_connect import dbConnect

class CheckQty:
    def __init__(self):
        self.db = dbConnect()
    
    def check_qty(self, product_name):
        query = "SELECT p.name, i.quantity FROM products p JOIN inventory i ON i.product_id = p.id WHERE p.name LIKE %s AND i.quantity >= 0"
        product_name = f"%{product_name}%"
        return self.db.execute_query(query, (product_name,))

    
if __name__ == "__main__":
    check_qty = CheckQty()
    check_qty.check_qty("Áo thun nam")
