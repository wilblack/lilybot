import subprocess
from uuid import getnode as get_mac

def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def shutdown():
  command = "/usr/bin/sudo /sbin/shutdown -h now"
  process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  output = process.communicate()[0]
  print output

def get_mac_address():
    mac = get_mac()
    return "%012X"%mac


def hex2rgb(hex):
    return [ord(c) for c in hex[1:].decode("hex")]

def rgb2hex(rgb):
  """
  Inputs:
  rgb - A tuple or list of length 3 with each item an iteger between
        0 and 255.

  """
  return "#%02X%02X%02X" % rgb