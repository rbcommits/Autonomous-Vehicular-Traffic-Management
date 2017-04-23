import rospy
import smbus
from std_msgs.msg import Int32

NODE_NAME = "Driver"
turn_offset_topic = "CAMERA"
forward_steer_topic = "FORWARD_STEER"

global forward_steer
global turn_offset
forward_steer = 0
turn_offset = 0
def update_turn_offset(offset):
	global turn_offset
	turn_offset = offset
	rospy.loginfo("updated offset: %d", % (turn_offset));

def update_steer(steer):
	global forward_steer
	forward_steer = steer
	rospy.loginfo("updated velocity: %d", % (forward_steer));

if __name__ == '__main__':
	global forward_steer, turn_offset
	rospy.init_node(NODE_NAME)
	rospy.Subscribe(turn_offset_topic, Int32, update_turn_offset)
	rospy.Subscribe(forward_steer_topic, Int32, update_steer)

	i2c = smbus.SMBus(1)
	DEVICE_ADDRESS = 0x0a
	while True:
		i2c.write_byte(DEVICE_ADDRESS, 99)
		# vCom setting forward drive (0-255)
		i2c.write_byte(DEVICE_ADDRESS, 200 + forward_steer)
		# sCom setting steering (127 (standby), 126-0(max) left, 128-255(max) right)
		i2c.write_byte(DEVICE_ADDRESS, 127 + turn_offset)
		pass