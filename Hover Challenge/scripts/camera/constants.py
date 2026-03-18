'''
Parameters for the challenge to avoid hardcoded values (in case something needs to be swapped quickly)

author
-----
Kelly Langlais, 2026
'''

#Brand used in this challenge - how it shows up was determined using pygrabber.dshow_graph import FilterGraph.get_input_devices() in setup_cameras
CAMERA_NAME = "brio"
DEFAULT_CAMERA = 0 # device index 0 - webcam if no other cameras, will return error if no webcam

PROJECT_DIR = "McGill Aerohacks\\"
DATA_DIR = "\\data\\"

RED_HUE = 0
GREEN_HUE = 120
BLUE_HUE = 240

#Filters for LEDs determined through trial and error
#Good starting point, but ideally putting it through ML to fine tune these values would be the next step
# Some test values for HSV,
# red_low_hsv =(0, 148, 135)
# red_high_hsv = (10, 255, 255)
# low_H:100, low_S:54, low_V :0
# high_H:140, high_S:255, high_V:255
# green_low_hsv =(100, 54, 0)
# green_high_hsv = (140, 255, 255)
# blue_low_hsv =(140, 64, 0)
# blue_high_hsv = (174, 255, 255)
RED_LOW_HSV = (0, 148, 135)
RED_HIGH_HSV = (10, 255, 255)
BLUE_LOW_HSV  = (100, 54, 0) #not tuned
BLUE_HIGH_HSV = (140, 255, 255)#not tuned
GREEN_LOW_HSV  = (50, 66, 130)
GREEN_HIGH_HSV = (75 , 255, 255)


