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