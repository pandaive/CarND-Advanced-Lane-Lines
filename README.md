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
[image7]: ./test_images/result_with_lines.jpg "With lines"
[image8]: ./test_images/result_final.jpg "With lines"
[video1]: ./project_video.mp4 "Video"

### [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

##### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

#### Camera Calibration

##### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the file called `camera_calibration.py` in `utils` directory.  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1] ![alt text][image2]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

Here is application of distortion correction to one of the actual images of the road. This step is done in file `track_lines.py` in line #34, at the beginning of frame processing pipeline.
![alt text][image3] ![alt text][image4]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

I applied perspective transform before thresholding, not too loose too much of the upper lines part from thresholded image.
The code for my perspective transform includes a file `transform_perspective.py` in `methods` directory. I also used a separate script for generating transform matrix and reversed transform matrix, so it's not repeated in processing of every image (this file can be found in `utils` direcotry and is called `get_perspective_transform_matrix.py`).
I chose to hardcode the source and destination points in the following manner:

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

Perspective transform of processed frame is triggered in line #35 in file `track_lines.py`.
Transformed image:
![alt text][image5]


#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps methods and steps (method _process_image_) in `threshold.py` in `methods` directory). I use all the line points from thresholded *S* layer from image in HLS color space and aditionally I get points by applying sobel of x gradients on *S* layer of image in HLS color space and checking if the direction of the gradients is in specified range. All of the threshold parameters can be found in lines #52-#55 in `threshold.py` and they are mostly the result of trial-and-error method of adjusting them.
For the video frames, thresholding is applied using defined before _process_image_ method called in `track_lines.py` file in line #36. After threshold is done, I also use `warp.py` from `methods` directory to select only the region of interest of the image. The ROI points I chose can be found in lines #17-#22 of the `warp.py` file.
Color thresholding and selecting ROI of processed image is triggered in lines #36-#37 in `track_lines.py` file.
Here's an example of my output for this step.

![alt text][image6]


#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Code for finding lane lines can be found in file `find_lane_lines.py` in `methods` directory. I used the method shown in the course with window search and adjusting a second order polynomial. It's used in frame processing in line #38 in file `track_lines.py`. I save right and left line **x** values for evaluation. This is an example with drawn lines.

![alt text][image7]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I calculate the radius of curvature in file `curvature_measurement.py` in `methods` directory, following the idea given in the course. Calculation for each image is triggered in line #51 in file `track_lines.py`. The position of the car with respect to the road center is calculated in `track_lines.py` in line #52.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in file `draw_lane.py` which is used in `track_lines.py` in line #54.  It uses reversed perspective transform matrix generated before with `get_perspective_transform_matrix.py` in `utils` directory. Here is an example of my result on a test image:

![alt text][image8]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [final output video](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.
Main file in my project is `P4.py`. I run it by
```
python3 P4.py [input_filename] [output_filename] [nb_frames]
```
Where nb_frames argument states how many frames from the past will be analyzed during processing of the video. I usually used 4 frames.
Each frame of the video is going through method _process_image_ of `track_lines.py`. This class (_TrackLines_) is used through the entire processing and it handles the parameters, history of detected lines and all steps of processing of new images.
In lines #29-#32 it creates new instance of a _Lines_ class (implenented in file `lines.py` in `utils` directory) and passes historical values for left and right lanes. This class handles both lines of the single frame. It is responsible for performing sanity checks of currently detected lines and comparing them with previous lines in order to get the best fit for the current frame.
In lines #34-#38 it performs image processing and lane lines detection. When lane lines are found in #38, they are being passed to the current instance of the _Lines_ class. After evaluation in _Lines_ we get data for left and right lane and the boolean value stating if the evaluation was correct or not (it is incorrect if lane lanes weren't find or there was is no historical detections yet, so there is nothing to evaluate the results with).
Based on the evaluation, param _incorrect_frames_ is altered accordingly. Thanks to that, in case if the frame is not evaluated, I cut the last pixels (20 per incorrect frame) from the output drawing, so there is no "fake predictions" in the output video (no lanes found, no drawing on coming lane). It can be seen in the output video around 0'40s in the output video when there are couple of incorrectly processed frames in a row.
At the end, I draw the lane marking and needed data onto the frame and return it.
