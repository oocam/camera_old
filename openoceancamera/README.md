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

# Live Stream feature

The intuition behind building Live Video Stream feature is to help client fine-tune the OOCAM camera focus.

On the server side, you can find the live stream main code inside `openoceancamera/main.py`. 

### get_video()
When there is a post request coming from the client, it will read and save the `stream_duration` value in a global variable. It'll be use to determine how long the livestream last. On the other hand, When there is a get request coming, it will give response and initiate the Live Video Stream feature.

```python
@app.route("/stream", methods=["GET", "POST"])
def get_video():
    global stream_duration
    if request.method == "GET":
        return Response(gen(Camera_Pi(stream_duration)),mimetype='multipart/x-mixed-replace; boundary=frame' )
    if request.method == "POST":
        time_duration = request.get_json()["time_duration"]
        stream_duration = int(time_duration)
        return "OK"
```
