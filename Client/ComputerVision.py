import cv2
import rospy
#import LaneDetection
import Localizer
from std_msgs.msg import Int32, Bool

# rospy globals
global camera_topic
global location_topic
global NODE_NAME
#global camera_publisher
#global location_publisher

NODE_NAME = "ComputerVision"
camera_topic = "CAMERA"

location_topic ="LOCATION"

def InitRospy():
	global camera_topic, location_topic
	camera_publisher = rospy.Publisher(camera_topic, Int32 , queue_size = 10)
	location_publisher = rospy.Publisher(location_topic, Bool, queue_size = 10)
	rospy.init_node(NODE_NAME)
	rate = rospy.Rate(10) # 10/second
	return camera_publisher, location_publisher, rate

def Sense():
	cap = cv2.VideoCapture(-1)
	turn_offset = 1#LaneDetection.detectLane(cap)
	in_intersection = Localizer.detect(cap)
	return turn_offset, in_intersection

if __name__ == "__main__":
	camera_publisher, location_publisher, rate = InitRospy()
	while not rospy.is_shutdown():
		turn_offset, in_intersection = Sense()
		# use rospy.loginfo(data) to log all the data being sent
		#camera_publisher.publish(turn_offset)
		location_publisher.publish(in_intersection)
		rospy.loginfo(in_intersection)
		rate.sleep()
		pass
