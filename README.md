pi-cctv
=======

![raspberry-pi-with-camera-module](https://i.imgur.com/zbGtq9j.jpg)

pi-cctv is a script for use with your raspberry pi and raspberry pi camera module.
When ran it will continually take image captures with the camera module (placing them in an 'images' folder), and will rsync the image captures to a remove machine incase the raspberry pi gets stolen.


### Installation

    git clone https://github.com/richardasaurus/pi-cctv.git
    cd ./pi-cctv
    pip install -r requirements.txt

### Example Usage

    python capture.py --user=myusername --password=mypassword --remote=192.168.0.14 --output=/home/hilaryclinton/Desktop/my_spy_images

Help information

    Usage:
      main.py -u USER -p PASSWORD -r REMOTE_HOST -o OUTPUT_PATH
      main.py --doctest
      main.py --version

    Options:
      -h --help            show this help message and exit
      -u --user USER  username of the remote machine you want to rsync
      -p --password PASSWORD  password of the USER on the remote machine
                              you want to ssh images to
      -r --remote REMOTE_HOST  host/ip of the remote machine to rsync to
      -o --output OUTPUT_PATH  dir path on the remote machine to rsync images to
      --doctest            run doctest on this script



