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
from actions.functions.check_qty import CheckQty
import re

base_url_img = "http://127.0.0.1:8000/uploads/product/"
base_url = "http://127.0.0.1:8000/product-details/"

# custom fallback
class action_custom_fallback(Action):
    def name(self) -> Text:
        return "action_custom_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cust_sex = tracker.get_slot("cust_sex").capitalize()
        
        dispatcher.utter_message(text=f"Xin {cust_sex} vui lòng diễn đạt lại yêu cầu để em có thể hỗ trợ tốt hơn ạ.")
        
        return []
# response bot functions
class action_return_bot_functions(Action):

    def name(self) -> Text:
        return "action_return_bot_functions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Danh sách chức năng của bot
        bot_functions = [
            "Tư vấn thời điểm cần thay nhớt và gợi ý nhớt",
            "Tư vấn thời điểm cần thay lọc gió và gợi ý lọc gió",
            "Tư vấn thời điểm cần thay bugi và gợi ý bugi",
            "Tư vấn chọn size áo bảo hộ theo chiều cao và cân nặng",
            "Tư vấn cách chọn size nón bảo hiểm",
            "Cung cấp thông tin liên hệ cửa hàng",
            "Cung cấp thông tin tồn kho của sản phẩm",
            "Cung cấp thông tin khuyến mãi",
            "Cung cấp thông tin phí vận chuyển theo khu vực",
            "Cung cấp thông tin các chính sách đổi trả, bảo hành, và vận chuyển",
        ]
        
        # Dùng vòng lặp để gửi từng chức năng
        list_items = "Em có thể thực hiện được các chức năng sau:\n"
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
         
        list_items = "Danh mục sản phẩm của cửa hàng:\n"

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
        
        cust_sex = tracker.get_slot("cust_sex")
        type = tracker.get_slot("vehicle_type")
        type = type.lower()
        if (type == "xe tay ga"):
            products = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe tay ga")
        elif (type == "xe số" or type == "xe côn tay"):
            products = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe số")
            print(products)
        else:
            products = None
      
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho loại xe anh/chị đã cung cấp !.")
            return []
        
        dispatcher.utter_message(text=f"Em gửi danh sách nhớt phù hợp với {type}: \n")
        elements = []
        
        for item in products:
            
            if(item[4] == None):
                     check_qty = f"Sản phẩm đã hết hàng"
            else:
                check_qty = f"SL tồn kho {item[4]}"
            
            element = {
                "title": item[0],
                "image_url": f"{base_url_img}{item[3]}",
                "subtitle": f"Giá: {PriceFormatter.format_price(item[2])}",
                "subtitle": f"SL tồn kho: {check_qty}",
                "default_action": {
                    "type": "web_url",
                    "url": f"{base_url}{item[1]}",
                    "webview_height_ratio": "square"
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "url": f"{base_url}{item[1]}",
                        "title": "Xem chi tiết"
                    },
                ]
            }
            elements.append(element)
            
            # Nếu có ít nhất một sản phẩm, gửi carousel
        if elements:
            new_carousel = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements  # Thêm danh sách các mục vào đây
                }
            }
            dispatcher.utter_message(attachment=new_carousel)
            dispatcher.utter_message(text=f"{cust_sex} có thể xem chi tiết sản phẩm bằng cách click vào nút Xem chi tiết.")
            return []
        
        return []

# response recommend air filter
class action_return_recommend_air_filter(Action):
    def name(self) -> Text:
        return "action_return_recommend_air_filter"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        model_type = tracker.get_slot("model_type")
        sub_category_1 = tracker.get_slot("sub_category_1")
        
        
        products = ProductInfo().get_products_by_category_and_name(sub_category_1, model_type)
        
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho loại xe anh/chị đã cung cấp!")
            return []
        else:
            # base_url = "http://127.0.0.1:8000/product-details/"
            dispatcher.utter_message(text=f"Em gửi danh sách lọc gió phù hợp với xe {model_type}: \n")
            # list_items = f"Lọc gió phù hợp với xe {model_type}: \n"  
            elements = []
            
            for item in products:
                
                if(item[6] == None):
                     check_qty = f"Sản phẩm đã hết hàng"
                else:
                    check_qty = f"SL tồn kho {item[6]}"
                
                element = {
                    "title": item[0],
                    "image_url": f"{base_url_img}{item[5]}",
                    "subtitle": f"Giá: {PriceFormatter.format_price(item[2])}",
                    "subtitle": f"{check_qty}",
                    "default_action": {
                        "type": "web_url",
                        "url": f"{base_url}{item[1]}",
                        "webview_height_ratio": "square"
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": f"{base_url}{item[1]}",
                            "title": "Xem chi tiết"
                        },
                    ]
                }
                
                elements.append(element)
                
                # Nếu có ít nhất một sản phẩm, gửi carousel
            if elements:
                new_carousel = {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements  # Thêm danh sách các mục vào đây
                    }
                }
                dispatcher.utter_message(attachment=new_carousel)
                return []
            
        return []
        
# recommend bugi
class action_return_recommend_bugi(Action):
    def name(self) -> Text:
        return "action_return_recommend_bugi"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        model_type = tracker.get_slot("model_type")
        sub_category_3 = tracker.get_slot("sub_category_3")
        
        print(f"sub_category_3: {sub_category_3}")
        print(f"model_type: {model_type}")
        
        products = ProductInfo().get_products_by_category_and_name(sub_category_3, model_type)
        
        if not products:
            dispatcher.utter_message(text=f"Hiện tại không có sản phẩm phù hợp cho xe {model_type} anh/chị đã cung cấp!")
        else:
            dispatcher.utter_message(text=f"Em gửi danh sách bugi phù hợp với xe {model_type}: \n")
            # base_url = "http://127.0.0.1:8000/product-details/"
            
            elements = []
            
            for item in products:
                
                if(item[6] == None):
                     check_qty = f"Sản phẩm đã hết hàng"
                else:
                    check_qty = f"SL tồn kho {item[6]}"
                    
                element = {
                    "title": item[0],
                    "image_url": f"{base_url_img}{item[5]}",
                    "subtitle": f"Giá: {PriceFormatter.format_price(item[2])}",
                    "subtitle": f"{check_qty}",
                    "default_action": {
                        "type": "web_url",
                        "url": f"{base_url}{item[1]}",
                        "webview_height_ratio": "square"
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": f"{base_url}{item[1]}",
                            "title": "Xem chi tiết"
                        },
                    ]
                }
                elements.append(element)
                
                 # Nếu có ít nhất một sản phẩm, gửi carousel
            if elements:
                new_carousel = {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements  # Thêm danh sách các mục vào đây
                    }
                }
                dispatcher.utter_message(attachment=new_carousel)
                return []
            
        return []
        
# recommend protective clothing by gender
class action_return_recommend_protective_clothing(Action):
    def name(self) -> Text:
        return "action_return_recommend_protective_clothing"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        gender = tracker.get_slot("gender")
        print(gender)
        
        # Lấy sản phẩm theo giới tính
        if gender.lower() in ["anh", "chú"]:
            products = ProductInfo().get_products_by_name("nam")
        else:
            products = ProductInfo().get_products_by_name("nữ")
        
        # Kiểm tra nếu không có sản phẩm phù hợp
        if not products:
            dispatcher.utter_message(text=f"Hiện tại không có sản phẩm phù hợp cho {gender}!")
        else:
            dispatcher.utter_message(text=f"Em gửi {gender} danh sách áo bảo hộ: \n")
            base_url = "http://127.0.0.1:8000/product-details/"
            base_img_url = "http://127.0.0.1:8000/uploads/product/"

            # Tạo danh sách các phần tử (elements) cho carousel
            elements = []
            
            for item in products:
                # Tạo từng mục trong carousel
                element = {
                    "title": item[0],
                    "image_url": f"{base_img_url}{item[3]}",
                    "subtitle": f"Giá: {PriceFormatter.format_price(item[2])}",
                    "default_action": {
                        "type": "web_url",
                        "url": f"{base_url}{item[1]}",
                        "webview_height_ratio": "square"
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": f"{base_url}{item[1]}",
                            "title": "Xem chi tiết"
                        },
                    ]
                }
                # Thêm mục vào danh sách elements
                elements.append(element)
            
            # Nếu có ít nhất một sản phẩm, gửi carousel
            if elements:
                new_carousel = {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements  # Thêm danh sách các mục vào đây
                    }
                }
                dispatcher.utter_message(attachment=new_carousel)
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
        print(helmet_type)
        
        products = ProductInfo().get_products_by_name(helmet_type)
        
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho anh/chị !")
        else:
            dispatcher.utter_message(text=f"Em gửi danh sách nón bảo hộ loại {helmet_type} : \n")

            elements = []
            for item in products:
                if(item[4] == None):
                     check_qty = f"Sản phẩm đã hết hàng"
                else:
                    check_qty = f"SL tồn kho {item[4]}"
                    
                element = {
                    "title": item[0],
                    "image_url": f"{base_url_img}{item[3]}",
                    "subtitle": f"Giá: {PriceFormatter.format_price(item[2])}",
                    "subtitle": f"{check_qty}",
                    "default_action": {
                        "type": "web_url",
                        "url": f"{base_url}{item[1]}",
                        "webview_height_ratio": "square"
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": f"{base_url}{item[1]}",
                            "title": "Xem chi tiết"
                        },
                    ]
                }
                 
                elements.append(element)
                
                # Nếu có ít nhất một sản phẩm, gửi carousel
            if elements:
                new_carousel = {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements  # Thêm danh sách các mục vào đây
                    }
                }
                dispatcher.utter_message(attachment=new_carousel)
                return []
        
        return []
        
# ask shipping fee
class action_return_shipping_cost(Action):
    def name(self) -> Text:
        return "action_return_shipping_cost"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        province = tracker.get_slot("province").capitalize()
        
        if province == "TP HCM" or province == "TP Hồ Chí Minh":
            province = "TP HCM"
        
        
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
    
# check qty
class action_check_qty(Action):
    def name(self) -> Text:
        return "action_check_qty"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product_name = tracker.get_slot("product_name")
        
        check_qty = CheckQty().check_qty(product_name)
        
        if check_qty and len(check_qty) > 0:
            dispatcher.utter_message(text=f"Sản phẩm {product_name} còn hàng! Số lượng còn lại: {check_qty[0][1]}")
        else:
            dispatcher.utter_message(text=f"Hiện tại sản phẩm {product_name} đã hết hàng!")
        
# show table chose size
class action_ask_product_size(Action):
    def name(self):
        return "action_ask_product_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cust_sex = tracker.get_slot("cust_sex")
        cust_sex = cust_sex.capitalize()
        
        product_type = tracker.get_slot("product_type")
        # Gửi hình ảnh
        if product_type == "áo":
            dispatcher.utter_message(text= f"{cust_sex} cung cấp thông tin chiều cao và cân nặng để em tư vấn size áo phù hợp ạ !")
        elif (product_type == "nón" or product_type == "mũ"):
            dispatcher.utter_message(text= f"Em gửi {cust_sex} bảng size {product_type}:", image="https://shop2banh.vn/images/2020/05/20200527_d048f4b83908d99ebb740ab0b8355f05_1590565151.jpeg")
        else:
            dispatcher.utter_message(text="Hiện tại em không có bảng size cho sản phẩm này ạ !")
        return []

class action_recommend_shirt_size(Action):     
    def name(self) -> Text:
        return "action_recommend_shirt_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cust_sex = tracker.get_slot("cust_sex")
        height = tracker.get_slot("height")
        weight = tracker.get_slot("weight")

        # Cập nhật các mẫu regex cho chiều cao và cân nặng
        height_patterns = [
            r'1m([5-9][0-9])',    # Match 1m50-1m99
            r'1m([5-9])',         # Match 1m5-1m9
        ]

        weight_patterns = [
            r'100kg',            # Match 100kg
            r'([5-9][0-9]?)kg',  # Match 50kg-99kg
        ]

        # Process height
        height_in_cm = None
        for pattern in height_patterns:
            match = re.search(pattern, height)
            if match:
                matched_value = match.group(1)
                if len(matched_value) == 1:  # trường hợp 1m6, 1m7, ..
                    height_in_cm = int(matched_value) * 10  # lấy số sau m và nhân với 10
                else:  # trường hợp 1m50, 1m51, ..
                    height_in_cm = int(matched_value)
                break

        # nếu không tìm thấy chiều cao
        if height_in_cm is None:
            dispatcher.utter_message(text="Xin lỗi, tôi không hiểu định dạng chiều cao. Vui lòng nhập theo định dạng 1m80 hoặc 1.80")
            return []

        # Tính chiều cao thực tế
        actual_height = height_in_cm + 100

        # xử lý cân nặng
        weight_value = None
        for pattern in weight_patterns:
            match = re.search(pattern, weight)
            if match:
                if pattern == r'100kg':
                    weight_value = 100
                else:
                    weight_value = int(match.group(1)) # lấy số trước kg
                break

        if weight_value is None:
            dispatcher.utter_message(text="Xin lỗi, tôi không hiểu định dạng cân nặng. Vui lòng nhập theo định dạng 70kg")
            return []

        # Tính size áo
        if ((actual_height <= 165) and (45 <= weight_value <= 60)):
            size = "S"
        elif ((165 < actual_height <= 170) and (60 < weight_value <= 65)):
            size = "M"
        elif ((170 < actual_height <= 180) and (65 < weight_value <= 80)):
            size = "L"
        else:
            size = "XL"
        # Send response
        dispatcher.utter_message(
            text=f"Với chiều cao {actual_height}cm và cân nặng {weight_value}kg, "
                 f"Em khuyên {cust_sex} nên chọn size {size}."
        )

        return []

        
    
        
    




