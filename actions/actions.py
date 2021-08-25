# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import feedparser
import requests
import random

class action_get_lottery(Action):
   def name(self):
        return 'action_get_lottery'
   def run(self, dispatcher, tracker, domain):
        url = 'https://xskt.com.vn/rss-feed/mien-bac-xsmb.rss'
        feed_cnt = feedparser.parse(url)
        first_node = feed_cnt['entries']
        return_msg = first_node[0]['title'] + "\n" + first_node[0]['description']
        dispatcher.utter_message(return_msg)
        return []


class ActionCoronaTracker(Action):
    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("https://corona.lmao.ninja/v2/countries").json()

        entities = tracker.latest_message['entities']
        country = None

        for e in entities:
            if e['entity'] == 'country':
                country = e['value']
        # dispatcher.utter_message(text=f"Here is the information in {country}")
        for data in response:
            if data['country'] == country:
                print(country)
                statistics = f"Quốc gia: {data['country']}\nTổng số ca: {data['cases']}\nSố ca ngày hôm nay: {data['todayCases']}\nTổng số ca tử vong: {data['deaths']}\nTổng số ca tử vong ngày hôm nay: {data['todayDeaths']}"
                print(statistics)
                dispatcher.utter_message(text=statistics)
        return []




DATABASE = ["cơm gà",
            "cơm hải sản",
            "mì spaghetti",
            "cơm sườn",
            "bún bò",
            "mì tôm hải sản",
            "bánh mì trứng",
            "bánh mì xúc xích",
            "bánh mì pate",
            "trà tắc anh ManBurn"
            ]
class ActionRecommend(Action):
    def name(self) -> Text:
        return "action_recommend"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = []
        for i in range(2):
            food_number = random.randrange(len(DATABASE))
            food.append(DATABASE[food_number])

        dispatcher.utter_message(
            text="Bot nghĩ hôm nay anh có thể thử món '{}' hoặc bên cạnh đó cũng có thể là món '{}' ạ".format(food[0], food[1]))

        return []
