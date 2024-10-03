from db_connect import dbConnect
import datetime
import logging

class OrderInfo:
    def __init__(self):
        self.db = dbConnect()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def create_order(self, user_id, subtotal, shipping, discount_code, grand_total, payment_method, 
                     name, email, mobile, city, district, ward, address, notes, products):
        try:
            self.db.start_transaction()

            order_data = {
                "user_id": user_id,
                "subtotal": subtotal,
                "shipping": shipping,
                "discount_code": discount_code,
                "grand_total": grand_total,
                "payment_method": payment_method,
                "name": name,
                "email": email,
                "mobile": mobile,
                "city": city,
                "district": district,
                "ward": ward,
                "address": address,
                "notes": notes,
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

            self.add_user_address(user_id, name, email, mobile, city, district, ward, address)

            self.db.commit_transaction()
            self.logger.info(f"Order created successfully. Order ID: {order_id}")
            return order_id

        except Exception as e:
            self.db.rollback_transaction()
            self.logger.error(f"Error creating order: {str(e)}")
            raise

    def add_user_address(self, user_id, name, email, mobile, city, district, ward, address):
        try:
            query = "SELECT id FROM user_addresses WHERE user_id = %s AND address = %s"
            existing_address = self.db.fetch_one(query, (user_id, address))

            if not existing_address:
                address_data = {
                    "user_id": user_id,
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
                self.db.insert_data("user_addresses", address_data)
                self.logger.info(f"New address added for user {user_id}")
            else:
                self.logger.info(f"Address already exists for user {user_id}")

        except Exception as e:
            self.logger.error(f"Error adding user address: {str(e)}")
            raise