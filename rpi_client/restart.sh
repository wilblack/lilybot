#!/bin/bash

# Checks the status of ardyh_cleintd and restarts if dead.

status=$(/etc/init.d/ardyh_clientd status)
echo $status

size=${#status}
echo $size

# out=$( status | sed -e 's/^.*\(Process dead\).*$/\1/')
# echo $out

if [ $size == 81 ]; then
  echo 'Trying to restart...'
  /etc/init.d/ardyh_clientd start
fi
