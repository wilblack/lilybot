import os
import time
import picamera
from datetime import datetime as dt

out_dir = "/home/pi/growbot/"
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.start_preview()
    # camera.exposure_compensation = 2
    # camera.exposure_mode = 'spotlight'
    # camera.meter_mode = 'matrix'
    # camera.image_effect = 'gpen'
    # Give the camera some time to adjust to conditions
    time.sleep(2)
    fname = "image_%s.jpg" %(dt.strftime(dt.now(), "%Y-%m-%dT%H:%M:%SZ"))
    print "Creating image %s in %s" %(fname, out_dir)
    camera.capture(os.path.join(out_dir, fname))
    camera.stop_preview()


"""
*/1 * * * * python /home/pi/projects/lilybot/rpi_client/bot_roles/camera.py > /home/pi/cron.log 2>&1
"""