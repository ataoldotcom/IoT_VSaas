
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

# Optional: increase webcam resolution
# cap.set(3, 1280)  # width
# cap.set(4, 720)   # height


if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Optional: increase YOLO inference resolution
    # results = model(frame, imgsz=1280)

    results = model(frame)
    annotated = results[0].plot()

    cv2.imshow("YOLO Test", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()