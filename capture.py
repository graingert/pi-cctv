"""pi-cctv

Usage:
  main.py -u USER -p PASSWORD -r REMOTE_HOST -o OUTPUT_PATH
  main.py --doctest
  main.py --version

Options:
  -h --help            show this help message and exit
  -u --user USER  username of the remote machine you want to copy
  -p --password PASSWORD  password of the USER on the remote machine
                          you want to copy images to
  -r --remote REMOTE_HOST  host/ip of the remote machine to copy to
  -o --output OUTPUT_PATH  dir path on the remote machine to copy images to
  --doctest            run doctest on this script
"""
import os
import time
from datetime import datetime

import picamera
from docopt import docopt

os.environ['TZ'] = 'Europe/London'
time.tzset()

dir = os.path.dirname(os.path.realpath(__file__))
save_dir = os.path.join(dir, 'images/')

if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def _get_files(dirpath):
    # Get the files in a directory sorted by date descending
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a


def _purge_files(files_dir):
    # When the number of local files reaches 100, purge half of them
    # they are no longer needed here as should be on the remote machine now
    local_files = _get_files(files_dir)
    if len(local_files) >= 100:
        for file_name in local_files[0:30]:
            file_path = os.path.join(files_dir, file_name)
            os.remove(file_path)


def capture_frame(args, count):
    now = datetime.now().strftime('%a %w %b %H:%M:%S')

    print('--- Captured image on {} ---'.format(now))

    capture_filename = '{0}.jpg'.format(now)
    file_path = os.path.join(save_dir, capture_filename)
    camera.capture(file_path)

     # Every 20 image captures run scp to the remote machine
    if count % 20 == 0:
        _purge_files(files_dir=save_dir)
        # build up the scp command
        cmd = (
            'sshpass -p "{ssh_pass}" rsync -avz '
            '{local_path}* {ssh_user}@{ssh_host}:{remote_path}'
        ).format(
            ssh_pass=args.get('--password'),
            ssh_user=args.get('--user'),
            ssh_host=args.get('--remote'),
            remote_path=args.get('--output'),
            local_path=save_dir,
        )
        print('--- uploading data ---')

        os.system(cmd)

if __name__ == '__main__':
    arguments = docopt(__doc__)

    camera = picamera.PiCamera()

    loop_count = 0
    while True:
        capture_frame(arguments, loop_count)
        loop_count += 1
        time.sleep(1)
