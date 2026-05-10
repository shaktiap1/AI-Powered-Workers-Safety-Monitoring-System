# MAIN - this is the main entry point of the application where the video processing loop is implemented. 
# It initializes the person detector, safety analytics, and handles video reading, processing, and output generation.

import cv2
import platform
import os
from detector import PersonDetector
from posture import classify_posture
from safety_rules import get_safety_status
from analytics import SafetyAnalytics

# Create outputs folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Using webcam (camera 0) instead of video file for LIVE input
CAMERA_ID = 0
OUTPUT_VIDEO_PATH = "outputs/processed_video.mp4"


def play_beep():
    """
    Play a simple beep sound when RISK is detected.
    Works cross-platform without additional dependencies.
    """
    system = platform.system()
    
    if system == "Windows":
        import winsound
        winsound.Beep(1000, 200)  # Frequency: 1000Hz, Duration: 200ms
    elif system == "Darwin":  # macOS
        import os
        os.system('afplay /System/Library/Sounds/Alarm.aiff')
    else:  # Linux
        import os
        os.system('beep 2>/dev/null || echo -e "\a"')


def draw_boxes(frame, boxes):
    """
    This function takes a video frame and a list of detected bounding boxes as input.
    For each detected person (represented by a bounding box), it classifies the posture and determines the safety status based on predefined rules.
    """
    postures = []
    safety_states = []
    has_risk = False  # Track if any RISK detected in this frame

    for (x1, y1, x2, y2, conf) in boxes:
        posture = classify_posture(x1, y1, x2, y2)
        safety = get_safety_status(posture)

        postures.append(posture)
        safety_states.append(safety)

        if safety == "SAFE":
            color = (0, 255, 0)  # Green
        elif safety == "MONITOR":
            color = (0, 255, 255)  # Yellow
        else:
            color = (0, 0, 255)  # Red
            has_risk = True  # Flag RISK detection

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        label = f"{posture} | {safety} | {conf:.2f}"

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # Display threat alert on screen if RISK detected
    if has_risk:
        cv2.putText(
            frame,
            "⚠️ THREAT DETECTED - RISK POSTURE IDENTIFIED",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )
        play_beep()  # Play beep sound

    return postures, safety_states


def main():
    """
    Main function that orchestrates the live video processing workflow using webcam input.
    """
    detector = PersonDetector()
    analytics = SafetyAnalytics()

    # Open webcam instead of video file
    cap = cv2.VideoCapture(CAMERA_ID)

    if not cap.isOpened():
        print("Error: Cannot access webcam. Please check your camera connection.")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define codec and create VideoWriter (optional - saves live feed)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (width, height))

    print("Starting live safety monitoring from camera...")
    print("Press 'ESC' to stop monitoring and exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from camera.")
            break

        boxes = detector.detect_people(frame)

        postures, safety_states = draw_boxes(frame, boxes)

        analytics.update(boxes, postures, safety_states)

        # Save frame to output video
        out.write(frame)

        # Display live feed
        cv2.imshow("🔒 Live Worker Safety Monitoring System", frame)

        # Press ESC (key code 27) to exit
        if cv2.waitKey(1) & 0xFF == 27:
            print("\nMonitoring stopped by user.")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    analytics.generate_report()

    print("Processed video saved to:", OUTPUT_VIDEO_PATH)
    print("✅ Live monitoring session ended.")


if __name__ == "__main__":
    main()

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
