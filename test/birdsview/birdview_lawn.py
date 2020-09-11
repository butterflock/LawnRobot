import cv2
import numpy as np
import matplotlib.pyplot as plt


src = np.float32([[100, 255], [429, 255], [0, 0], [513, 0]])
dst = np.float32([[202, 255], [328, 255], [0, 0], [513, 0]])
M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation

img = cv2.imread('../img/WaveshareCamera.jpg') # Read the test img
img = img[165:420, 0:513] # Apply np slicing for ROI crop

warped_img = cv2.warpPerspective(img, M, (513, 255)) # Image warping
_, ax = plt.subplots(nrows=2)
ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # Show results
ax[1].imshow(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB)) # Show results
plt.show()
