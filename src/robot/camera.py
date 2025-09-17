import cv2
import numpy as np

img = cv2.imread("test-img.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)

cv2.imshow("Detected Screws", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Detect circles (screws)
circles = cv2.HoughCircles(
    blur, 
    cv2.HOUGH_GRADIENT, 
    dp=1.2,     # resolution ratio
    minDist=1,  # min distance between screws
    param1=5,   # edge threshold
    param2=30,  # accumulator threshold
    minRadius=1, 
    maxRadius=20
)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for (x, y, r) in circles[0, :]:
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)  # outline
        cv2.circle(img, (x, y), 2, (0, 0, 255), 3)  # center


cv2.imshow("Detected Screws", img)
cv2.waitKey(0)
cv2.destroyAllWindows()