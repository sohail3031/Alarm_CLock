import threading
import time

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from pygame import mixer

mixer.init()


class Timer(Screen):
    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)
        self.start = False
        self.hour, self.minute, self.second = 0, 0, 59
        daemon_thread = threading.Thread(target=self.start_timer)
        daemon_thread.daemon = True
        daemon_thread.start()
        self.dialog = None

    def show_dialog(self, text):
        layout = MDGridLayout(cols=1, padding=10, spacing=10)
        popup_label = MDLabel(text=text, font_size=20, bold=True, pos_hint={"center_x": .5, "center_y": .5},
                              theme_text_color="Custom", text_color=[1, 1, 1, 1], halign="center")
        popup_button = MDRaisedButton(text="OK", size_hint=(1, None), height=50, bold=True, font_size=20,
                                      pos_hint={"center_x": .5, "center_y": .5})
        layout.add_widget(popup_label)
        layout.add_widget(popup_button)
        popup = Popup(title="Alert!", content=layout, size_hint=(None, None), size=(300, 300), auto_dismiss=False)
        popup.open()
        popup_button.bind(on_press=popup.dismiss)
        popup_button.bind(on_press=self.stop_alarm)

    def stop_alarm(self, *args):
        mixer.music.stop()

    def set_timer(self):
        self.hour, self.minute = self.ids.hours_timer.text, self.ids.minutes_timer.text
        if len(self.hour) < 2:
            self.show_dialog(text="Hours should in (00-23) format")
        elif len(self.minute) < 2:
            self.show_dialog(text="Minutes should in (00-23) format")
        else:
            if self.ids.start_timer.text == "Start":
                try:
                    self.hour = int(self.hour)
                    if self.hour < 0 or self.hour > 23:
                        self.show_dialog(text=f"Hours should in (00-23) format. Not {self.hour}")
                except ValueError:
                    self.show_dialog(text="Hours should in (00-23) format. It should not be empty")
                try:
                    self.minute = int(self.minute)
                    if self.minute < 0 or self.minute > 59:
                        self.show_dialog(text=f"Minutes should in (00-59) format. Not {self.minute}")
                    self.minute -= 1
                    if self.minute == -1 and self.hour >= 1:
                        self.minute = 59
                        self.hour -= 1
                except ValueError:
                    self.show_dialog(text="Minutes should in (00-59) format. It should not be empty")
                if self.hour >= 0 and self.hour < 24 and self.minute >= 0 and self.minute < 60:
                    self.ids.pause_timer.disabled = False
                    self.ids.start_timer.text = "Cancel"
                    self.ids.start_timer.md_bg_color = [1, 0, 0, 1]
                    self.start = True
                else:
                    self.ids.hours_timer.text, self.ids.minutes_timer.text = "", ""
            elif self.ids.start_timer.text == "Cancel":
                self.reset_timer()

    def reset_timer(self):
        self.ids.show_timer.text = "00:00:00"
        self.ids.start_timer.text = "Start"
        self.ids.start_timer.md_bg_color = [0, 0, 1, 1]
        self.ids.pause_timer.text = "Pause"
        self.ids.pause_timer.disabled = True
        self.start = False
        self.ids.hours_timer.text, self.ids.minutes_timer.text = "", ""
        self.hour, self.minute, self.second = 0, 0, 59

    def pause_timer_function(self):
        if self.ids.pause_timer.text == "Pause":
            self.start = False
            self.ids.pause_timer.text = "Resume"
        else:
            self.ids.pause_timer.text = "Pause"
            self.start = True

    def check_time_format(self):
        if len(str(self.hour)) == 1 and len(str(self.minute)) == 1 and len(str(self.second)) == 1:
            return f"0{self.hour}:0{self.minute}:0{self.second}"
        elif len(str(self.minute)) == 1 and len(str(self.second)) == 1:
            return f"{self.hour}:0{self.minute}:0{self.second}"
        elif len(str(self.hour)) == 1 and len(str(self.second)) == 1:
            return f"0{self.hour}:{self.minute}:0{self.second}"
        elif len(str(self.hour)) == 1 and len(str(self.minute)) == 1:
            return f"0{self.hour}:0{self.minute}:{self.second}"
        elif len(str(self.hour)) == 1:
            return f"0{self.hour}:{self.minute}:{self.second}"
        elif len(str(self.minute)) == 1:
            return f"{self.hour}:0{self.minute}:{self.second}"
        elif len(str(self.second)) == 1:
            return f"{self.hour}:{self.minute}:0{self.second}"

    def start_timer(self):
        while True:
            if self.start:
                if self.minute != -1:
                    if self.second != 0:
                        self.ids.show_timer.text = self.check_time_format()
                        self.second -= 1
                        time.sleep(1)
                    else:
                        self.ids.show_timer.text = self.check_time_format()
                        self.minute -= 1
                        self.second = 59
                else:
                    if self.hour == 0 and self.minute == -1:
                        self.reset_timer()
                        self.show_dialog(text="Time's Up")
                        with open("selected_alarm_ringtone.txt", "r") as file:
                            data = file.readlines()
                        mixer.music.load(f"ringtones/{data[0]}.mp3")
                        mixer.music.play()
                    else:
                        self.minute = 59
                        self.hour -= 1
