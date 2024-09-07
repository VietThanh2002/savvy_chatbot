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
from actions.functions.get_categories import CategoriesInfo
from actions.functions.get_products import ProductInfo

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

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

        # Gửi tin nhắn chứa thông danh mục sản phẩm cho người dùng
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
        
        if type == "xe tay ga":
            product = ProductInfo().get_products_by_category_and_subcategory("Phụ gia xe tay ga")
        elif type == "xe số phổ thông":
            product = ProductInfo().get_products_by_category_and_subcategory("Phụ gia xe số")
        else:
            product = ProductInfo().get_products_by_category_and_subcategory("Nhớt xe máy")
            
        list_items = "Danh sách sản phẩm phù hợp với loại xe của bạn:\n"
        
        for item in product:
            list_items += f"- {str(item[0])} \n"
            
        dispatcher.utter_message(text=list_items)
        
        return []
            
        
        
        
    
        
    




