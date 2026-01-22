import cv2
from ultralytics import YOLO
import math

class Sentinel:
    def __init__(self):
        print("Loading AI Model")
        self.model = YOLO('yolov8n.pt')
        
        self.PHONE_CLASS_ID = 67
        self.CONFIDENCE_THRESHOLD = 0.3

    def detect_phone(self, frame):
        results = self.model(frame, verbose=False)

        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = self.model.names[cls_id] 
                if conf > 0.2:
                    print(f"Saw: {name} ({conf:.2f})")

                if cls_id == self.PHONE_CLASS_ID and conf > self.CONFIDENCE_THRESHOLD:
                    return True, box.xyxy[0].tolist()

        return False, None

if __name__ == "__main__":
    sentinel = Sentinel()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    print("Sentinel Active. Press 'q' to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        found_phone, coords = sentinel.detect_phone(frame)

        if found_phone:
            x1, y1, x2, y2 = map(int, coords)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, "PHONE DETECTED", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Focus Mode: Safe", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Sentinel Test', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()