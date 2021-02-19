from datetime import datetime
from pygame import mixer
from win10toast import ToastNotifier

mixer.init()

while True:
    with open("my_alarm_save.txt", "r") as file:
        data = file.readlines()
        date = datetime.now().strftime("%H:%M:%S")
        for i in data:
            if (date in i) and ("on" in i):
                ToastNotifier().show_toast("Alarm", "Alarm Time", duration=5)
                with open("selected_alarm_ringtone.txt", "r") as file:
                    data = file.readlines()
                name = data[0].replace("\n", "")
                mixer.music.load(f"ringtones/{name}.mp3")
                mixer.music.play()
