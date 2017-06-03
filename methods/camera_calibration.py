import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import pickle

nx = 9
ny = 6

objpoints, imagepoints = [], []
objp = np.zeros((nx*ny, 3), np.float32)
objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)
calibration_images = glob.glob('../camera_cal/calibration*')

for i, filename in enumerate(calibration_images):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
    if ret == True:
        objpoints.append(objp)
        imagepoints.append(corners)

test_image = cv2.imread('../test_images/straight_lines1.jpg')
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imagepoints, test_image.shape[:2], None, None)

pickle.dump((mtx, dist), open("params/calibration.p", "wb"))
print("Calibration data saved")