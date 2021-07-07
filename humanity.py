from os import environ
import mouse
import time
import math

def normalize(events, dest):
    last_move = 0
    first_move = 0
    result = []
    init_pos = mouse.get_position()
    for i in reversed(range(1, len(events))):
        if isinstance(events[i], mouse.ButtonEvent) and isinstance(events[i - 1], mouse.MoveEvent):
            last_move = (events[i - 1].x, events[i - 1].y)
            break
    for i in range(0, len(events)):
        if isinstance(events[i], mouse.MoveEvent):
            first_move = (events[i].x, events[i].y)
            break

    angle = math.atan2(first_move[0] - last_move[0], first_move[1] - last_move[1]) + math.atan2(dest[1] - init_pos[1], dest[0] - init_pos[0]) + math.pi / 2

    for i in range(0, len(events)):
        if isinstance(events[i], mouse.ButtonEvent):
            result.append(mouse.ButtonEvent(events[i].event_type, events[i].button, events[i].time))
            continue
        ox, oy = first_move
        px, py = events[i].x, events[i].y

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy) - ox
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy) - oy
        result.append(mouse.MoveEvent(round(qx), round(qy), events[i].time))
    return result


def scale(events, dest):
    i = 0
    for i in reversed(range(1, len(events))):
        if isinstance(events[i], mouse.ButtonEvent) and isinstance(events[i - 1], mouse.MoveEvent):
            last_move = (events[i - 1].x, events[i - 1].y)
            i -= 1
            break
    curpos = mouse.get_position()
    c_dist = math.sqrt(math.pow(events[i].x - events[0].x, 2) + math.pow(events[i].y - events[0].y, 2))
    dist = math.sqrt(math.pow(dest[0] - curpos[0], 2) + math.pow(dest[1] - curpos[1], 2))
    factor = dist / c_dist
    print(c_dist, dist, factor)
    for i, event in enumerate(events):
        if isinstance(event, mouse.MoveEvent):
            events[i] = mouse.MoveEvent(round(event.x*factor), round(event.y*factor), event.time)
    i = 0
    while i < len(events) - 1:
        if isinstance(events[i], mouse.MoveEvent) and isinstance(events[i + 1], mouse.MoveEvent):
            if events[i].x == events[i + 1].x and events[i].y == events[i + 1].y:
                del events[i + 1]
                continue
        i += 1

    return events

def move_to(events, dest, include_clicks=True, include_moves=True, include_wheel=False):
    events = normalize(events, dest)
    events = scale(events, dest)
    i = 0
    init_pos = mouse.get_position()
    t_start = time.time()
    while i < len(events):
        t_now = time.time()
        if t_now - t_start > events[i].time - events[0].time:
            if isinstance(events[i], mouse.ButtonEvent) and include_clicks:
                if events[i].event_type == mouse.UP:
                    mouse.release(events[i].button)
                else:
                    mouse.press(events[i].button)
            elif isinstance(events[i], mouse.MoveEvent) and include_moves:
                mouse.move(events[i].x + init_pos[0], events[i].y + init_pos[1])
            elif isinstance(events[i], mouse.WheelEvent) and include_wheel:
                mouse.wheel(events[i].delta)
            i+=1




