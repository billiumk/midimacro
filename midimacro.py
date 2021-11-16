import mido
import json
import keyboard

macros = json.load((open("config.json", "r")))
#  {   "channel": "1", "onchange": "", "onincrease": "", "ondecrease": "", "granularity": 8 },

keymap=[0 for i in range(100)]

with mido.open_input() as inport:
    for msg in inport:
        # control_change channel=0 control=13 time=0
        lines = str(msg).split()
        for i in range(0, len(lines)):
            kvpair = lines[i].split('=')
            if len(kvpair)>1:
                    if(i == 2):
                        channel = int(kvpair[1])
                    if(i == 3):
                        # consume new channel value
                        old_value = keymap[channel]
                        channel_value = int(kvpair[1])
                        print("channel: " + str(channel))
                        for entry in macros["macros"]:
                            if int(entry["channel"]) == int(channel):
                                if int(channel_value)) % int(entry["granularity"]) == 0:
                                    for k in entry["macro"]:
                                        print("sending " + k)
                                        keyboard.press_and_release(k)

