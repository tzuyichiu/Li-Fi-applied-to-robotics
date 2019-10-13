#!/usr/bin/env python

import rospy
import turtlebot3_func as fc

fc.x = None
fc.y = None
fc.theta = None

rospy.init_node("turtlebot3_autonomous", anonymous=True)
fc.rate = rospy.Rate(20)
fc.left_turn(90)
fc.left_turn(90)
fc.right_turn(90)
fc.right_turn(90)
