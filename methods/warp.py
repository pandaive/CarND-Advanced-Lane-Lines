import numpy as np
import cv2

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)   
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def process(image):
    imshape = image.shape
    a = (350,imshape[0])
    b = (350, 600)
    c = (100,0)
    d = (imshape[1],0)
    e = (1010, 600)
    f = (1010, imshape[0])
    roi_points = np.array([[a, b, c, d, e, f]], dtype=np.int32)
    selected_final = region_of_interest(image, roi_points)

    return selected_final