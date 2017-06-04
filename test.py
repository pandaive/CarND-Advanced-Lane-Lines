import cv2
import pickle
import matplotlib.pyplot as plt
from methods import threshold
from methods import transform_perspective as trp
from methods import warp

M = pickle.load(open("params/perspectiveTransformMatrix.p", "rb"))

dist_pickle = pickle.load( open( "params/calibration.p", "rb" ) )
mtx = dist_pickle[0]
dist = dist_pickle[1]

image = cv2.imread('test_images/result_transformed.jpg')
thresholded = threshold.process_image(image)
#warped = warp.process(thresholded)
cv2.imwrite('test_images/result_thresholded.jpg', thresholded)
