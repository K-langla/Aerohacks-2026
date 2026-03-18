
Note: Large ata was pushed to git by accident, causing us to run git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch <data/>' --all
this affects the commit history

TASK DIVISION,
Challenge 1 - RTM CHALLENGE,
Participants: @Kelly, @deadxrk, @Taylor
 Need to review tasks and extract relevant info from Readme @deadxrk @Taylor
I did my best but this likely requires tweaking
Let me know which you think which tasks you want to work on

Task 1- Navigation Algorythm
Assigned members: Kelly, Rohan,Nicolas

Get to destination
Airspace traffic
Energy margins (Energy efficiency? Unclear),
Efficiency (time),
,
,
Task 2- Safe emergency landing
Assigned members: ?? (Do this last anyways, can assign people after task 1 more complete)
    -Designated landing site
Task 3-Figure out Simulation Environment
Assigned members: ???
    -Scoring algo
    -How to connect to sim/how it works
        -packages/libraries/programming language interaction/ necessary json files etc etc
:thumbsup:
Click to react
:heart:
Click to react
:wave:
Click to react
Add Reaction
Edit
Forward
More
[8:59 AM]Saturday, March 14, 2026 8:59 AM
Challenge 2 - Vision-Based Autonomous Hover,
Participants: @LJWANG24 , @deadxrk , @C'EST PAWAN  @Kelly , @Taylor

Task 1 - Assess the operating conditions
Assigned members:  ????? NEED VOLUNTEER

Determine criteria crucial to success using the documentation available
  for example:
the drone will automatically trigger an emergency stop if it exceeds approximately 45º in either pitch or roll
We will not let you fly if you don't have an emergency stop in place (something that calls the "emergency_stop()"
 function that can be easily and quickly be activated manually from your laptop,
Make sure criteria are met in the code
Especially to ensure we can utilise use our booked timeslots,
make sure we are compliant with the rules,
make sure we meet judging criteria,
,
,
,
Task 2 - Hover (using integrated systems)
Assigned members:   Larry, Pawan, Rohan

General onboard control systems
MPU6050,
ESP32-S2-MINI,,
Battery life/ power / existing physical constraints,
,
,
Task 3- Networking
Assigned members:  Nicholas
    -Make sure controls (especially emergency landing control) can reliably
    be sent to drone
    -Make sure feedback information can be collected from the drone

Make sure visual information can be collected efficiently enough from cameras
   to use for stabilisation -(Good to have) prevent most basic forms of malicious interferance from other teams/
  interference from other sources,
Task 4- LED detection using Computer Vision
Assigned members: Kelly, (maybe 1 more would be good, if someone wants to join)

Get camera feed from 2 cameras efficiently
Find algorythm to quickly and efficiently find LED light in video
Find algo to correct drone position using LED light position,
(Good to have) Noise removal layer (diffused light etc)


Unsorted References:

https://docs.opencv.org/4.x/d7/d00/tutorial_meanshift.html