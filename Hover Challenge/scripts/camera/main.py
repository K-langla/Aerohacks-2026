
'''
This is the computer vision portion of McGill Aerohacks 2026 drone challenge.
The goal was to identify the LEDs on the drones (4 LEDS, 1 white, 1 green, 1 red, and 1 blue)
and use that information to correct the drone hover, accounting for transmission delays and
low battery capacity.

Equipment provided:
    2 Logitech 'Brio 101' cameras (USB connection)
    1 ESP- 32 drone
        - 4 LEDs (1 white, 1 green, 1 red, 1 blue)
        - Wifi connection

Goal:

    -Use computer vision to:
        - Detect LED Lights with minimal noise (SUCCESS- See threshold.run_threshold)
        - Track LED lights reliably (Camshift implemented, working for face detection, but not tested on LED data)
        - Use the LED light data to counter turbulance during autonomous hover (No attempt made- Time limit reached)

Challenges:

    -Not all 4 LED's are always on.
    -The white LED contains all 3 colours.
    -No point of reference inside the box to use to augment/facilitate calculations
    -Time constraints, limited access to drone unit.
    -Drone inside cage surrounded by plastic sheets that reflect light and diffuse some of the LED light


=================
Part 1:
Isolating LED lights using Brio 101 cameras

Camera Detection: setup_cameras.py

=================
Experimenting with mean-shift based traking:
Found in run_camshift
App(video_src1, video_src2).run_camshift()

References:
Camshift tracker from https://github.com/opencv/opencv/blob/3.4/samples/python/camshift.py
================

This is a demo that shows mean-shift based tracking
You select a color objects sit tracks it.
This reads from video camera (0 by default, or the camera number the user enters)

[1] http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.14.7673

Usage:
------
    camshift.py [<video source>]

    To initialize tracking, select the object with mouse

Keys:
-----
    ESC   - exit
    b     - toggle back-projected probability visualization

Author
-----
Kelly L, 2026
'''

# Python 2/3 compatibility
from __future__ import print_function
import sys
import os
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2 as cv

# local module
import video
import threshold

from constants import DATA_DIR, GREEN_LOW_HSV,GREEN_HIGH_HSV

class Camera(object):
    def __init__(self, name, video_src):
        self.name = name
        self.cam_feed = video.create_capture(video_src, fallback=None)
        cv.namedWindow(self.name)


class App(object):
    def __init__(self, video_src1, video_src2):

        self.cam_feed1 = video.create_capture(video_src1, fallback = None)
        self.cam_feed2 = video.create_capture(video_src2, fallback = None)
        self.camera1 = 'camera1'
        self.camera2 = 'camera2'
        _ret1, self.frame1 = self.cam_feed1.read()
        _ret2, self.frame2 = self.cam_feed2.read()
        cv.namedWindow(self.camera1)
        cv.setMouseCallback(self.camera1, self.onmouse)

        cv.namedWindow(self.camera2)
        cv.setMouseCallback(self.camera2, self.onmouse)

        self.selection = None
        self.drag_start = None
        self.show_backproj = False
        self.track_window = None

    def onmouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.track_window = None
        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])
            self.selection = (xmin, ymin, xmax, ymax)
        if event == cv.EVENT_LBUTTONUP:
            self.drag_start = None
            self.track_window = (xmin, ymin, xmax - xmin, ymax - ymin)

    def show_hist(self):
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv.cvtColor(img, cv.COLOR_HSV2BGR)
        cv.imshow('hist', img)

    def run_camshift(self):
        while True:
            _ret1, self.frame1 = self.cam_feed1.read()
            cv.normalize(self.frame1, self.frame1, 0, 255, cv.NORM_MINMAX)
            _ret2, self.frame2 = self.cam_feed2.read()
            vis1 = self.frame1.copy()
            if (self.frame2 is None):
                print("")
            vis2 = self.frame2.copy()
            hsv1 = cv.cvtColor(self.frame1, cv.COLOR_BGR2HSV)
            # https://stackoverflow.com/questions/61016954/controlling-contrast-and-brightness-of-video-stream-in-opencv-and-python
            contrast = 50
            brightness = 0
            hsv1[:, :, 2] = np.clip(contrast * hsv1[:, :, 2] + brightness, 0, 255)
            #hsv1 = cv.cvtColor(hsv1, cv.COLOR_HSV2BGR)

            hsv2 = cv.cvtColor(self.frame2, cv.COLOR_BGR2HSV)
            mask1 = cv.inRange(hsv1, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
            mask2 = cv.inRange(hsv2, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

            if self.selection:
                x0, y0, x1, y1 = self.selection
                hsv_roi = hsv1[y0:y1, x0:x1]
                mask_roi = mask1[y0:y1, x0:x1]
                hist = cv.calcHist([hsv_roi], [0], mask_roi, [16], [0, 180])
                cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)
                self.hist = hist.reshape(-1)
                self.show_hist()

                vis_roi = vis1[y0:y1, x0:x1]
                cv.bitwise_not(vis_roi, vis_roi)
                vis1[mask1 == 0] = 0

            if self.track_window and self.track_window[2] > 0 and self.track_window[3] > 0:
                self.selection = None
                prob = cv.calcBackProject([hsv1], [0], self.hist, [0, 180], 1)
                prob &= mask1
                term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
                track_box, self.track_window = cv.CamShift(prob, self.track_window, term_crit)

                if self.show_backproj:
                    vis1[:] = prob[..., np.newaxis]
                try:
                    cv.ellipse(vis1, track_box, (0, 0, 255), 2)
                except:
                    print(track_box)

            cv.imshow(self.camera1, vis1)
            cv.imshow(self.camera2, vis2)

            ch = cv.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv.destroyAllWindows()
    def run_optical_flow(self):
        #parser = argparse.ArgumentParser(description='This sample demonstrates Lucas-Kanade Optical Flow calculation. \
                                                      #The example file can be downloaded from: \
                                                      #https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
        #parser.add_argument('image', type=str, help='path to image file')
        #args = parser.parse_args()

        #cap = cv.VideoCapture(args.image)

        # params for ShiTomasi corner detection
        feature_params = dict(maxCorners=100,
                              qualityLevel=0.3,
                              minDistance=7,
                              blockSize=7)

        # Parameters for lucas kanade optical flow
        lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

        # Create some random colors
        color = np.random.randint(0, 255, (100, 3))

        # Take first frame and find corners in it
        ret, old_frame1 = self.cam_feed1.read()
        old_gray = cv.cvtColor(old_frame1, cv.COLOR_BGR2GRAY)
        p0 = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

        # Create a mask image for drawing purposes
        mask = np.zeros_like(old_frame1)

        while (1):
            ret, frame1 = self.cam_feed1.read()
            if not ret:
                print('No frames grabbed!')
                break

            frame_gray = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)

            # calculate optical flow
            p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

            # Select good points
            if p1 is not None:
                good_new = p1[st == 1]
                good_old = p0[st == 1]

            # draw the tracks
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
                frame1 = cv.circle(frame1, (int(a), int(b)), 5, color[i].tolist(), -1)
            img = cv.add(frame1, mask)

            cv.imshow('frame', img)
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break

            # Now update the previous frame and previous points
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)

        cv.destroyAllWindows()



if __name__ == '__main__':
    print(__doc__)
    import sys
    cameras = video.get_available_cameras()
    #Test print
    #print(cameras)

    vid_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+ DATA_DIR
    # Test print
    #print( "video dir: " +vid_path)

    #vid_1 = "drone video long.mp4"
    #vid_2 = "drone video short.mp4"
    vid_1 = "drone cam 1.mp4"
    vid_2 = "drone cam 2.mp4"

    small_clip1 = "Small clip 1.mp4"
    blue_LED_clip = "Blue LED clips.mp4"


    #Caution : No error checking for video src - will fail if no cameras detected

    try:
        video_src1 = sys.argv[1] #can pass sys.argv, i dont but i left as is
    except:
        #video_src1 = cameras[0] #Uncomment to use live video feed from a Brio Webcam
        #video_src1 = vid_path + vid_1 #Uncomment to use video of the drone for testing
        #video_src1 = vid_path + small_clip1 #uncomment for short video with 3/4 leds
        video_src1 = vid_path + blue_LED_clip #uncomment for short video with blue LED
    try:
        video_src2 = sys.argv[2] #can pass sys.argv, i dont but i left as is
    except:

        #video_src2 = cameras[1] #Uncomment to use live video feed from a second Brio Webcam
        video_src2 = vid_path + vid_2 #Uncomment to use video of the drone for testing


    #App(video_src1, video_src2).run_camshift() #Uncomment for Camshift tracking

    #threshold.run_threshold_tester(video_src1) #Uncomment to test HSV levels on video




    #Uncomment these to see filter on video
    #threshold.run_threshold(video_src1, "red", RED_LOW_HSV,RED_HIGH_HSV)
    #threshold.run_threshold(video_src1,"blue", BLUE_LOW_HSV,BLUE_HIGH_HSV)
    threshold.run_threshold(video_src1, "green", GREEN_LOW_HSV, GREEN_HIGH_HSV)



