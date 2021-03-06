import numpy as np
import cv2

def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255):
    #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray=img
    sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0) if orient == 'x' else cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    abs_sobel = np.absolute(sobel)
    scaled = np.uint8(255*abs_sobel/np.max(abs_sobel))
    binary = np.zeros_like(scaled)
    binary[(scaled <= thresh_max) & (scaled >= thresh_min)] = 1
    return binary

def mag_thresh(img, sobel_kernel=3, mag_thresh=(0,255)):
    #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = img
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobel = np.sqrt(sobelx**2 + sobely**2)
    scaled = np.uint8(255*abs_sobel/np.max(abs_sobel))
    binary = np.zeros_like(scaled)
    binary[(scaled <= mag_thresh[1]) & (scaled >= mag_thresh[0])] = 1
    return binary

'''
Direction of the gradient is computed with arctan(sobely/sobelx)
'''
def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    direction = np.arctan2(abs_sobely, abs_sobelx)
    binary = np.zeros_like(direction)
    binary[(direction <= thresh[1]) & (direction >= thresh[0])] = 1
    return binary

def s_select_thresh(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s = hls[:,:,2]
    binary_output = np.zeros_like(s)
    binary_output[(s <= thresh[1]) & (s > thresh[0])] = 1
    return binary_output

def s_select(img):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s = hls[:,:,2]
    return s

def process_image(image):
    hls = s_select_thresh(image, (140, 255))
    s = s_select(image)
    sobelx = abs_sobel_thresh(s, 'x', 7, 140)
    dr = dir_threshold(image, 3,(0.001, 0.3))
    combined = np.zeros_like(s)
    combined[((dr == 1) & (sobelx == 1)) | (hls == 1)] = 1
    return combined