import cv2
import numpy as np
import pickle

image = cv2.imread('../test_images/test1.jpg')
imshape = image.shape
a = (276,imshape[0]-50)
b = ((imshape[1]/2)-47, 450)
c = ((imshape[1]/2)+55, 450)
d = (imshape[1]-240,imshape[0]-50)
src = np.array([[a, b, c, d]], dtype=np.float32)
offsetx = 400
offsety = 0
dst = np.float32([[offsetx,imshape[0]-offsety], 
                    [offsetx,offsety], 
                    [imshape[1]-offsetx, offsety], 
                    [imshape[1]-offsetx, imshape[0]-offsety]])

M = cv2.getPerspectiveTransform(src, dst)
Minv = cv2.getPerspectiveTransform(dst, src))

pickle.dump(M, open("params/perspectiveTransformMatrix.p", "wb"))
pickle.dump(Minv, open("params/oppositePerspectiveTransformMatrix.p", "wb"))
print("Perspective transform matrix saved")