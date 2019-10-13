#!/usr/bin/env python

import rospy
import sys
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from math import atan2, sqrt, pi

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

err = """
Communications Failed or Error Compilation
"""

def newOdom(msg):
    global x, y, theta
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    theta = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])[2]

def shut_down():
    print("\n####################End of execution####################\n")
    twist = Twist()
    twist.linear.x = 0.0
    twist.angular.z = 0.0
    pub.publish(twist)

def print_info(pos_x, pos_y, theta, inc_theta):
    if pos_x is None or pos_y is None or theta is None:
        print "Suscribing..."
    print "Pos: (%.3f, %.3f)\tAng: %3.1f\tTurn: %3.1f" % (pos_x, pos_y, theta*180/pi, inc_theta*180/pi)

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input
    return input

def checkLinearLimitVelocity(vel):
    vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    return vel

def checkAngularLimitVelocity(vel):
    vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    return vel

def betweenMinusPiAndPi(theta):
    res = divmod(theta, 2*pi)[1]
    if res > pi:
        res -= 2*pi
    return res

def dist_eucli(pos_x, pos_y, pos_x0, pos_y0):
    inc_x = pos_x - pos_x0
    inc_y = pos_y - pos_y0
    return sqrt(inc_x*inc_x+inc_y*inc_y)

def start_suscribe():
    global x, y, theta
    if x is None:
        return False
    if y is None:
        return False
    if theta is None:
        return False
    return True

def goal(goal_x, goal_y):
    global x, y, theta
    goal = Point()
    goal.x = goal_x
    goal.y = goal_y

    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0

    while not start_suscribe():
        pub.publish(twist)

    while not rospy.is_shutdown():
        inc_x = goal.x - x
        inc_y = goal.y - y
        inc_theta = betweenMinusPiAndPi(atan2(inc_y, inc_x) - theta)

        if abs(inc_x) < 0.01 and abs(inc_y) < 0.01:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            pub.publish(twist)
            print_info(x, y, theta, inc_theta)
            return

        print_info(x, y, theta, inc_theta)

        if abs(inc_theta) > 0.1:
            twist.linear.x = 0.0
            if inc_theta < 0:
                twist.angular.z = -ANG_VEL
            else:
                twist.angular.z = ANG_VEL
        else:
            twist.linear.x = LIN_VEL
            twist.angular.z = 0.0

        pub.publish(twist)
        rate.sleep()

# angle has to be included between -180 and 180 (avoid -180)
def turn(ang):
    global x, y, theta
    
    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
    
    while not start_suscribe():
        pub.publish(twist)

    theta0 = theta
    ang_rad = betweenMinusPiAndPi(ang*pi/180)

    if ang_rad > 0:
        twist.angular.z = -ANG_VEL
    else:
        twist.angular.z = ANG_VEL
    pub.publish(twist)

    while not rospy.is_shutdown():
        inc_theta = betweenMinusPiAndPi(theta + ang_rad - theta0)
        if abs(inc_theta) < 0.03:
            twist.angular.z = 0.0
            pub.publish(twist)
            print_info(x, y, theta, inc_theta)
            return
        print_info(x, y, theta, inc_theta)
        pub.publish(twist)
        rate.sleep()

def left_turn(ang):
    print "\n####################Turning left####################"
    print "Turn: %3.1f deg\n" % ang
    turn(ang)

def right_turn(ang):
    print "\n####################Turning right####################"
    print "Turn: %3.1f deg\n" % ang
    turn(-ang)

def strait(dis):
    global x, y, theta
    
    print "dis: %.3f\n" % dis

    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
    
    while not start_suscribe():
        pub.publish(twist)

    x0 = x
    y0 = y
    theta0 = theta

    if dis > 0:
        twist.linear.x = LIN_VEL
    else:
        twist.linear.x = -LIN_VEL

    while not rospy.is_shutdown():
        d = dist_eucli(x, y, x0, y0)
        if dis < 0:
            d = -d
        inc_d = dis - d
        inc_theta = theta - theta0
        if abs(inc_d) < 0.03:
            twist.linear.x = 0.0
            pub.publish(twist)
            print_info(x, y, theta, inc_theta)
            return
        print_info(x, y, theta, inc_theta)
        pub.publish(twist)
        rate.sleep()

def go_forward(dis):
    print "\n####################Going forward####################"
    strait(dis)

def go_back(dis):
    print "\n####################Going back####################"
    strait(-dis)

LIN_VEL = checkLinearLimitVelocity(0.2)
ANG_VEL = checkAngularLimitVelocity(0.5)

x = None
y = None
theta = None

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

rospy.on_shutdown(shut_down)

if __name__ == "__main__":
    rospy.init_node("turtlebot3_move", anonymous=True)
    rate = rospy.Rate(20)
    for _ in range(4):
        go_forward(0.5)
        right_turn(90)
