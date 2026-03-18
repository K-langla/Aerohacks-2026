'''
Meanshift tracking on video - also known as mode-seeking.

====
What is meanshift?

Unsupervised learning algorithm.
Mode : Highest density of data points in the region.

Non-parametric, density-based clustering algorithm.
Iteratively shifts data towards the mode until convergence at local maximum of density function.
Used for Datasets that have arbitrary shapes + not well seperated by linear boundaries
Unlike K-means, does not require specific number of clusters in advance,
number of clusters is determined by the algorithm based on the data.

The process of mean-shift clustering algorithm can be summarized as follows:

Initialize the data points as cluster centroids.
Repeat the following steps until convergence or a maximum number of iterations is reached:
For each data point, calculate the mean of all points within a certain radius (i.e., the "kernel") centered at the data point.
Shift the data point to the mean.
Identify the cluster centroids as the points that have not moved after convergence.
Return the final cluster centroids and the assignments of data points to clusters.

Suitability
----------
Mean shift is expensive - O(n^2).In our case, the number of clusters is known (there are 4 LED lights to be tracked.)
This could lead to false positives (though it is robust to outliers)
 Unsure if it is a suitable algo for the task.
Needs to be tested against other alternatives.


Based on code found at:
https://docs.opencv.org/4.x/d7/d00/tutorial_meanshift.html
https://github.com/opencv/opencv/blob/4.x/samples/cpp/tutorial_code/video/meanshift/meanshift.cpp
https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4
'''

import numpy as np
import cv2 as cv
import argparse

parser = argparse.ArgumentParser(description='This sample demonstrates the meanshift algorithm. \
                                              The example file can be downloaded from: \
                                              https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
parser.add_argument('image', type=str, help='path to image file')
args = parser.parse_args()

cap = cv.VideoCapture(args.image)

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
x, y, w, h = 300, 200, 100, 50 # simply hardcoded the values
track_window = (x, y, w, h)

# set up the ROI for tracking
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret, frame = cap.read()

    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv.imshow('img2',img2)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break