import os
import time
import picamera
from datetime import datetime as dt

out_dir = "/home/pi/projects/lilybot/images/growbot"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.rotation = 180
    camera.start_preview()
    # camera.exposure_compensation = 2
    # camera.exposure_mode = 'spotlight'
    # camera.meter_mode = 'matrix'
    # camera.image_effect = 'gpen'
    # Give the camera some time to adjust to conditions
    time.sleep(2)
    fname = "image_%s.jpg" %(dt.strftime(dt.now(), "%Y-%m-%dT%H-%M-%SZ"))
    print "Creating image %s in %s" %(fname, out_dir)
    camera.capture(os.path.join(out_dir, fname))
    camera.stop_preview()

    os.system("su pi -c 'rsync -avz /home/pi/projects/lilybot/images/growbot/ wilblack@ardyh.solalla.com:/home/wilblack/projects/lilybot/web_client/growbot'")

"""
12 */2 * * * python /home/pi/projects/lilybot/rpi_client/bot_roles/camera.py > /home/pi/cron.log 2>&1

rsync -avz /home/pi/projects/lilybot/images/growbot/ wilblack@192.168.0.106:/Users/wilblack/Desktop/growbot/
rsync -avz /home/pi/projects/lilybot/images/growbot/ wilblack@ardyh.solalla.com:/home/wilblack/projects/lilybot/web_client/growbot


Possible way to send an image

with open("some_image.png", "rb") as imageFile:
    self.str = base64.b64encode(imageFile.read())

"""

