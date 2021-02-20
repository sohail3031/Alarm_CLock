from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, ILeftBodyTouch, TwoLineAvatarIconListItem
from threading import Thread
from datetime import datetime
from pygame import mixer
from kivymd.uix.button import MDFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.toast import toast

update_alarm_time = ""
dialog = None
add_weekdays, all_alarm_data = [], []
flag = False
alarm_time = ""
mixer.init()


def show_dialog(text):
    dialog = MDDialog(
        text=f"{text}\n\n",
        buttons=[MDRaisedButton(text="OK", on_release=lambda _: dialog.dismiss())]
    )
    dialog.open()


class RightSwitch(IRightBodyTouch, MDBoxLayout):
    '''Custom right container.'''


class CustomOneLineListItemAlarm(TwoLineAvatarIconListItem):
    '''Custom list item.'''

    def __init__(self, **kwargs):
        super(CustomOneLineListItemAlarm, self).__init__(**kwargs)
        self.set_alarm()

    def get_date_index(self):
        return self.parent.get_view_index_at(self.center)

    @property
    def rv(self):
        return self.parent.recycleview

    def on_release(self, text="", status=True):
        remove = self.get_date_index()
        if status:
            self.rv.data.pop(remove)
            with open("my_alarm_save.txt", "r") as file1:
                data = file1.readlines()
                item = data[remove]
                with open("my_alarm_save.txt", "w") as file2:
                    for i in range(len(data)):
                        if i != remove:
                            file2.write(data[i])
            toast(f"Alarm at time {item.split('---')[0]} is deleted")
        else:
            self.rv.data.remove(text)

    def change_state(self, text, status):
        with open("my_alarm_save.txt", "r") as file1:
            data = file1.readlines()
            with open("my_alarm_save.txt", "w") as file:
                if file:
                    for i in data:
                        if text in i:
                            file.write(
                                f"{i.split('---')[0]}---{i.split('---')[1]}---{'on' if status else 'off'}\n")
                        else:
                            file.write(f"{i}")

    def set_alarm(self):
        with open("my_alarm_save.txt", "r") as file:
            for i in file.readlines():
                if "on" in i:
                    self.ids.switch.active = True


class CheckboxRightWidget(MDCheckbox, ILeftBodyTouch):
    pass


class Days(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check, text):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
            else:
                check.active = True
        if text not in add_weekdays:
            add_weekdays.append(text)

    def display_results(self, checkbox, status):
        if status:
            add_weekdays.append(checkbox)
        else:
            add_weekdays.remove(checkbox)


class AddEmptySpace(OneLineAvatarIconListItem):
    divider = None


class AlarmClock(Screen):
    dialog = None
    week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def __init__(self, **kwargs):
        super(AlarmClock, self).__init__(**kwargs)
        self.ids.rv.data = []
        self.search_alarms()
        thread = Thread(target=self.background_process)
        thread.daemon = True
        thread.start()

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

    def background_process(self):
        while True:
            with open("my_alarm_save.txt", "r") as file:
                data = file.readlines()
                date = datetime.now().strftime("%H:%M:%S")
                day = datetime.now().strftime("%A")
                for i in data:
                    if (date in i) and ("on" in i) and (day in i):
                        self.show_dialog(text="Time's Up")
                        with open("selected_alarm_ringtone.txt", "r") as file:
                            data = file.readlines()
                        name = data[0].replace("\n", "")
                        mixer.music.load(f"ringtones/{name}.mp3")
                        mixer.music.play()

    def search_alarms(self, text="", status=True, days=None):
        if days is None:
            days = []

        def add_alarms(alarm_time, alarm_days=None):
            if alarm_days is None:
                alarm_days = []

            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineListItemAlarm",
                    "text": alarm_time,
                    "secondary_text": ", ".join(alarm_days),
                    "callback": lambda x: x,
                }
            )

        if status:
            with open("my_alarm_save.txt", "r") as file:
                for i in file.readlines():
                    add_alarms(alarm_time=i.split("---")[0], alarm_days=i.split("---")[1].split(" "))
        else:
            toast(f"Alarm set at time {text}")
            add_alarms(str(text), alarm_days=days)

    def show_time_picker(self, flag=False):
        time_dialog = MDTimePicker()
        if flag:
            time_dialog.bind(time=CustomOneLineListItemAlarm().update_alarm)
        else:
            time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        global alarm_time
        alarm_time = time
        self.open_weekdays_dialog()

    def open_weekdays_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Select Days",
                type="confirmation",
                items=[
                    *[Days(text=i) for i in self.week_days],
                    *[AddEmptySpace(text="") for i in range(4)]
                ],
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda _: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="OK", on_release=self.ok_button_clicked
                    ),
                ],
            )

        self.dialog.open()

    def ok_button_clicked(self, instance):
        global alarm_time
        if add_weekdays:
            with open("my_alarm_save.txt", "a") as file:
                file.write(f"{str(alarm_time)}---{' '.join(add_weekdays)}---on\n")
            self.search_alarms(text=alarm_time, status=False, days=add_weekdays)
        self.dialog.dismiss()
