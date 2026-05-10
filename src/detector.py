# DETECTOR - this class is responsible for loading the YOLOv8 model and performing object detection on video frames to identify and locate people in the scene.


from ultralytics import YOLO


class PersonDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.4):
        """
        Initialize YOLO model.
        - model_path: pretrained YOLO weights
        - conf_threshold: minimum confidence for detections
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect_people(self, frame):
        """
        Detect only 'person' class in the frame.

        Returns:
        - List of bounding boxes [(x1, y1, x2, y2, confidence)]
        """
        results = self.model(frame, conf=self.conf_threshold, verbose=False)[0]

        person_boxes = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]

            if label == "person":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                person_boxes.append((x1, y1, x2, y2, conf))

        return person_boxes
