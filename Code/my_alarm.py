from kivy import Config
from kivymd.app import MDApp
from kivymd.uix.behaviors import RectangularElevationBehavior, BackgroundColorBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from timer_alarm import Timer
from kivy.lang import Builder
from stop_watch_alarm import StopWatch
from world_clock_alarm import WorldClock
from alarm_clock import AlarmClock
from change_ringtone import ShowAllRingtones

Builder.load_file("timer_alarm_kv.kv")
Builder.load_file("stop_watch_alarm_kv.kv")
Builder.load_file("world_clock_alarm_kv.kv")


class AlarmApp(MDApp):
    def build(self):
        with open("check_theme.txt", "r") as file:
            self.theme_cls.theme_style = "Light" if "Light" in file.readlines() else "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "A700"
        self.icon = "images/alarm_clock.jpg"
        Config.set('kivy', 'window_ico', 'images/alarm_clock.jpg')
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.screen_manager.add_widget(AlarmClock(name="Alarm Clock"))
        self.screen_manager.add_widget(WorldClock(name="World Clock"))
        self.screen_manager.add_widget(StopWatch(name="Stop Watch"))
        self.screen_manager.add_widget(Timer(name="Timer"))
        return self.screen_manager

    def change_ringtone(self):
        ShowAllRingtones().show_confirmation_dialog()

    def change_screen(self, change_screen):
        self.screen_manager = change_screen

    def change_theme(self, flag):
        self.theme_cls.theme_style = "Dark" if flag else "Light"
        with open("check_theme.txt", "w") as file:
            file.write("Dark" if flag else "Light")


class RectangularElevationButton(RectangularElevationBehavior, MDBoxLayout, BackgroundColorBehavior):
    md_bg_color = [.60, .60, .60, 1]


if __name__ == '__main__':
    AlarmApp().run()
