from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarListItem
from kivy.properties import StringProperty
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivymd.toast import toast
from pygame import mixer

Builder.load_file("check_ringtone_kv.kv")

selected_ringtone = []
selected = 0
mixer.init()


def music_controller(name):
    mixer.music.stop()
    if name:
        name = name.replace("\n", "")
        mixer.music.load(f"ringtones/{name}.mp3")
        mixer.music.play()


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # preview=True,
        )

    # def add_new_ringtone(self):
    #     pass
    # path = "/"
    # file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
    # file_manager.close()

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        toast(path)
        print(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


class CheckboxLeftWidget(MDCheckbox, ILeftBodyTouch):
    pass


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check, text):
        global selected
        selected_ringtone.append(text)
        selected = -2
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
        music_controller(name=text)

    def display_results(self, checkbox):
        global selected
        selected_ringtone.append(checkbox)
        selected = -1
        music_controller(name=checkbox)


class ShowAllRingtones:
    dialog = None

    def show_confirmation_dialog(self):
        with open("all_alarms_ringtone.txt", "r") as file:
            data = file.readlines()
        if not self.dialog:
            self.dialog = MDDialog(
                title="Alarm ringtone",
                type="confirmation",
                items=[*[ItemConfirm(text=i) for i in data],
                       Item(text="Add Ringtone", source="images/new_add_icon.png")],
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda _: self.dialog.dismiss(), on_press=self.stop_music
                    ),
                    MDFlatButton(
                        text="OK", on_release=self.save_new_ringtone, on_press=self.stop_music
                    ),
                ],
            )

        self.dialog.open()

    def stop_music(self, inst):
        mixer.music.stop()

    def save_new_ringtone(self, inst):
        if (selected == -1) or (selected == -2):
            with open("selected_alarm_ringtone.txt", "w") as file:
                file.write(selected_ringtone[selected])
        self.dialog.dismiss()
