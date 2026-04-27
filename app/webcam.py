import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import colors
from detection_filters import is_target_detection

# Load model
model = YOLO("yolov8n.pt")

# Target classes
TARGET_CLASSES = []

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame)

    # Loop through detections
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Filter for target classes
            if is_target_detection(class_name, TARGET_CLASSES):
                # Confidence
                confidence = float(box.conf[0])
                label = f"{class_name} {confidence:.2f}"

                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])

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

                # Draw filled rectangle background
                cv2.rectangle(
                    frame,
                    (x1, y1 - text_height - 12),
                    (x1 + text_width + 8, y1),
                    color,
                    -1
                )

                # Draw text (white)
                cv2.putText(
                    frame,
                    label,
                    (x1 +4, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (255, 255, 255),
                    thickness
                )

    # Show frame
    cv2.imshow("No filtering", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
