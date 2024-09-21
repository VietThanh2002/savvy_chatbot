# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.functions.db_connect import dbConnect
from actions.functions.format_price import PriceFormatter
from actions.functions.get_categories import CategoriesInfo
from actions.functions.get_products import ProductInfo
from actions.functions.get_shipping_fee import ShippingFee
from actions.functions.get_promotions import PromotionsInfo

class action_custom_fallback(Action):
    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Xin lỗi, em không hiểu yêu cầu của anh/chị. Anh chị có thể thử lại không ?")
        
        return []


class action_return_bot_functions(Action):

    def name(self) -> Text:
        return "action_return_bot_functions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Danh sách chức năng của bot
        bot_functions = [
            "Tư vấn thay lọc gió",
            "Tư vấn thay nhớt",
            "Tư vấn chọn bugi",
            "Tư vấn chọn size áo, nón bảo hộ",
            "Thông tin giá cả của sản phẩm",
            "Thông tin khuyến mãi",
            "Thông tin vận chuyển",
            "Thông tin chính sách đổi trả, bảo hành, vận chuyển"
        ]
        
        # Dùng vòng lặp để gửi từng chức năng
        list_items = "Danh sách chức năng:\n"
        for function in bot_functions:
            list_items += f"- {function}\n"

        dispatcher.utter_message(text=list_items)
        
        return []

# response categories
class action_return_categories(Action):
    
    def name(self) -> Text:
        return "action_return_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        categories = CategoriesInfo().get_categories()
         
        list_items = "Danh sách danh mục sản phẩm cửa cửa hàng:\n"

        for category in  categories:
             list_items += f"- {str(category[0])} \n"

        dispatcher.utter_message(text=list_items)

        return []
    
# response recommend oil  
class action_return_recommend_oil(Action):
    
    def name(self) -> Text:
        return "action_return_recommend_oil"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        type = tracker.get_slot("vehicle_type")
        
        if (type == "xe tay ga"):
            product = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe tay ga")
        elif (type == "xe số" or type == "xe côn tay"):
            product = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe số")
            print(product)
        else:
            product = None
      
        if not product:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho loại xe anh/chị đã cung cấp !.")
            return []
        
        list_items = f"Danh sách sản phẩm phù hợp với xe {type}:\n"
        base_url = "http://127.0.0.1:8000/product-details/"
        for item in product:
            product_name = item[0]
            product_slug = item[1]
            product_url = f"{base_url}{product_slug}"
            list_items += f"- {product_name}: {product_url} \n"
            
        dispatcher.utter_message(text=list_items)
        
        return []

# response recommend air filter

class action_return_recommend_air_filter(Action):
    def name(self) -> Text:
        return "action_return_recommend_air_filter"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        model_type = tracker.get_slot("model_type")
        filter_type = tracker.get_slot("filter_type")
        
        
        products = ProductInfo().get_products_by_category_and_name(filter_type, model_type)
        
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho loại xe anh/chị đã cung cấp!")
            return []
        else:
            base_url = "http://127.0.0.1:8000/product-details/"
            list_items = f"Lọc gió phù hợp với xe {model_type} \n"  
            for item in products:
                product_name = item[0]
                product_slug = item[1]
                product_url = f"{base_url}{product_slug}"
                list_items += f"- {product_name}: {product_url} \n"
            dispatcher.utter_message(text=list_items)
            
            return []
        
# recommend bugi
class action_return_recommend_bugi(Action):
    def name(self) -> Text:
        return "action_return_recommend_bugi"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        model_type = tracker.get_slot("model_type")
        bugi_type = tracker.get_slot("bugi_type")
        
        print(f"bugi_type: {bugi_type}")
        print(f"model_type: {model_type}")
        
        products = ProductInfo().get_products_by_category_and_name(bugi_type, model_type)
        
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho loại xe anh/chị đã cung cấp!")
        else:
            base_url = "http://127.0.0.1:8000/product-details/"
            list_items = f"Bugi phù hợp với {model_type}: \n"
             
            for item in products:
                product_name = item[0] 
                product_slug = item[1]
                product_url = f"{base_url}{product_slug}" 
                list_items += f"- {product_name}: {product_url} \n"
            # Gửi tin nhắn danh sách sản phẩm đến người dùng
            dispatcher.utter_message(text=list_items)
            
        return []
        

# recommend protective clothing by gender

class action_return_recommend_protective_clothing(Action):
    def name(self) -> Text:
        return "action_return_recommend_protective_clothing"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        gender = tracker.get_slot("gender")
        
        products = ProductInfo().get_products_by_name(gender)
        
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho anh/chị !")
        else:
            base_url = "http://127.0.0.1:8000/product-details/"
            list_items = f"Áo giáp bảo hộ cho {gender}: \n"  
            
            for item in products:
                product_name = item[0]
                product_slug = item[1]
                product_url = f"{base_url}{product_slug}"
                list_items += f"- {product_name}: {product_url} \n"

            dispatcher.utter_message(text=list_items)
            
            return []
        
        return []
    
# recommend helmet
class action_return_recommend_helmet(Action):
    def name(self) -> Text:
        return "action_return_recommend_helmet"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        helmet_type = tracker.get_slot("helmet_type")
        
        products = ProductInfo().get_products_by_name(helmet_type)
        
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho anh/chị !")
        else:
            base_url = "http://127.0.0.1:8000/product-details/"
              
            list_items = f"Danh sách mũ bảo hiểm loại {helmet_type}: \n"
            
            for item in products:
                product_name = item[0]
                product_slug = item[1]
                product_url = f"{base_url}{product_slug}"
                list_items += f"- {product_name}: {product_url} \n"
                
            dispatcher.utter_message(text=list_items)
            
            return []
        
        return []
        
# ask product price
class action_return_product_price(Action):
    def name(self) -> Text:
        return "action_return_product_price"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product_name = tracker.get_slot("product_name")
        
        price = ProductInfo().get_product_price(product_name)
        
        if not price:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho anh/chị !")
        else:
            price = PriceFormatter.format_price(price)
            dispatcher.utter_message(text=f"Giá của sản phẩm {product_name} là: {price}")
        
        return []

# ask shipping fee
class action_return_shipping_cost(Action):
    def name(self) -> Text:
        return "action_return_shipping_cost"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        province = tracker.get_slot("province")
        
        shipping_fee = ShippingFee().get_shippingFee_info(province)
        
        if not shipping_fee:
            fee_not_exist = 60000
            fee_not_exist = PriceFormatter.format_price(fee_not_exist)
            dispatcher.utter_message(text=f"Phí vận chuyển về { province } là {fee_not_exist}.")

        else:
            shipping_fee = PriceFormatter.format_price(shipping_fee)
            dispatcher.utter_message(text=f"Phí vận chuyển về { province } là {shipping_fee}.")
        
        return []
# about promotions

class action_return_promotions(Action):
    def name(self) -> Text:
        return "action_return_promotions"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        promotions = PromotionsInfo().get_promotions()
        
        if not promotions:
            dispatcher.utter_message(text="Hiện tại cửa hàng không có chương trình khuyến mãi !")
        else:
            url_path = f"http://127.0.0.1:8000/promotions"
            dispatcher.utter_message(text=f"Chương trình khuyến mãi đang diễn ra anh/chị truy cập vào trang khuyến mãi để lấy những voucher khuyến mãi hấp dẫn !")
            dispatcher.utter_message(text=f"Truy cập vào đường link sau để xem chi tiết: {url_path}")
        
        return []
        
# show table chose size
class action_show_size_table_image(Action):
    def name(self):
        return "action_show_size_table_image"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product_type = tracker.get_slot("product_type")
        # Gửi hình ảnh
        if product_type == "áo":
            dispatcher.utter_message(text="Bảng size:", image="https://bigbike.vn/wp-content/uploads/2020/06/Alpinestars-Mens-Size-Chart.jpg")
            dispatcher.utter_message(text="Anh/chị có thể chọn lớn hơn 1 size để mặc thoải mái hơn ạ")
        else:
            dispatcher.utter_message(text= "Bảng size:", image="https://shop2banh.vn/images/2020/05/20200527_d048f4b83908d99ebb740ab0b8355f05_1590565151.jpeg")
        return []

            
        
        
        
    
        
    




