#!/usr/bin/env python

import rospy
import sys
import turtlebot3_func as fc

fc.x = None
fc.y = None
fc.theta = None

sys.stdout.write("Provide goal.x: ")
goal_x = input()
sys.stdout.write("Provide goal.y: ")
goal_y = input()

rospy.init_node("turtlebot3_goal", anonymous=True)
fc.rate = rospy.Rate(20)
fc.goal(goal_x, goal_y)