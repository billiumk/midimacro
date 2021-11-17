import mido
import json
import keyboard

macros = json.load((open("config.json", "r")))
#  {   "channel": "1", "onchange": "", "onincrease": "", "ondecrease": "", "granularity": 8 },

keymap=[0 for i in range(100)]

#with mido.open_input() as inport:
with mido.open_input('nanoKONTROL Studio:nanoKONTROL Studio MIDI 1 24:0') as inport:

    for msg in inport:
        print(msg)
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
                        keymap[channel] = channel_value
                        print("channel: " + str(channel))
                        for entry in macros["macros"]:
                            if int(entry["channel"]) == int(channel):
                                if entry["onpress"] != "" and int(channel_value) == 127 :
                                    keyboard.press_and_release(entry["onpress"])
                                if int(channel_value) % int(entry["granularity"]) == 0:
                                    print(channel_value)
                                    # check last value
                                    if entry["onchange"] != "":
                                        keyboard.press_and_release(entry["onchange"])
                                    if entry["ondecrease"] != "" and int(channel_value) < int(old_value):
                                        keyboard.press_and_release(entry["ondecrease"])
                                    if entry["onincrease"] != "" and int(channel_value) > int(old_value):
                                        keyboard.press_and_release(entry["onincrease"])
