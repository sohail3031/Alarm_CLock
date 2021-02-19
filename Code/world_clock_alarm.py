import threading
import pytz
import time

from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem
from datetime import datetime
from kivymd.toast import toast

time_zones = list(pytz.all_timezones)
name = ""


class CustomOneLineListItemAddCities(OneLineListItem):
    pass


class CustomOneLineListItem(OneLineListItem):
    @staticmethod
    def add_new_clock(city_name):
        global name
        name = city_name


class WorldClock(Screen):
    def __init__(self, **kwargs):
        super(WorldClock, self).__init__(**kwargs)
        self.search_time_zones()
        self.cities = []
        daemon_thread = threading.Thread(target=self.continuous)
        daemon_thread.daemon = True
        daemon_thread.start()
        self.label_text = ""
        self.dialog = None
        self.start = False

    def continuous(self):
        while True:
            if name and name not in self.cities:
                self.cities.append(name)
            text = ""
            for i in self.cities:
                text += f"{i}    {datetime.now(pytz.timezone(i)).strftime('%H:%M:%S')}\n\n"
            self.ids.display_added_world_clock.text = text
            time.sleep(1)

    def search_time_zones(self, text="", search=False):
        def add_items(city_name):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineListItem",
                    "text": city_name,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        for i in time_zones:
            if search:
                if text.title() in i:
                    add_items(i)
            else:
                add_items(i)

    def add_clock(self):
        global name
        text = self.ids.select_world_clock.text

        if name != "" or text != "":
            for i in set(time_zones):
                if (i.lower() == text.lower()) or (text.lower() in i.lower()):
                    name = i
                    toast(f"Added {name}")
                    break
        else:
            toast(f"{text} is not present!")
        self.ids.select_world_clock.text = ""

    def remove_clock(self):
        global name
        text = self.ids.remove_world_clock.text

        if self.cities and text == "":
            toast(f"Removed {self.cities[0]}")
            self.cities.pop(0)
        elif not self.cities:
            toast(f"Not Present")
        elif text.lower() == "all":
            self.cities.clear()
            name = ""
            self.ids.remove_world_clock.text = ""
            self.ids.select_world_clock.text = ""
            toast("Removed All Timezones")
        elif text in self.cities:
            toast(f"Removed {text}")
            self.cities.remove(text)
        else:
            length = len(self.cities)
            print(self.cities)
            self.cities = [i for i in self.cities if text.lower() not in i.lower()]
            print(self.cities)
            if length <= len(self.cities):
                toast(f"{text} is not present!")

        self.ids.remove_world_clock.text = ""
        name = ""
