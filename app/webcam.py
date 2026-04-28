import cv2
import os
import time
from pathlib import Path
from ultralytics import YOLO
from ultralytics.utils.plotting import colors
from detection_filters import filter_detections
from kafka_producer import producer, send_event


# Load model (allow env override; default to file next to this script)
model_path = os.getenv("YOLO_MODEL_PATH")
if not model_path:
    model_path = str(Path(__file__).resolve().with_name("yolov8n.pt"))
model = YOLO(model_path)

#Flask video stream path
FRAME_PATH = "latest_frame.jpg"
TEMP_FRAME_PATH = "latest_frame_tmp.jpg"

# Target classes
TARGET_CLASSES = []

# Kafka Cooldown (debounce)
LAST_EVENT_TIME = 0
COOLDOWN_SECONDS = 3  # can be adjusted as needed

# Start webcam
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference
        results = model(frame)

        # Loop through detections
        for result in results:
            detections = []

            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append(
                    {
                        "class_id": class_id,
                        "class_name": class_name,
                        "confidence": confidence,
                        "box": (x1, y1, x2, y2),
                    }
                )

            filtered_detections = filter_detections(detections, TARGET_CLASSES)

            for detection in filtered_detections:
                class_id = detection["class_id"]
                class_name = detection["class_name"]
                confidence = detection["confidence"]
                x1, y1, x2, y2 = detection["box"]

                label = f"{class_name} {confidence:.2f}"

                if class_name == "dog" and confidence >= 0.5:
                    current_time = time.time()

                    if current_time - LAST_EVENT_TIME > COOLDOWN_SECONDS:
                        send_event(confidence)
                        LAST_EVENT_TIME = current_time

                # Per-class color (matches Ultralytics palette)
                color = colors(class_id, True)

                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

                # Label (YOLO-style)
                font_scale = 1.6
                thickness = 3

                (text_width, text_height), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
                )

                # Keep label background/text inside the frame near top edge.
                label_top = max(0, y1 - text_height - 12)
                label_bottom = max(text_height + 12, y1)
                text_y = max(text_height + 4, label_bottom - 5)

                # Draw filled rectangle background
                cv2.rectangle(
                    frame,
                    (x1, label_top),
                    (x1 + text_width + 8, label_bottom),
                    color,
                    -1,
                )

                # Draw text (white)
                cv2.putText(
                    frame,
                    label,
                    (x1 + 4, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (255, 255, 255),
                    thickness,
                )

        # Send processed frame to Flask UI
        cv2.imwrite(TEMP_FRAME_PATH, frame)
        os.replace(TEMP_FRAME_PATH, FRAME_PATH)

        # Show processed frame on local machine
        cv2.imshow("No filtering", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    cap.release()
    cv2.destroyAllWindows()
    producer.flush(5.0)
