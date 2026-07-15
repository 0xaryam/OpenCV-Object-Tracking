import cv2
import time
import os
from collections import deque
from datetime import datetime

# =========================
# SETTINGS
# =========================
CAMERA_INDEX = 0
TRAIL_LENGTH = 40

# Create output folders
os.makedirs("screenshots", exist_ok=True)
os.makedirs("recordings", exist_ok=True)

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

tracker = None
tracking = False
trail = deque(maxlen=TRAIL_LENGTH)

recording = False
video_writer = None

previous_time = time.time()
fps = 0


def create_tracker():
    """Create a CSRT object tracker."""
    return cv2.TrackerCSRT_create()


def select_object(frame):
    """Allow the user to select an object."""
    bbox = cv2.selectROI(
        "Select Object - Press ENTER",
        frame,
        fromCenter=False,
        showCrosshair=True
    )

    cv2.destroyWindow("Select Object - Press ENTER")

    if bbox[2] == 0 or bbox[3] == 0:
        return None

    new_tracker = create_tracker()
    new_tracker.init(frame, bbox)

    return new_tracker


def start_recording(frame):
    """Create a new video recording."""
    height, width = frame.shape[:2]

    filename = os.path.join(
        "recordings",
        "tracking_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        filename,
        fourcc,
        20.0,
        (width, height)
    )

    print(f"Recording started: {filename}")

    return writer


print("""
========================================
     SMART OBJECT TRACKING SYSTEM
========================================
R  - Select / Reset Object
S  - Save Screenshot
V  - Start / Stop Video Recording
Q  - Quit
========================================
""")


while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read camera frame.")
        break

    # =========================
    # FPS
    # =========================
    current_time = time.time()
    difference = current_time - previous_time

    if difference > 0:
        current_fps = 1 / difference

        # Smooth FPS value
        if fps == 0:
            fps = current_fps
        else:
            fps = (fps * 0.9) + (current_fps * 0.1)

    previous_time = current_time

    # =========================
    # TRACKING
    # =========================
    status = "WAITING FOR OBJECT"
    status_color = (0, 255, 255)

    position_text = "Position: --"
    size_text = "Object Size: --"

    if tracking and tracker is not None:

        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = [int(value) for value in bbox]

            center_x = x + w // 2
            center_y = y + h // 2

            trail.append((center_x, center_y))

            # Bounding box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Center point
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 255, 0),
                -1
            )

            # Motion trail
            for i in range(1, len(trail)):
                if trail[i - 1] is None or trail[i] is None:
                    continue

                thickness = max(
                    1,
                    int(4 * (i / len(trail)))
                )

                cv2.line(
                    frame,
                    trail[i - 1],
                    trail[i],
                    (255, 0, 255),
                    thickness
                )

            status = "TRACKING ACTIVE"
            status_color = (0, 255, 0)

            position_text = f"Position: ({center_x}, {center_y})"
            size_text = f"Object Size: {w} x {h}"

        else:
            status = "TRACKING LOST"
            status_color = (0, 0, 255)

    # =========================
    # INFORMATION PANEL
    # =========================
    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (10, 10),
        (390, 165),
        (0, 0, 0),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.65,
        frame,
        0.35,
        0,
        frame
    )

    cv2.putText(
        frame,
        "SMART OBJECT TRACKER",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        status,
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        status_color,
        2
    )

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (280, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        position_text,
        (20, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        size_text,
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # =========================
    # RECORDING INDICATOR
    # =========================
    if recording:
        cv2.circle(
            frame,
            (frame.shape[1] - 100, 35),
            8,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            frame,
            "REC",
            (frame.shape[1] - 80, 43),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 255),
            2
        )

    # Controls
    cv2.putText(
        frame,
        "R: Select | S: Screenshot | V: Record | Q: Quit",
        (20, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        2
    )

    # =========================
    # SAVE VIDEO FRAME
    # =========================
    if recording and video_writer is not None:
        video_writer.write(frame)

    cv2.imshow("Smart Object Tracking System", frame)

    key = cv2.waitKey(1) & 0xFF

    # =========================
    # CONTROLS
    # =========================

    # Select or reset object
    if key == ord("r"):
        new_tracker = select_object(frame.copy())

        if new_tracker is not None:
            tracker = new_tracker
            tracking = True
            trail.clear()

    # Screenshot
    elif key == ord("s"):
        filename = os.path.join(
            "screenshots",
            "tracking_" +
            datetime.now().strftime("%Y%m%d_%H%M%S") +
            ".jpg"
        )

        cv2.imwrite(filename, frame)
        print(f"Screenshot saved: {filename}")

    # Start / stop recording
    elif key == ord("v"):

        if not recording:
            video_writer = start_recording(frame)
            recording = True

        else:
            recording = False

            if video_writer is not None:
                video_writer.release()
                video_writer = None

            print("Recording stopped and saved.")

    # Quit
    elif key == ord("q"):
        break


# =========================
# CLEANUP
# =========================
if video_writer is not None:
    video_writer.release()

cap.release()
cv2.destroyAllWindows()

print("Program closed successfully.")