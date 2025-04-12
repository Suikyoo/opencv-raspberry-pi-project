import cv2, numpy, sys
import model, cv_draw, camera, core_functs

stream = camera.VideoCapture("assets/sample.mp4")


frame = stream.capture()

size = [len(frame[0]), len(frame)]
interface_size = [int(size[0] * 0.4), int(size[1])]

#scale the interface location: from a normalized value to resolution coordinates
#INTERFACE_LOCATION = numpy.array([int(INTERFACE_LOCATION[i] * size[i]) for i in range(len(INTERFACE_LOCATION))])

detection_model = model.Model()
detection_model.set_capture_size(size)

save_time = core_functs.get_ms()
calc_time = core_functs.get_ms()

while True:
    new_time = core_functs.get_ms() 

    frame = stream.capture()
    interface_frame = cv_draw.create_interface(interface_size)
    
    if (new_time - calc_time) > 1100:
        detection_model.calculate(frame)
        calc_time = new_time

    
    if int(new_time - save_time) > 3000:
        detection_model.save_data()
        save_time = new_time

    detection_model.draw(frame, interface_frame)

    final_frame = numpy.concatenate((frame, interface_frame), axis=1)

    cv2.imshow("Window", final_frame)
    if cv2.waitKey(60) & 0xFF == ord('q'):
        break


stream.release()
cv2.destroyAllWindows()
