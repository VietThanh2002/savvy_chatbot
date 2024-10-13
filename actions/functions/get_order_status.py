from db_connect import dbConnect

class OrderStatus:
        
        def __init__(self):
            self.db = dbConnect()
            
        def get_order_status_by_user_email(self, email, order_id):
            query = f"""SELECT o.id, o.status 
                        FROM orders o
                        JOIN users u ON o.user_id = u.id 
                        WHERE u.email = '{email}' AND o.id = {order_id}
                    """
            return self.db.execute_query(query)

if __name__ == "__main__":
    order = OrderStatus()
    print(order.get_order_status_by_user_email('vthanh2410@gmail.com', 2))

        