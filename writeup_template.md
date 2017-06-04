## Project Writeup

---
**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./camera_cal/calibration2.jpg "Distorted"
[image2]: ./camera_cal/result.jpg "Undistorted"
[image3]: ./test_images/straight_lines1.jpg "Distorted"
[image4]: ./test_images/result.jpg "Undistorted"
[image5]: ./test_images/result_transformed.jpg "Transformed"
[image6]: ./test_images/result_thresholded.jpg "Thresholded and warped"
[video1]: ./project_video.mp4 "Video"

### [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

##### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

#### Camera Calibration

##### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the file called `camera_calibration.py` in _utils_ directory.  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1] ![alt text][image2]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

Here is application of distortion correction to one of the actual images of the road. This step is done in file `track_lines.py` in line #34, at the beginning of frame processing pipeline.
![alt text][image3] ![alt text][image4]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

I applied perspective transform before thresholding, not too loose too much of the upper lines part from thresholded image.
The code for my perspective transform includes a file `transform_perspective.py` and a file `warp.py` both in _methods_ directory. I also used a separate script for generating transform matrix and reversed transform matrix, so it's not repeated in processing of every image (this file can be found in _utils_ direcotry and is called `get_perspective_transform_matrix.py`).
I chose the hardcode the source and destination points in the following manner:

```python
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
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 276, 670      | 400, 720        | 
| 593, 450      | 400, 0      |
| 695, 450     | 880, 0      |
| 1020, 670      | 880, 720        |

Transformed image:
![alt text][image4]


#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps methods and steps (method _process_image_) in `threshold.py` in _methods_ directory). I use all the line points from thresholded *S* layer from image in HLS color space and aditionally I get points by applying sobel of x gradients on *S* layer of image in HLS color space and checking if the direction of the gradients is in specified range. All of the threshold parameters can be found in lines #52-#55 and they are mostly the result of trial-and-error method of adjusting them.
For the video frames, thresholding is applied using defined before _process_image_ method called in `track_lines.py` file in line #36
Here's an example of my output for this step.


![alt text][image3]


#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
