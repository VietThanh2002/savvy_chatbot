from db_connect import dbConnect
import datetime

class OrderInfo:
    def __init__(self):
        self.db = dbConnect()

    def create_order(self, user_id, subtotal, shipping, discount_code, grand_total, payment_method, 
                     name, email, mobile, city, district, ward, address, notes, products):
        # Tạo đơn hàng mới
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

        # Tạo chi tiết đơn hàng
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

            # Cập nhật stock_out
            stock_out_data = {
                "order_id": order_id,
                "product_id": product['id'],
                "quantity": product['quantity'],
                "stock_out_date": datetime.datetime.now(),
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()
            }
            self.db.insert_data("stock_out", stock_out_data)

        # Thêm địa chỉ mới vào user_addresses nếu cần
        self.add_user_address(user_id, name, email, mobile, city, district, ward, address)

        return order_id

    def add_user_address(self, user_id, name, email, mobile, city, district, ward, address):
        # Kiểm tra xem địa chỉ đã tồn tại chưa
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