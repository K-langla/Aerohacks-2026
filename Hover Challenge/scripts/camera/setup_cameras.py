
'''
Helper function to detect connected webcams, and filter to just the 2 Brio 101 cameras.
-----

author: Kelly

'''
from pygrabber.dshow_graph import FilterGraph

from constants import CAMERA_NAME, DEFAULT_CAMERA

def get_available_cameras() :

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


