import mouse
import json
import math
import mouse
import keyboard


while(True):
    try:
        with open('data.json', "r", encoding='utf-8') as file:
            recordings = json.load(file)
    except:
        recordings = []

    recording = []                 #This is the list where all the events will be stored
    mouse.hook(recording.append)   #starting the recording
    keyboard.wait("q")          #Waiting for 'a' to be pressed
    mouse.unhook(recording.append) #Stopping the recording
    last_move = 0
    first_move = 0
    init_pos = mouse.get_position()
    for i in reversed(range(1, len(recording))):
        if isinstance(recording[i], mouse.ButtonEvent) and isinstance(recording[i - 1], mouse.MoveEvent):
            last_move = (recording[i - 1].x, recording[i - 1].y)
            break
    for i in range(0, len(recording)):
        if isinstance(recording[i], mouse.MoveEvent):
            first_move = (recording[i].x, recording[i].y)
            break
    
    for i in range(0, len(recording)):
        if isinstance(recording[i], mouse.ButtonEvent):
            recording[i] = mouse.ButtonEvent(recording[i].event_type, 'right', recording[i].time)
    dist = math.sqrt(math.pow(last_move[0] - first_move[0], 2) + math.pow(last_move[1] - first_move[1], 2))
    dist = math.floor(dist)

    recordings.append((dist, recording))
    recordings = sorted(recordings, key=lambda tup: tup[0])

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(recordings, f, ensure_ascii=False, indent=4)
    print('saved')