#! /usr/bin/env python

import rospy
from capstone_stage1.msg import speed_vector

#Define Unique car name:
global NAME
NAME = 'cream_cheese_and_ketchup'

global TOPIC
TOPIC = 'servo_controller'
"""
Subscriber/listener node for Capstone Stage 1
Goals to acomplish:
	-> listen to published messages
	-> drive servos
	-> log in rospy

receive data as speed_vector(linear,angular) msg
"""

def log_data(data):
	rospy.loginfo("Received linear: %0.3f, angular: %0.3f from %s" % (data.linear, data.angular, data.sender))
def drive_servo(data):
	# servo driving code goes here #
	# you get vector in the form of {linear, angular}
	# use them as data.linear and data.angular

	# I figured logging the data would be wise so i'm adding a logger. remove it later if you want
	log_data(data)

def servo_listener():
	rospy.init_node(NAME) # do not define anonymous = True as we want to assign custom names
	rospy.Subscriber(TOPIC, speed_vector, drive_servo)
	rospy.spin()

if __name__ == '__main__':
	servo_listener()