import numpy, cv2, datetime
import core_functs, cv_draw

class Model:
    def __init__(self):
        #colors for pedestrians(0), 2-wheelers(1), and 4-wheelers(2)
        self.colors  = numpy.random.uniform(0, 255, size=(3, 3))

        self.proto = "models/MobileNetSSD_deploy.prototxt"
        self.caffe = "models/MobileNetSSD_deploy.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(self.proto, self.caffe)

        self.classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
        self.classification = ["Pedestrian", "2-wheeler", "4-wheeler"]

        self.scale = 0.8

        #bicycle - 1
        #bus - 2
        #car - 2
        #motorbike - 1
        #person 0

        self.allowed_classes = {
                2: 1, 
                6: 2, 
                7: 2, 
                14: 1, 
                15: 0
                }

        self.scale = 0.9

        self.boxes = []
        self.current_classification_data = {k : 0 for k in self.classification} 
        self.cumulative_classification_data = {k : 0 for k in self.classification} 


    def set_capture_size(self, size):
        self.capture_size = size

        self.detection_margin = 120
        self.detection_padding = 230

        self.detection_axis_values = [self.capture_size[i] - self.detection_margin for i in range(2)] 

    def calculate(self, frame):

        blob = cv2.dnn.blobFromImage(frame, 0.007843, [int(self.capture_size[i] * self.scale) for i in range(2)], 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()


        self.current_classification_data = {k : 0 for k in self.classification} 

        self.boxes = []

        for i in numpy.arange(0, detections.shape[2]):
            index = int(detections[0, 0, i, 1])

            if index not in self.allowed_classes.keys():
                continue

            confidence = detections[0, 0, i, 2]

            if confidence > 0.7:

                box = detections[0, 0, i, 3:7] * numpy.array([*self.capture_size, *self.capture_size])
                (left, top, right, bottom) = box.astype("int")
                label = f"{self.classes[index]}({self.classification[self.allowed_classes[index]]}): {(confidence * 100):.2f}%"

                classification = self.classification[self.allowed_classes[index]]
                self.current_classification_data[classification] += 1

                center_point = (int(left + (right - left) / 2), int(top + (bottom - top) / 2))

                if classification in ("Pedestrian"): 
                    if (self.detection_axis_values[0] - center_point[0]) > self.detection_padding:
                        continue

                elif classification in ("2-wheeler", "4-wheeler"): 
                    if (self.detection_axis_values[1] - center_point[1]) > self.detection_padding:
                        continue

                self.cumulative_classification_data[classification] += 1
                self.boxes.append((label, self.colors[self.allowed_classes[index]], left, top, right, bottom))

    def draw_detection_lines(self, frame):
        cv2.line(frame, (self.detection_axis_values[0], 0), (self.detection_axis_values[0], self.capture_size[1]), (20, 200, 250), self.detection_padding)
        cv2.line(frame, (0, self.detection_axis_values[1]), (self.capture_size[0], self.detection_axis_values[1]), (200, 200, 20), self.detection_padding)

    #a "box" include both the rect and the text
    def draw_boxes(self, frame):
        for (text, color, left, top, right, bottom) in self.boxes:
            cv2.rectangle(frame, (left, top), (right, bottom), color, 5)
            cv_draw.draw_text(frame, color, numpy.array([left, bottom]) + cv_draw.TEXT_OFFSET, text)

    def draw_texts(self, frame):

        cv_draw.draw_text(frame, (255, 255, 255), (30, 30), "Passed:")
        start_location = (30, 60)
        index = 0
        
        for k, v in self.cumulative_classification_data.items():
            text = f"{k}: {v}"
            cv_draw.draw_text(frame, self.colors[index], (start_location[0], start_location[1] + 30 * index), text)
            index += 1

        cv_draw.draw_text(frame, (255, 255, 255), (30, 250), "Current:")
        start_location = (30, 280)
        index = 0
        
        for k, v in self.current_classification_data.items():
            text = f"{k}: {v}"
            cv_draw.draw_text(frame, self.colors[index], (start_location[0], start_location[1] + 30 * index), text)
            index += 1


        state = "LOW"
        
        if self.current_classification_data["Pedestrian"]:
            state = "MEDIUM"

        if self.current_classification_data["2-wheeler"] + self.current_classification_data["4-wheeler"] > 2:
            state = "HIGH"

        cv_draw.draw_text(frame, (255, 255, 255), (30, 500), f"Light State: {state}")

    def draw(self, capture_frame, interface_frame):
        self.draw_boxes(capture_frame)
        self.draw_texts(interface_frame)

    def save_data(self):
        current_date = datetime.datetime.now().strftime("%b-%d-%Y_%I-%M-%p")
        core_functs.create_json(f'data/{"-".join(current_date.split(" "))}.json', self.cumulative_classification_data)


