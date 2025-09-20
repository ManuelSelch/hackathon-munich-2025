import cv2
import numpy as np
import math
from robot.robot import Robot

robot = Robot()

# input: viddeo
video_path = "test-video-h264.mp4"
video = cv2.VideoCapture(video_path)

# parse video parameters
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(
    "output.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

# yellow marker range
lower_box = np.array([20, 31, 177], dtype=np.uint8)
upper_box = np.array([70, 129, 255], dtype=np.uint8)

def detect_nearest_circle(frame, target):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_box, upper_box)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    tx, ty = target
    nearest = None
    min_dist = float("inf")

    for cnt in contours:
        (u, v), r = cv2.minEnclosingCircle(cnt)
        u, v, r = int(u), int(v), int(r)
        if r < 5:  # filter noise
            continue
        dist = math.hypot(u - tx, v - ty)
        if dist < min_dist:
            min_dist = dist
            nearest = (u, v, r)

    return nearest

def calculate_error(target, detection):
    pass

def mark_frame(frame: cv2.typing.MatLike):
    # target location
    h, w, _ = frame.shape
    x = w // 2 + 20
    y = h // 2 + 50
    target = (x, y)
    cv2.circle(frame, (x, y), 10, (0, 255, 0), 2)

    detection = detect_nearest_circle(frame, target)
    if detection:
        # draw detected circle & error
        u, v, r = detection
        cv2.circle(frame, (u, v), int(r), (255, 0, 0), 2)
        cv2.line(frame, (x, y), (u, v), (0, 0, 255), 2)

        err_x = u - target[0]
        err_y = v - target[1]
        scale = 0.001 # 1px = 0.001 m
        dx = -err_x * scale     # correct x error
        dy = -err_y * scale     # correct y error
        dz = -0.001             # move down slowly

        robot.moveLeftArm(dx, dy, dz)
        
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

    return frame



# step 1: load each frame of video
while video.isOpened():
    ret, frame = video.read()
    if not ret: break

    # step 2: manipulate frame
    processed = mark_frame(frame)

    # step 3: save frame to video
    out.write(processed)

# done
video.release()
out.release()
