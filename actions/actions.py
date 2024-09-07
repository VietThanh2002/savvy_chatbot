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

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


# response categories
class response_list_categories(Action):
    
    def name(self) -> Text:
        return "response_list_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        categories = CategoriesInfo().get_categories()
         
        list_items = "Danh sách danh mục:\n"
        
        for category in  categories:
             list_items += f"- Tên: {str(category[0])} \n"

        # Gửi tin nhắn chứa thông danh mục sản phẩm cho người dùng
        dispatcher.utter_message(text=list_items)

        return []




