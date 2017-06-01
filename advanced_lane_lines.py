import cv2
import pickle
import threshold
import find_lane_lines as finder
import curvature_measurement as cm
import matplotlib.pyplot as plt
import draw_lane as dl

dist_pickle = pickle.load( open( "calibration.p", "rb" ) )
mtx = dist_pickle[0]
dist = dist_pickle[1]

M = pickle.load(open( "perspectiveTransformMatrix.p", "rb" ))

def process(image):
    dst = cv2.undistort(image, mtx, dist, None, mtx)
    thresholded = threshold.process_image(dst)
    imshape = image.shape
    transformed = cv2.warpPerspective(thresholded, M, (imshape[1], imshape[0]), flags=cv2.INTER_LINEAR)
    ploty, left_fitx, right_fitx = finder.find(transformed)
    measurements = cm.measure(ploty, left_fitx, right_fitx)
    result = dl.draw(image, transformed, ploty, left_fitx, right_fitx, M)
    return result

image = cv2.imread('test_images/test2.jpg')
result = process(image)
plt.imshow(result)
plt.show()
