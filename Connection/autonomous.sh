#!/bin/sh

ros_setup="export ROS_MASTER_URI=http://localhost:11311; export ROS_HOSTNAME=localhost; source /opt/ros/kinetic/setup.bash; source ~/catkin_ws/devel/setup.bash"

lxterminal --command="/bin/bash -c '${ros_setup}; killall roslaunch; roscore'"
sleep 15
lxterminal --command="/bin/bash -c '${ros_setup}; roslaunch turtlebot3_bringup turtlebot3_core.launch'"
sleep 20
lxterminal --command="/bin/bash -c '${ros_setup}; rosrun turtlebot3_automation turtlebot3_autonomous.py'"
