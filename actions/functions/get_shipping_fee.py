from .db_connect import dbConnect

class ShippingFee:
    
    def __init__(self):
        self.db = dbConnect()
        
    def get_shippingFee_info(self, city_province):
        city_province = f"%{city_province}%"
        query = "select shipping_fee from shipping_cost where city_province like %s"
        
        result = self.db.execute_query(query, (city_province,))

        return result[0][0] if result else None
    # def get_shippingFee_info(self, city_province):
    #     query = "SELECT city_province, shipping_fee FROM shipping_cost WHERE city_province LIKE %s"

    #     search_term = f"%{city_province}%"
        
    #     return self.db.execute_query(query, (search_term,))
    

if __name__ == "__main__":
    shipping_info = ShippingFee()
    shipping_info.get_shippingFee_info("đồng")
    