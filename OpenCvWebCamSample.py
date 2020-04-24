import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    cv2.imshow('camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        camera.release()
        cv2.destroyAllWindows()
        break

