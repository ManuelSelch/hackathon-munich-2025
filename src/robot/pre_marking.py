import cv2
import numpy as np

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

def mark_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # yellow marker mask
    mask = cv2.inRange(hsv, lower_box, upper_box)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # skip if no contours found
    if not contours: return frame

    # filter only small controus (small yellow circles)
    MAX_AREA = 100
    contours = [c for c in contours if cv2.contourArea(c) < MAX_AREA]

    if not contours: return frame

    # ROI = box around yellow colors
    c = max(contours, key=cv2.contourArea)
    cv2.drawContours(frame, [c], -1, (0, 0, 255), 10)
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
