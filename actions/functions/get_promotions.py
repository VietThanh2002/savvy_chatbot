from .db_connect import dbConnect

class PromotionsInfo:
    def __init__(self):
        self.db = dbConnect()
    
    def get_promotions(self):
        query = "select count(id) from discount_coupons where status = 1"
        return self.db.execute_query(query)
    
# if __name__ == "__main__":
#     print(PromotionsInfo().get_promotions())