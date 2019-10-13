#!/usr/bin/env python

import rospy
import turtlebot3_func as fc

fc.x = None
fc.y = None
fc.theta = None

rospy.init_node("turtlebot3_turn", anonymous=True)
fc.rate = rospy.Rate(20)
sys.stdout.write("Angle (between -179 and 180): ")
ang = float(input())

if ang > 0:
	fc.left_turn(ang)
else:
	fc.right_turn(-ang)