import cv2
import pickle
import matplotlib.pyplot as plt

dist_pickle = pickle.load( open( "params/calibration.p", "rb" ) )
mtx = dist_pickle[0]
dist = dist_pickle[1]

image = cv2.imread('camera_cal/calibration2.jpg')
dst = cv2.undistort(image, mtx, dist, None, mtx)
plt.figure()
plt.imshow(dst)
plt.show()