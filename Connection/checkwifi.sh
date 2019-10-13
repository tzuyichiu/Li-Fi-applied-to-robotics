#!/bin/sh

MASTER=$(echo $ROS_MASTER_URI | cut -c 8- | cut -d':' -f 1)

while [ true ]; do
  sleep 1
  ping -c1 $MASTER > /dev/null 2>&1

  if [ $? != 0 ]
  then
    rosrun turtlebot3_automation autonomous.sh
    while [ true ]; do
      sleep 1
      ping -c1 $MASTER > /dev/null 2>&1
      if [ $? -eq 0 ]
      then
        rosrun turtlebot3_automation connectagain.sh
        break
      fi
    done
  fi
done
