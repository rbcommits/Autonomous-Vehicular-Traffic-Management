import zmq
import sys
import threading
import time
from random import randint, random
import zlib, cPickle as pickle
#Launch Multiple car clients to test the server
"""
 This client code will be loaded on to the cars. Each car will be a single client connected to the server.
 For the purposes of testing the server, I went ahead and created 2 car objects in the same file.
 Feel free to modify and add more car clients as you test the robustness of your algorithm
"""

"""
 Most of the code here is communication related and you probably don't need to understand it to work on the server but I will try and 
 comment it as much as possible
"""


# creates a basic car object to hold the car data.
# nothing fancy here

RATE = 40 # Delay in msec between each message. delay of 40ms = 25 messages per second. make it higher for testing if you want
class Car(object):
	ID = ""
	length = 0
	linear_velocity = 0
	angular_velocity = 0
	# add other things here in future if needed

	def __init__(self,ID,length, linear = 0, angular = 0):
		self.ID = ID
		self.length = length
		self.linear_velocity = linear
		self.angular_velocity = angular
def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

# Since the communication can get very busy with each car repeatedly sending data, we try our best to reduce the
# size of the communication by compressing and serializing it. Since we send only textual data, it can be compressed
# greatly and reduce latency which is great for communication
def send_zipped_packet(socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    p = pickle.dumps(obj, protocol)
    z = zlib.compress(p)
    return socket.send(z, flags=flags)

# Each car client will be an instance of this class. It connects to the server and repeatedly sends information to it
# until you shut it off. 
# As soon as the instance is initialized, an identity of the client is created that helps us to identify the client
# on server side. The identity will usually be the ID of the car but can be changed to something else by modifying
# socket.identity attribute
class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, car):
        self.id = car.ID
        threading.Thread.__init__ (self)
        self.car = car
    def run(self):
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
            print('Req #%d sent..' % (reqs))
            #socket.send_string(u'request #%d' % (reqs))
            send_zipped_packet(socket, self.car)
            for i in range(5):
                sockets = dict(poll.poll(RATE))
                if socket in sockets:
                    msg = socket.recv()
                    tprint('Client %s received: %s' % (identity, msg))

        socket.close()
        context.term()

if __name__ == '__main__':
	car1 = Car("A", 1, 1, 0)
	car2 = Car("B", 1, 0, 1)
	client1 = ClientTask(car1)
	client1.start()
	client2 = ClientTask(car2)
	client2.start()