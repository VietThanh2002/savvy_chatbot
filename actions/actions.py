
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.functions.db_connect import dbConnect
from actions.functions.format_price import PriceFormatter
from actions.functions.get_categories import CategoriesInfo
from actions.functions.get_products import ProductInfo
from actions.functions.get_shipping_fee import ShippingFee
from actions.functions.get_promotions import PromotionsInfo
from actions.functions.check_qty import CheckQty
import re
import random

base_url_img = "http://127.0.0.1:8000/uploads/product/"
base_url = "http://127.0.0.1:8000/product-details/"
    
class action_greet_with_name(Action):
    def name(self) -> Text:
        return "action_greet_with_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cust_sex = tracker.get_slot("cust_sex")
        cust_name = tracker.get_slot("cust_name")
        
        # Capitalize if values exist
        if cust_sex:
            cust_sex = cust_sex.capitalize()
        if cust_name:
            cust_name = cust_name.capitalize()

        formal_templates = [
            "Xin chào quý khách! Em có thể hỗ trợ tư vấn thông tin gì ạ?",
            "Chào quý khách! Em có thể giúp gì cho quý khách ạ?",
            "Kính chào quý khách! Quý khách cần em hỗ trợ thông tin gì ạ?"
        ]

        name_only_templates = [
            f"Xin chào {cust_name}! Em có thể hỗ trợ tư vấn thông tin gì ạ?",
            f"Chào {cust_name}! Em có thể giúp gì cho quý khách ạ?",
            f"Rất vui được gặp {cust_name}! Quý khách cần em hỗ trợ thông tin gì ạ?"
        ]

        full_info_templates = [
            f"Xin chào {cust_sex} {cust_name}! Em có thể hỗ trợ tư vấn thông tin gì cho {cust_sex} ạ?",
            f"Chào {cust_sex} {cust_name}! Em có thể giúp gì cho {cust_sex} ạ?",
            f"Rất vui được gặp {cust_sex} {cust_name}! {cust_sex} cần em hỗ trợ thông tin gì ạ?"
        ]

        # Choose appropriate template based on available information
        if cust_sex is None and cust_name is None:
            dispatcher.utter_message(text=random.choice(formal_templates))
            return [
                SlotSet("cust_sex", "Quý khách"),
                SlotSet("cust_name", "Quý khách")
            ]
        elif cust_sex is None and cust_name:
            dispatcher.utter_message(text=random.choice(name_only_templates))
            return [
                SlotSet("cust_sex", "Quý khách"),
                SlotSet("cust_name", cust_name)
            ]
        else:
            dispatcher.utter_message(text=random.choice(full_info_templates))
            return [
                SlotSet("cust_sex", cust_sex if cust_sex else "Quý khách"),
                SlotSet("cust_name", cust_name if cust_name else "Quý khách")
            ]
        
        
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
class action_return_recommend_oil_by_vehicle_type(Action):
    
    def name(self) -> Text:
        return "action_return_recommend_oil_by_vehicle_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cust_sex = tracker.get_slot("cust_sex")
        vehicle_type = tracker.get_slot("vehicle_type")
      
        # Kiểm tra loại xe để tìm sản phẩm phù hợp
        if vehicle_type == "xe tay ga":
            products = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe tay ga")
        elif vehicle_type in ["xe số", "xe côn tay"]:
            products = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe số")     
        else:
            dispatcher.utter_message(text="Không xác định được loại xe. Vui lòng cung cấp loại xe hợp lệ.")
            return []
      
        # Kiểm tra nếu không có sản phẩm nào
        if not products:
            dispatcher.utter_message(text="Hiện tại không có sản phẩm phù hợp cho loại xe anh/chị đã cung cấp!")
            return []
        
        # Thông báo danh sách sản phẩm nếu có
        dispatcher.utter_message(text=f"Em gửi danh sách nhớt phù hợp với {vehicle_type}: \n")
        
        elements = []
        
        for item in products:
            # Kiểm tra giá sản phẩm
            price = "Liên hệ" if item[2] == 0 else PriceFormatter.format_price(item[2])
            
            # Kiểm tra số lượng tồn kho
            check_qty = "Sản phẩm đã hết hàng" if item[4] is None or item[4] <= 0 else f"SL tồn kho {item[4]}"
            
            # Tạo phần tử cho carousel
            element = {
                "title": item[0] or "Sản phẩm",
                "image_url": f"{base_url_img}{item[3]}" if item[3] else "",
                "subtitle": f"Giá: {price} - {check_qty}", 
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
        
        # Gửi carousel nếu có phần tử
        if elements:
            new_carousel = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
            dispatcher.utter_message(attachment=new_carousel)
            dispatcher.utter_message(text=f"{cust_sex} có thể xem chi tiết sản phẩm bằng cách click vào nút Xem chi tiết.")
        
        return []


# recommend oil buy motobike name
class action_return_recommend_oil_by_motorbike_name(Action):
    def name(self) -> Text:
        return "action_return_recommend_oil_by_motorbike_name"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cust_sex = tracker.get_slot("cust_sex")
        cust_sex = cust_sex.capitalize()
        motorbike_name = tracker.get_slot("motorbike_name")
        motorbike_name = motorbike_name.lower()
        category_1 = tracker.get_slot("category_1")
        category_1 = category_1.lower()
        
        scooter_bikes = set(["grande", "ab", "air blade", "lead", "vision", "click", "sh"])
        manual_bikes = set(["wave", "dream", "sirius", "future", "winner", "exciter", "sonic", "ware alpha"])

        if motorbike_name in scooter_bikes:
            products = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe tay ga")
        elif motorbike_name in manual_bikes:
            products = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe số")

        if not products:
            dispatcher.utter_message(text=f"Hiện tại không có sản phẩm phù hợp cho xe {motorbike_name} của {cust_sex}!")
    
        else:
            dispatcher.utter_message(text=f"Em gửi danh sách nhớt phù hợp với xe {motorbike_name}: \n")
            elements = []
        
            for item in products:
                if item[2] == 0:
                    price = "Liên hệ"
                else:
                    price = PriceFormatter.format_price(item[2])
                
                if item[4] == None:
                    check_qty = f"Sản phẩm đã hết hàng"
                else:
                    check_qty = f"SL tồn kho {item[4]}"
                
                elements = []
        
                for item in products:
                    
                    if(item[2] == 0):
                        price = "Liên hệ"
                    else:
                        price = PriceFormatter.format_price(item[2])
                    
                    if(item[4] == None):
                            check_qty = f"Sản phẩm đã hết hàng"
                    else:
                        check_qty = f"SL tồn kho {item[4]}"
                    
                    element = {
                        "title": item[0],
                        "image_url": f"{base_url_img}{item[3]}",
                        "subtitle": f"Giá: {price} - {check_qty}", 
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
        cust_sex = tracker.get_slot("cust_sex")
        cust_sex = cust_sex.capitalize()
        
        products = ProductInfo().get_products_by_category_and_name(sub_category_1, model_type)
        
        if not products:
            dispatcher.utter_message(text=f"Hiện tại cửa hàng không có {sub_category_1} phù hợp cho xe của {cust_sex}")
            return []
        else:
            # base_url = "http://127.0.0.1:8000/product-details/"
            dispatcher.utter_message(text=f"Em gửi danh sách lọc gió phù hợp với xe {model_type}: \n")
            # list_items = f"Lọc gió phù hợp với xe {model_type}: \n"  
            elements = []
            
            for item in products:
                
                if(item[2] == 0):
                    price = "Liên hệ"
                else:
                    price = PriceFormatter.format_price(item[2])
            
                if(item[6] == None):
                     check_qty = f"Sản phẩm đã hết hàng"
                else:
                    check_qty = f"SL tồn kho {item[6]}"
                
                element = {
                    "title": item[0],
                    "image_url": f"{base_url_img}{item[5]}",
                    "subtitle": f"Giá: {price} - {check_qty}", 
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
                if(item[2] == 0):
                    price = "Liên hệ"
                else:
                    price = PriceFormatter.format_price(item[2])
                    
                if(item[6] == None):
                     check_qty = f"Sản phẩm đã hết hàng"
                else:
                    check_qty = f"SL tồn kho {item[6]}"
                    
                element = {
                    "title": item[0],
                    "image_url": f"{base_url_img}{item[5]}",
                    "subtitle": f"Giá: {price} - {check_qty}", 
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
                if(item[2] == 0):
                    price = "Liên hệ"
                else:
                    price = PriceFormatter.format_price(item[2])
                    
                if(item[4] == None):
                    check_qty = f"Sản phẩm đã hết hàng"
                else:
                    check_qty = f"SL tồn kho {item[4]}"    
                # Tạo từng mục trong carousel
                element = {
                    "title": item[0],
                    "image_url": f"{base_img_url}{item[3]}",
                    "subtitle": f"Giá: {price} - {check_qty}", 
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
            dispatcher.utter_message(text= f"Em gửi {cust_sex} bảng size {product_type}:", image="https://bigbike.vn/wp-content/uploads/2024/09/z5815672163854_fdc64e15333852403f43e7507805d32a.jpg")
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
    
# response membership benefits
class action_return_membership_benefits(Action):
    def name(self) -> Text:
        return "action_return_membership_benefits"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Chương trình thành viên của cửa hàng áp dụng ưu đãi xếp hạng mua sắm trong tháng như sau: \n"
                                    "- Tặng voucher giảm giá 20.000đ cho khách hàng bậc Bạc\n"
                                    "- Tặng voucher giảm giá 50.000đ cho khách hàng bậc Vàng\n"
                                    "- Tặng voucher giảm giá 100.000đ cho khách hàng bậc Kim Cương\n")
                                   
        
        return []

        
    
        
    




