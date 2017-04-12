import zmq
import sys
import threading
import time
from random import randint, random
import zlib, pickle as pickle

# Launch Multiple car clients to test the server
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

RATE = 40   # Delay in msec between each message. delay of 40ms = 25 messages per second. make it higher for testing if you want

'''
class Car(object):
    ID = ""
    length = 0
    linear_velocity = 0
    angular_velocity = 0
    # add other things here in future if needed

    def __init__(self, ID, length, linear=0, angular=0):
        self.ID = ID
        self.length = length
        self.linear_velocity = linear
        self.angular_velocity = angular
'''


class Car:

    inQueue = False
    intersectionTimeStamp = 0
    accelerationX = 0           # X Acceleration in meters/(second per second)
    accelerationY = 0           # Y Acceleration in meters/(second per second)
    calculationTime = 0         # Attribute to track the total time spent in calculations

    def __init__(self, length, width, velocityX, velocityY, startX, startY, ID, direction, startTime):
        self.length = length            # Length in meters
        self.width = width              # Width in meters
        self.velocityX = velocityX      # X Velocity in meters/second
        self.velocityY = velocityY      # Y Velocity in meters/second
        self.positionX = startX         # X start coordinate
        self.positionY = startY         # Y start coordinate
        self.ID = ID                    # Give car unique ID
        self.waiting = False            # Set the waiting attribute to false
        self.direction = direction
        self.startTime = startTime      # This is the cars stamped time. We must monitor how much time the car spends inside calculations as well
        self.timeStamped = False

    # Print all details of car instance
    def displayCar(self):
        print ("Length: " + self.length)
        print ("Width: " + self.width)
        print ("X Position: " + self.positionX)
        print ("Y Position: " + self.positionY)
        print ("X Velocity: " + self.velocityX)
        print ("Y Velocity: " + self.velocityY)
        print ("X Acceleration: " + self.accelerationX)
        print ("Y Acceleration: " + self.accelerationY)

    def displayPosition(self):
        print ("(" + self.positionX + ", " + self.positionY, ")")

    def displayVelocity(self):
        print ("(" + self.velocityX + ", " +self.velocityY, ")")

    def displayAcceleration(self):
        print ("(" + self.accelerationX + ", " + self.accelerationX, ")")

    def updatePosition(self, time):
        self.positionX = self.positionX + self.velocityX * time
        self.positionY = self.positionY + self.velocityY * time

    # Calculate velocity
    def updateVelocity(self, newPositionX, newPositionY):
        self.velocityX = newPositionX - self.positionX
        self.velocityY = newPositionY - self.positionY

    # Calculate acceleartion
    def updateAcceleration(self, newVelocityX, newVelocityY):
        self.accelerationX = newVelocityX - self.velocityX
        self.accelerationY = newVelocityY - self.velocityY


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
        threading.Thread.__init__(self)
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
            # socket.send_string(u'request #%d' % (reqs))
            send_zipped_packet(socket, self.car)
            for i in range(5):
                sockets = dict(poll.poll(RATE))
                if socket in sockets:
                    msg = socket.recv()
                    tprint('Client %s received: %s' % (identity, msg))

        socket.close()
        context.term()


'''
if __name__ == '__main__':

    car1 = Car("A", 1, 1, 0)
    car2 = Car("B", 1, 0, 1)
    client1 = ClientTask(car1)
    client1.start()
    client2 = ClientTask(car2)
    client2.start()
'''

def newCar(carObject):
    # ClientTask(carObject).start()
    #client.start()
