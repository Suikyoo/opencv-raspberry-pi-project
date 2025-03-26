import cv2, numpy, pygame, sys



FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_WIDTH = 2
LINE_TYPE = cv2.LINE_AA
TEXT_OFFSET = numpy.array([10, 30])

PROTO = "models/MobileNetSSD_deploy.prototxt"
CAFFE = "models/MobileNetSSD_deploy.caffemodel"

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

#ALLOWED_CLASSES = list(range(len(CLASSES)))

CLASSIFICATION = ["Pedestrian", "2-wheeler", "4-wheeler"]

#colors for pedestrians(0), 2-wheelers(1), and 4-wheelers(2)
COLORS = numpy.random.uniform(0, 255, size=(3, 3))

#bicycle - 1
#bus - 2
#car - 2
#motorbike - 1
#person 0
ALLOWED_CLASSES = {
        2: 1, 
        6: 2, 
        7: 2, 
        14: 1, 
        15: 0
        }

NET = cv2.dnn.readNetFromCaffe(PROTO,CAFFE)

def draw_text(frame, color, location, text):
    cv2.putText(frame, text, location, FONT, FONT_SCALE, color, FONT_WIDTH, LINE_TYPE)

def calculate_boxes(frame, boxes, size, scale):
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, [int(size[i] * scale) for i in range(2)], 127.5)
    NET.setInput(blob)
    detections = NET.forward()

    boxes.clear()

    classification_stats = {k : 0 for k in CLASSIFICATION}

    for i in numpy.arange(0, detections.shape[2]):
        index = int(detections[0, 0, i, 1])

        if index not in ALLOWED_CLASSES.keys():
            continue


        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * numpy.array([width, height, width, height])
            (left, top, right, bottom) = box.astype("int")
            label = f"{CLASSES[index]}({CLASSIFICATION[ALLOWED_CLASSES[index]]}): {(confidence * 100):.2f}%"
            boxes.append((label, COLORS[ALLOWED_CLASSES[index]], left, top, right, bottom))
            classification_stats[CLASSIFICATION[ALLOWED_CLASSES[index]]] += 1
            
    return classification_stats


#a "box" include both the rect and the text
def draw_boxes(frame, box_list):
    for (text, color, left, top, right, bottom) in box_list:
        cv2.rectangle(frame, (left, top), (right, bottom), color, 5)
        draw_text(frame, color, numpy.array([left, bottom]) + TEXT_OFFSET, text)


def create_interface(size):
    return numpy.full((size[1], size[0], 3), 0.2)

def draw_interface(frame, stats):
    index = 0
    for k in stats.keys():
        draw_text(frame, COLORS[index], (100, 100 + index * 50), f"{k}: {stats[k]}")
        index += 1

    #light logic

    state = "LOW"
    
    if stats[CLASSIFICATION[0]]:
        state = "MEDIUM"

    if stats[CLASSIFICATION[1]] + stats[CLASSIFICATION[2]] > 2:
        state = "HIGH"

    draw_text(frame, (255, 255, 255), (100, 500), f"Light State: {state}")

video_capture = cv2.VideoCapture("assets/sample2.mp4")

frame = video_capture.read()[1]
size = [len(frame[0]), len(frame)]
interface_size = [int(size[0] * 0.4), int(size[1])]
#scale the interface location: from a normalized value to resolution coordinates
#INTERFACE_LOCATION = numpy.array([int(INTERFACE_LOCATION[i] * size[i]) for i in range(len(INTERFACE_LOCATION))])


timer = 0
clock = pygame.time.Clock()

boxes = []
statistics = {k : 0 for k in CLASSIFICATION}

#pygame code
screen = pygame.display.set_mode(((size[0] + interface_size[0]) * 0.7, size[1] * 0.7))

while True:

    ret, frame = video_capture.read()
    interface_frame = create_interface(interface_size)

    timer = (timer + 1) % 10

    if not ret:
        break

    if not timer:
        statistics = calculate_boxes(frame, boxes, size, 0.8)

    draw_boxes(frame, boxes)
    draw_interface(interface_frame, statistics)


    frame = cv2.rotate(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), cv2.ROTATE_90_COUNTERCLOCKWISE)
    interface_frame = cv2.rotate(interface_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #pygame code

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            video_capture.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    screen.fill((60, 60, 60))

    frame = pygame.transform.flip(pygame.transform.scale_by(pygame.surfarray.make_surface(frame), 0.7), True, False)
    interface_frame = pygame.transform.flip(pygame.transform.scale_by(pygame.surfarray.make_surface(interface_frame), 0.7), True, False)
    screen.blit(frame, (0, 0))
    screen.blit(interface_frame, (frame.get_width() + 1, 0))

    clock.tick(30)
    pygame.display.flip()




