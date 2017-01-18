#! /usr/bin/env python

"""
Things to do:
    -> Accept camera feed. Use OpenCV for this
    -> Convert camera feed to a string, time stamp it
    -> Publish it to the necessary topic
"""
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image   # Might wanna switch to CompressedImage later
from cv_bridge import CvBridge

TOPIC = "ImageProcessing"
NAME = "Camera"
FEED = "video.mpg" #Camera feed goes here. Use dummy video to test
rospy.init_node(NAME)
publisher = rospy.Publisher(TOPIC, Image, queue_size=10)
camera = cv2.VideoCapture(FEED)

while camera.isOpened():
    meta, frame = camera.read()
    msg_frame = CvBridge.cv2_to_imgmsg(frame)
    publisher.publish(msg_frame)
