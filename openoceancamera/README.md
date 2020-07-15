# OpenOceanCamera

#### Camera interface for the onboard Raspberry Pi

The on-board Raspberry Pi uses the interface to control the camera and storage for the recordings.

##### Main features
* Set record schedule to follow (Allows setting camera parameters for each time slot in the schedule).
* Connect to an external device via Wi-Fi to configure scheduler

#### Project dependencies
* Python 3
* Raspberry Pi
* Raspberry Pi camera module

#### Runbook

1. Clone the git repository in the Raspberry Pi   
`https://github.com/shark-trek/openoceancamera.git`

2. Go to the project folder and install dependencies   
`cd openoceancamera/`   
`pip3 install -r requirements.txt`

3. Run the application   
`python3 main.py <external_drive_name>`   
