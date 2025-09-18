import cv2
import numpy as np

# input: viddeo
video_path = "vide.mp4"
video = cv2.VideoCapture(video_path)

# parse video parameters
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(
    video_path,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

# step 1: load each frame of video
img = cv2.imread("test-img.png")


# step 2: manipulate frame
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# yellow marker
lower_box = np.array([20, 31, 177], dtype=np.uint8)
upper_box = np.array([70, 129, 255], dtype=np.uint8)


def pickLower0(value):
    lower_box[0] = value
    refresh()

def pickLower1(value):
    lower_box[1] = value
    refresh()

def pickLower2(value):
    lower_box[2] = value
    refresh()


def pickUpper0(value):
    upper_box[0] = value
    refresh()

def pickUpper1(value):
    upper_box[1] = value
    refresh()

def pickUpper2(value):
    upper_box[2] = value
    refresh()

def refresh():
    mask = cv2.inRange(hsv, lower_box, upper_box)
    result = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("Filtered", result)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("H_min", "Trackbars", lower_box[0], 255, pickLower0)
cv2.createTrackbar("H_max", "Trackbars", lower_box[1], 255, pickLower1)
cv2.createTrackbar("S_min", "Trackbars", lower_box[2], 255, pickLower2)
cv2.createTrackbar("S_max", "Trackbars", upper_box[0], 255, pickUpper0)
cv2.createTrackbar("V_min", "Trackbars", upper_box[1], 255, pickUpper1)
cv2.createTrackbar("V_max", "Trackbars", upper_box[2], 255, pickUpper2)
cv2.waitKey(0)
cv2.destroyAllWindows()


def detect_circles():
    # mask 
    mask = cv2.inRange(hsv, lower_box, upper_box)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Assume largest red box is the ROI
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        cv2.drawContours(img, [c], -1, (0, 0, 255), 2)

        # Crop ROI from original image
        roi = img[y:y+h, x:x+w]

        # Convert ROI to grayscale & blur
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)

        # Detect circles inside ROI
        circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=1,
            param1=5,
            param2=30,
            minRadius=10,
            maxRadius=20
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for (cx, cy, r) in circles[0, :]:
                cv2.circle(img, (x + cx, y + cy), r, (0, 255, 0), 50)

detect_circles()

cv2.imshow("Detected Screws in ROI", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# step 3: save frame to video

# done