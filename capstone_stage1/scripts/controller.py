#! /usr/bin/env python

import pygame
from pygame.locals import *
import rospy
from capstone_stage1.msg import speed_vector
"""
Stage 1 controller for senior design.
Goals to acomplish:
	-> Establish basic communication between ROScore and cars
	-> Send basic movement vectors so cars can move
	-> (optional) add support for game controllers (ps3 controller, xbox, sticks)
"""
"""
keylogging is done using pygame which is a python library for making games.
It logs active key states which makes it suitable for our cause
"""
global TOPIC
TOPIC = 'servo_controller'

global NODE_NAME
NODE_NAME = 'pc_controller'
global scale_factor
scale_factor = input("input values between 0 - 1 to scale car speed and turn rate")

def generate_vector():
	key_press = pygame.key.get_pressed()
	vector = speed_vector()
	vector.sender = NODE_NAME
	if key_press[K_w] | key_press[K_UP]:
		vector.linear = 1 * scale_factor
	if key_press[K_a] | key_press[K_LEFT]:
		vector.angular = - (90 * scale_factor)
	if key_press[K_s] | key_press[K_DOWN]:
		vector.linear = - (1 * scale_factor)
	if key_press[K_d] | key_press[K_RIGHT]:
		vector.angular = 90 * scale_factor
	if key_press[K_ESCAPE]:
		# shut down rospy
		rospy.signal_shutdown("Escape key pressed ")
	pygame.event.poll()
	return vector

def servo_controller():
	publisher = rospy.Publisher(TOPIC, speed_vector, queue_size = 10)
	rospy.init_node(NODE_NAME)
	rate = rospy.Rate(10) # broadcast at 10 times a second
	data = speed_vector()
	data.sender = NODE_NAME
	data.linear = 0
	data.angular = 0
	# The following loop sends data of the previous iteration to account for the exception when
	# user presses ESC while in the loop. The delay in data reception is negligible and can be ignored
	while not rospy.is_shutdown():
		rospy.loginfo(data)
		publisher.publish(data)
		data = generate_vector()
		rate.sleep()


if __name__ == '__main__':
	try:
		pygame.init()
		screen = pygame.display.set_mode((500,500))
		servo_controller()
	except rospy.ROSInterruptException:
		pass