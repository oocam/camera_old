# Open Ocean Camera

This is the code for Open Ocean Camera hardware. This repository includes the scripts required for setting up the Raspberry Pi as well as the essential code-base required for operation of the camera and the communication with the mobile application.

## Development Setup

### First time setup

#### Update system packages

Make sure that all `apt` packages are already up-to-date

```bash
sudo apt update
sudo apt upgrade
```

#### Mounting the USB storage device on boot

The OOCAM uses external storage device connected via USB in order to function. However, to mount ExFAT filesystems it requires additional packages to be installed.

To install the required packages, use:

```bash
sudo apt-get install exfat-fuse
sudo apt-get install exfat-utils
```

Now, if the mount point `/media/pi/OPENOCEANCA` does not already exist, create it:

```bash
sudo mkdir /media/pi
```

To enable mounting the USB during boot, edit the file `/etc/fstab`:

```bash
sudo vim /etc/fstab
```

Add the mount point configuration in a new line:

```
LABEL=OOCAM   /media/pi/OPENOCEANCA   exfat   defaults,nofail   0   0
```

The `nofail` option is essential so that the boot does not fail if the usb device is not connnected, or fails to mount.

#### Install WittyPi

WittyPi installation scripts allows the system to load the deamon for graceful startups and shutdowns.

Run the installation by using:

```bash
wget http://www.uugear.com/repo/WittyPi3/install.sh
chmod +x ./install.sh
./install.sh
```

You might need root (using `sudo`) to run the commands above.

Reboot the RaspberryPi for the deamon to load.

#### Running the program on boot

To run the scripts on boot, add it to crontab using

```bash
crontab -e
```

Add the line to run a bash script on boot:

```
@reboot /home/pi/run.sh
```

The `run.sh` script executes the Python scripts as a background process.
