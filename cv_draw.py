import cv2, numpy

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_WIDTH = 2
LINE_TYPE = cv2.LINE_AA
TEXT_OFFSET = numpy.array([10, 30])

#shrink factor for videocaptures
SHRINK_FACTOR = 1


def create_interface(size):
    return numpy.full((size[1], size[0], 3), 0.2, dtype=numpy.uint8)

def draw_interface(frame, stats):
    index = 0
    for k in stats.keys():
        draw_text(frame, [index], (100, 100 + index * 50), f"{k}: {stats[k]}")
        index += 1

    #light logic

    state = "LOW"
    
    if stats["Pedestrian"]:
        state = "MEDIUM"

    if stats["2-wheeler"] + stats["4-wheeler"] > 2:
        state = "HIGH"

    draw_text(frame, (255, 255, 255), (100, 500), f"Light State: {state}")

def draw_text(frame, color, location, text):
    cv2.putText(frame, text, location, FONT, FONT_SCALE, color, FONT_WIDTH, LINE_TYPE)

def shrink(frame):
    return cv2.resize(frame, (int(len(frame[0]) * SHRINK_FACTOR), int(len(frame) * SHRINK_FACTOR)))
