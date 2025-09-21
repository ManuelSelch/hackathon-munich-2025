import cv2
import numpy as np
import math
from robot.robot import Robot
from robot.translator import get_pixel_world_coordinate
robot = Robot()
robot.connect()

robot.move_left_arm(0, 0, 0)

# input: viddeo
video_path = "pickEcuHolder.mp4"
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

def filter_range(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lower, upper)

def detect_nearest_circle(frame, target):
    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

def calculate_target(frame: cv2.typing.MatLike):
    h, w, _ = frame.shape
    x = w // 2 + 20
    y = h // 2 + 50
    return (x, y)

def calculate_error(target, detection):
    u, v, _ = detection
    err_x = u - target[0]
    err_y = v - target[1]
    return (err_x, err_y)

def draw_error(target, detection):
    x, y = target
    u, v, r = detection

    cv2.circle(frame, (target[0], target[1]), 10, (0, 255, 0), 2)
    cv2.circle(frame, (u, v), int(r), (255, 0, 0), 2)
    cv2.line(frame, (x, y), (u, v), (0, 0, 255), 2)

def process_frame(frame: cv2.typing.MatLike):
    target = calculate_target(frame)

    frame = filter_range(frame, lower_box, upper_box)
    detection = detect_nearest_circle(frame, target)
    if detection is None: 
        return frame # skip if no circle found
        
    err = calculate_error(target, detection)
    draw_error(target, detection)

    depth, _ = robot.get_left_depth()
    u, v = detection[0], detection[1]
    x, y, z = get_pixel_world_coordinate(u, v, depth[v, u])

    robot.move_abs_left_arm(x, y, z)

    return frame

while False:
    frame = robot.get_left_rgb()
    processed = process_frame(frame)

    if processed.dtype != np.uint8:
        processed = np.clip(processed * 255, 0, 255).astype(np.uint8)
    out.write(processed)

while video.isOpened():
    ret, frame = video.read()
    if not ret: break

    processed = process_frame(frame)

    if processed.dtype != np.uint8:
        processed = np.clip(processed * 255, 0, 255).astype(np.uint8)
    out.write(processed)


# done
video.release()
out.release()
