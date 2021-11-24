import mido
import json
import keyboard
import sys

# load macro mappings from config file
#TODO: command line option for filename
macros = json.load((open("config.json", "r")))

#  {   "channel": "1", "onpress": "", "onchange": "", "onincrease": "", "ondecrease": "", "granularity": 8 },
# configure the behavior for each channel. granularity is
# how many triggers per rotation. 1 is the most sensitive,
# try 2, 4, 8, 16 etc to add dead zones before firing the
# macro again.

# this will store the last value for each
# key to determine if it's increasing or
# decreasing
keymap=[0 for i in range(100)]

# detect device
ports = mido.get_input_names()

# no device detected
if len(ports) == 0:
    sys.stderr.write("ERROR: Couldn't find midi device\n")
    exit(1)

print(ports)
pnum = input("Please select a midi port number: ")
        
# connect and monitor the device messages
with mido.open_input(ports[int(pnum)]) as inport:

    for msg in inport:

        #print(msg)
        # control_change channel=0 control=13 time=0

        lines = str(msg).split()
        for i in range(0, len(lines)):

            # key value pair in message. a=b
            # split it into key and value
            kvpair = lines[i].split('=')

            # if there was a = in that piece
            if len(kvpair)>1:

                    # check the index and parse
                    if(i == 2):
                        channel = int(kvpair[1])

                    if(i == 3):

                        # consume new channel value
                        old_value = keymap[channel]
                        channel_value = int(kvpair[1])
                        keymap[channel] = channel_value

                        # print("channel: " + str(channel))

                        # TODO: put these entries in a map and use the channel as index
                        for entry in macros["macros"]:

                            if int(entry["channel"]) == channel:

                                if entry["onpress"] != "" and int(channel_value) == 127 :
                                    keyboard.press_and_release(entry["onpress"])

                                if int(channel_value) % int(entry["granularity"]) == 0:
                                    # print(channel_value)
                                    # check last value

                                    if entry["onchange"] != "":
                                        keyboard.press_and_release(entry["onchange"])

                                    if entry["ondecrease"] != "" and int(channel_value) < int(old_value):
                                        keyboard.press_and_release(entry["ondecrease"])

                                    if entry["onincrease"] != "" and int(channel_value) > int(old_value):
                                        keyboard.press_and_release(entry["onincrease"])
