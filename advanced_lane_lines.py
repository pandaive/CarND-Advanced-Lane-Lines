import cv2
import pickle
import threshold
import find_lane_lines as finder
import curvature_measurement as cm
import matplotlib.pyplot as plt
import draw_lane as dl
import transform_perspective as trp
import glob
import warp

dist_pickle = pickle.load( open( "calibration.p", "rb" ) )
mtx = dist_pickle[0]
dist = dist_pickle[1]

M = pickle.load(open( "perspectiveTransformMatrix.p", "rb" ))
Minv = pickle.load(open( "oppositePerspectiveTransformMatrix.p", "rb" ))

def process(image):
    dst = cv2.undistort(image, mtx, dist, None, mtx)
    transformed = trp.transform(dst, M)
    plt.figure()
    plt.imshow(transformed)
    imshape = image.shape
    thresholded = threshold.process_image(transformed)
    warped = warp.process(thresholded)
    plt.figure()
    plt.imshow(warped)
    ploty, left_fitx, right_fitx, ret = finder.find(warped)
    
    plt.plot(left_fitx, ploty, color='yellow')
    plt.plot(right_fitx, ploty, color='yellow')
    plt.xlim(0, 1280)
    plt.ylim(720, 0)
    if ret == False:
        return image
    measurements = cm.measure(ploty, left_fitx, right_fitx)
    result = dl.draw(image, warped, ploty, left_fitx, right_fitx, Minv)
    return result


test_images = glob.glob('test_images/*')
images = []
for i, filename in enumerate(test_images):
    img = cv2.imread(filename)
    result = process(img)
    plt.figure()
    plt.imshow(result)
    plt.show()
