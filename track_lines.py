import numpy as np
import cv2
import pickle

from methods import threshold
from methods import find_lane_lines as finder
from methods import draw_lane as dl
from methods import transform_perspective as trp
from methods import warp

from utils.lines import Lines

class TrackLines():
    def __init__(self, n_frames=1):
        self.detected = False
        self.all_fitted_left = []
        self.all_fitted_right = []
        dist_pickle = pickle.load(open( "params/calibration.p", "rb" ))
        self.mtx = dist_pickle[0]
        self.dist = dist_pickle[1]
        self.M = pickle.load(open( "params/perspectiveTransformMatrix.p", "rb" ))
        self.Minv = pickle.load(open( "params/oppositePerspectiveTransformMatrix.p", "rb" ))
        self.n_frames = n_frames
        self.ploty = np.linspace(0, 1280-1, 1280 )
        self.incorrect_frames = 0
        self.pix_per_frame = 20

    def process_image(self, image):
        if len(self.all_fitted_left) > self.n_frames:
            lines = Lines(self.detected, self.all_fitted_left[-self.n_frames:], self.all_fitted_right[-self.n_frames:])
        else:
            lines = Lines(self.detected, self.all_fitted_left, self.all_fitted_right)
        
        dst = cv2.undistort(image, self.mtx, self.dist, None, self.mtx)
        transformed = trp.transform(dst, self.M)
        thresholded = threshold.process_image(transformed)
        warped = warp.process(thresholded)
        left_fitx, right_fitx, ret = finder.find(warped, self.ploty)
        if ret == True:
            self.detected = True
            lines.setCurrentFit(left_fitx, right_fitx)
        else:
            self.detected = False

        left_fit, right_fit, correct = lines.evaluate()
        self.incorrect_frames += 1 if correct == False else -1 if self.incorrect_frames > 0 else 0
        self.all_fitted_left.append(left_fit)
        self.all_fitted_right.append(right_fit)

        curvature = lines.measure(self.ploty)
        vehicle_position = (image.shape[1]/2 - (right_fit[-1] + left_fit[-1])/2) * (3.7/700)
        cut = self.incorrect_frames*self.pix_per_frame
        result = dl.draw(image, warped, self.ploty[cut:], left_fit[cut:], right_fit[cut:], self.Minv)
        cv2.putText(result, 'Radius of curvature: = ' + str(round(curvature, 3)) + 'm',(50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
        cv2.putText(result, 'Position from center  ' + str(round(vehicle_position, 3)) + 'm',(50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
        return result