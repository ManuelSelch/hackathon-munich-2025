import cv2
import numpy as np

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

def mark_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # yellow marker mask
    mask = cv2.inRange(hsv, lower_box, upper_box)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # skip if no contours found
    if not contours: return frame

    # ROI = box around yellow colors
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    cv2.drawContours(frame, [c], -1, (0, 0, 255), 10)

    # crop ROI
    roi = frame[y:y+h, x:x+w]

    # convert ROI to to gray
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)

    # detect circles
    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=1,
        param1=5,
        param2=30,
        minRadius=2,
        maxRadius=20
    )

    # skip if no circles found
    if circles is None: return frame

    # mark circles
    # circles = np.uint16(np.around(circles))
    # for (cx, cy, r) in circles[0, :]:
    #    cv2.circle(frame, (x + cx, y + cy), r, (0, 255, 0), 50)

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
