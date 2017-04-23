import zmq
import sys
import threading
import time
from random import randint, random
import zlib, pickle as pickle
import rospy
from std_msgs.msg import Bool
from Car import Car
import signal
RATE = 40   # Delay in msec between each message. delay of 40ms = 25 messages per second. make it higher for testing if you want

global in_intersection
global car_object
global rospy_publisher
in_intersection = False
car_object = Car(1, 1, 1, 1, 1, 1, 1, 1, 1)

def send_zipped_packet(socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    p = pickle.dumps(obj, protocol)
    z = zlib.compress(p)
    return socket.send(z, flags=flags)
class ClientTask(threading.Thread):
    global car_object
    def __init__(self):
        self.id = car_object.ID
        threading.Thread.__init__(self)

    def run(self):
        global rospy_publisher
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = u'worker-%s' % self.id
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://localhost:5570')
        print('Client %s started' % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            #print('Req #%d sent..' % (reqs))
            # socket.send_string(u'request #%d' % (reqs))
            send_zipped_packet(socket, car_object)
            for i in range(5):
                sockets = dict(poll.poll(RATE))
                if socket in sockets:
                    msg = socket.recv()
                    rospy_publisher.PUBLISH(msg)
                    #print('Client %s received: %s' % (identity, msg))

        socket.close()
        context.term()

def detect_intersection(data):
    car_object.in_intersection = data.data
    #print "got rospy data. testing!"
    rospy.loginfo(data)

if __name__ == '__main__':
    NODE_NAME = "client"
    TOPIC = "LOCATION"
    PUBLISH = "FORWARD_STEER"
    global rospy_publisher
    rospy.init_node(NODE_NAME)
    rospy.Subscriber(TOPIC, Bool, detect_intersection)
    rospy_publisher = rospy.Publisher(PUBLISH, Int32 , queue_size = 10)
    #rospy.spin()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    client1 = ClientTask()
    client1.start()

