from db_connect import dbConnect
import datetime
import logging

class OrderInfo:
    def __init__(self):
        self.db = dbConnect()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def create_order(self, subtotal, grand_total, payment_method, 
                     name, email, mobile, city, district, ward, address, notes, products):
        try:
            self.db.start_transaction()

            order_data = {
                "subtotal": subtotal,
                "grand_total": grand_total,
                "payment_method": payment_method,
                "name": name,
                "email": email,
                "mobile": mobile,
                "city": city,
                "district": district,
                "ward": ward,
                "address": address,
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()
            }

            order_id = self.db.insert_data("orders", order_data)

            for product in products:
                order_detail_data = {
                    "order_id": order_id,
                    "product_id": product['id'],
                    "name": product['name'],
                    "qty": product['quantity'],
                    "size": product.get('size'),
                    "price": product['price'],
                    "total": product['price'] * product['quantity'],
                    "created_at": datetime.datetime.now(),
                    "updated_at": datetime.datetime.now()
                }
                self.db.insert_data("order_details", order_detail_data)

                stock_out_data = {
                    "order_id": order_id,
                    "product_id": product['id'],
                    "quantity": product['quantity'],
                    "stock_out_date": datetime.datetime.now(),
                    "created_at": datetime.datetime.now(),
                    "updated_at": datetime.datetime.now()
                }
                self.db.insert_data("stock_out", stock_out_data)

            self.db.commit_transaction()
            self.logger.info(f"Order created successfully. Order ID: {order_id}")
            return order_id

        except Exception as e:
            self.db.rollback_transaction()
            self.logger.error(f"Error creating order: {str(e)}")
            raise

