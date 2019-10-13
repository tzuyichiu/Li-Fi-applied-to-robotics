#!/bin/sh

MASTER=$(echo $ROS_MASTER_URI | cut -c 8- | cut -d':' -f 1)
HOSTNAME=$(hostname -I | awk '{print $1}')

ros_setup="export ROS_MASTER_URI=http://${MASTER}:11311; export ROS_HOSTNAME=${HOSTNAME}; source /opt/ros/kinetic/setup.bash; source ~/catkin_ws/devel/setup.bash"
killall python
killall roscore

lxterminal --command="/bin/bash -c '${ros_setup}; roslaunch turtlebot3_bringup turtlebot3_core.launch'"
