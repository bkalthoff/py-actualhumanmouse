import json
import math
import mouse
import humanity
import random
with open('data.json', "r", encoding='utf-8') as file:
            recordings = json.load(file)
clean_record = []
for recording in recordings:
    clean = []
    for record in recording[1]:
        if isinstance(record[0], str):
            clean.append(mouse.ButtonEvent(record[0], record[1], record[2]))
        else:
            clean.append(mouse.MoveEvent(record[0], record[1], record[2]))
    clean_record.append(clean)


def move_to(dest):
    curpos = mouse.get_position()
    dist = round(math.sqrt(math.pow(dest[0] - curpos[0],2) + math.pow(dest[1] - curpos[1],2)))
    print(dist)
    events = []
    found = False
    for i in range(len(clean_record)):
        if dist < recordings[i][0]:
            print(recordings[i][0])
            events = clean_record[i]
            found = True
            break
    if not found:
        events = clean_record[len(clean_record) - 1]
    humanity.move_to(events, dest)
while True:
    move_to((random.randint(500, 1000),random.randint(500, 1000)))