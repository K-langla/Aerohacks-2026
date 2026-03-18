#!/usr/bin/env python
'''

Class that deals with video capture

Keys:
    ESC    - exit
    SPACE  - save current frame to <shot path> directory

Based on code from:
https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
'''


# Python 2/3 compatibility
from __future__ import print_function
from pygrabber.dshow_graph import FilterGraph


import numpy as np
import cv2 as cv

import re


# local
from constants import CAMERA_NAME, DEFAULT_CAMERA



def create_capture(source = 0, fallback = None):

    '''source: <int> or '<int>|<filename>|synth [:<param_name>=<value> [:...]]'
    '''
    source = str(source).strip()

    # Win32: handle drive letter ('c:', ...)
    source = re.sub(r'(^|=)([a-zA-Z]):([/\\a-zA-Z0-9])', r'\1?disk\2?\3', source)
    chunks = source.split(':')
    chunks = [re.sub(r'\?disk([a-zA-Z])\?', r'\1:', s) for s in chunks]

    source = chunks[0]
    try: source = int(source)
    except ValueError: pass
    params = dict( s.split('=') for s in chunks[1:] )

    cap = cv.VideoCapture(source)
    if 'size' in params:
        w, h = map(int, params['size'].split('x'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, h)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', source)
        if fallback is not None:
            return create_capture(fallback, None)
    print('SUCCESS : opened video source: ', source)
    return cap

def get_available_cameras() :
    '''
    Helper function to detect connected webcams, and filter to just the 2 Brio 101 cameras.
    -----

    author: Kelly

    '''
    devices = FilterGraph().get_input_devices()
    #{0: 'Brio 101', 1: 'USB2.0 VGA UVC WebCam', 2: 'Brio 101'} just need the brios
    available_cameras = {}
    indexes = []

    camera_name = CAMERA_NAME #Brio

    for device_index, device_name in enumerate(devices):
        available_cameras[device_index] = device_name

    if(len(available_cameras) == 0): #no cameras found
        print("No cameras detected")
        return indexes

    print("Cameras found: ")
    print(available_cameras)

    for index, device_name in enumerate(devices):
        if camera_name in device_name.lower():
            indexes.append(index)
    print("Using camera indexes: ")
    print(indexes)
    return indexes


'''
if __name__ == '__main__':
    import sys
    import getopt

    print(__doc__)

    args, sources = getopt.getopt(sys.argv[1:], '', 'shotdir=')
    args = dict(args)
    shotdir = args.get('--shotdir', '.')
    if len(sources) == 0:
        sources = [ 0 ]

    caps = list(map(create_capture, sources))
    shot_idx = 0
    while True:
        imgs = []
        for i, cap in enumerate(caps):
            ret, img = cap.read()
            imgs.append(img)
            cv.imshow('capture %d' % i, img)
        ch = cv.waitKey(1)
        if ch == 27:
            break
        if ch == ord(' '):
            for i, img in enumerate(imgs):
                fn = '%s/shot_%d_%03d.bmp' % (shotdir, i, shot_idx)
                cv.imwrite(fn, img)
                print(fn, 'saved')
            shot_idx += 1
    cv.destroyAllWindows()
'''