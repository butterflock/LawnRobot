import cv2
import numpy as np


image = cv2.imread("img/1_20200708-213601.jpg")
corners = np.array([[(0, 420), (0, 290), (74, 224), (487, 240), (513, 270), (513, 420)]], dtype=np.int32)
image_overlay = cv2.polylines(image, [corners], isClosed=True, color=(0, 0, 0), thickness=3)

# cv2.imshow("test", image_overlay)
print(type(image))
print(type(image_overlay))
cv2.imshow("test", image)
cv2.waitKey()
