import threading
import time

from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem


class StopWatch(Screen):
    def __init__(self, **kwargs):
        super(StopWatch, self).__init__(**kwargs)
        self.start = False
        self.minutes, self.seconds, self.milli_seconds, self.count = 0, 0, 0, 1
        self.lap_list = []
        self.lap_time = ""
        daemon_thread = threading.Thread(target=self.stop_watch)
        daemon_thread.daemon = True
        daemon_thread.start()

    def start_stop_watch(self):
        if self.ids.stop_watch_start.text == "Start":
            self.ids.stop_watch_start.md_bg_color = [1, 0, 0, 1]
            self.ids.stop_watch_start.text = "Stop"
            self.start = True
            self.ids.stop_watch_lap.disabled = False
            self.ids.stop_watch_lap.text = "Lap"
            self.ids.stop_watch_lap.disabled = False
            self.lap_time = "00:00.00"
        else:
            self.ids.stop_watch_start.text = "Start"
            self.ids.stop_watch_start.md_bg_color = [0, 0, 1, 1]
            self.start = False
            self.ids.stop_watch_lap.text = "Reset"

    def lap_stop_watch(self):
        if self.ids.stop_watch_lap.text == "Reset":
            self.ids.stop_watch_time.text = "00:00.00"
            self.minutes, self.seconds, self.milli_seconds = 0, 0, 0
            self.ids.stop_watch_lap.text = "Lap"
            self.ids.stop_watch_lap.disabled = True
            self.start = False
            self.ids.stop_watch_container.clear_widgets()
        else:
            lap = self.check_correct_format(minutes=self.minutes, seconds=self.seconds,
                                            milli_seconds=self.milli_seconds)
            if self.count == 1:
                self.lap_time = lap
            else:
                time = int(lap.replace(":", "").replace(".", "")) - int(
                    self.lap_list[-1].replace(":", "").replace(".", ""))
                value = str("0" * (6 - len(str(time)))) + str(time)
                self.lap_time = f"{value[:2]}:{value[2:4]}.{value[4:6]}"
            self.lap_list.append(lap)
            self.ids.stop_watch_container.add_widget(OneLineListItem(text=f"{self.count}    {lap}    +{self.lap_time}"))
            self.count += 1

    def stop_watch(self):
        while True:
            if self.start:
                if self.minutes != 60:
                    if self.seconds != 60:
                        if self.milli_seconds != 99:
                            self.milli_seconds += 1
                            self.ids.stop_watch_time.text = self.check_correct_format(minutes=self.minutes,
                                                                                      seconds=self.seconds,
                                                                                      milli_seconds=self.milli_seconds)
                            time.sleep(0.005)
                        else:
                            self.milli_seconds = 0
                            self.seconds += 1
                    else:
                        self.seconds = 0
                        self.minutes += 1
                else:
                    self.minutes, self.seconds, self.milli_seconds = 0, 0, 0
                    self.start = False

    def check_correct_format(self, minutes, seconds, milli_seconds):
        if (len(str(minutes)) == 1) and (len(str(seconds)) == 1) and (len(str(milli_seconds)) == 1):
            return f"0{minutes}:0{seconds}.0{milli_seconds}"
        elif (len(str(seconds)) == 1) and (len(str(milli_seconds)) == 1):
            return f"{minutes}:0{seconds}.0{milli_seconds}"
        elif (len(str(minutes)) == 1) and (len(str(milli_seconds)) == 1):
            return f"0{minutes}:{seconds}.0{milli_seconds}"
        elif (len(str(minutes)) == 1) and (len(str(seconds)) == 1):
            return f"0{minutes}:0{seconds}.{milli_seconds}"
        elif len(str(seconds)) == 1:
            return f"{minutes}:0{seconds}.{milli_seconds}"
        elif len(str(minutes)) == 1:
            return f"0{minutes}:{seconds}.{milli_seconds}"
        elif len(str(milli_seconds)) == 1:
            return f"{minutes}:{seconds}.0{milli_seconds}"
