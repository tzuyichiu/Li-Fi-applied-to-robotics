#!/bin/sh

if [ "$#" -lt 1 ] ; then
  echo "Please indicate Master's IP."
  exit 0
elif [ "$#" -gt 1 ] ; then
  echo "Too many arguments: Please only indicate Master's IP."
  exit 1
fi

MASTER=$1
ros_setup="source /opt/ros/kinetic/setup.bash; source ~/catkin_ws/devel/setup.bash"
echo "Testing connection with ${MASTER}..."

while [ true ]; do
  sleep 1
  ping -c1 $MASTER > /dev/null 2>&1

  if [ $? != 0 ]
  then
    echo "Lost connection!"
    lxterminal --command="/bin/bash -c '${ros_setup}; rosrun turtlebot3_automation turtlebot3_autonomous.py'"

    while [ true ]; do
      sleep 1
      ping -c1 $MASTER > /dev/null 2>&1
      if [ $? -eq 0 ]
      then
	echo "Reconnected to ${MASTER}!"
	killall python
        lxterminal --command="/bin/bash -c '${ros_setup}; roslaunch turtlebot3_bringup turtlebot3_core.launch'"
	break
      fi
    done
  fi
done
