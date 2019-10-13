#!/usr/bin/env python

import sys
import rospy
import turtlebot3_func as fc

fc.x = None
fc.y = None
fc.theta = None

rospy.init_node("turtlebot3_strait", anonymous=True)
fc.rate = rospy.Rate(20)
sys.stdout.write("Distance (may be negatif): ")
dis = float(input())
print "Distance: %.3f" % dis

if dis > 0:
	fc.go_forward(dis)
else:
	fc.go_back(-dis)