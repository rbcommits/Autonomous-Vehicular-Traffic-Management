import zmq
import sys
import threading
import time
import Car
from queue import *
# import Queue
import zlib, pickle as pickle

PORT = 'tcp://*:5570'   # change this to whatever port you want your server to run on

# define a list of server workers
server_workers = []
car_queue = Queue()         # feel free to change the name! I just needed a dummy placeholder to send messages back lol
velocity_queue = Queue()


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()



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


def simulate(ID, msg):
    # start simulation here
    print("server simulate")

    # Simulation done, final velocities calculated
    # time to send data back to the car
    # To make this program work, I set velocity_queue = car_queue so the workers have something to send back
    # but in general, velocity queue should be filled up by the algorithm and then the workers can pull from it and send data back

    print("server velocity queue")
    velocity_queue = car_queue                      # remove this once you start populating this queue via the algorithm
    print("Get velocity queue")
    worker_ID, car = velocity_queue.get()
    print("allocate worker object")
    worker = object()

    print("server for loop")
    for workers in server_workers:
        print("workers.ID = ", workers.ID, "worker_ID = ", worker_ID)
        if worker_ID == workers.ID:
            worker = workers

    # Create packet
    # msg = "Hello from worker " + str(worker.ID)

    # Send packet to car
    print("about to send message")
    worker.worker.send_multipart([ID, msg])


def update_queue(object):
    print("OBJECT TUPLE = ", object)
    car_queue.put(object)
    # simulate()


def deserialize(msg):
    """inverse of send_zipped_packet"""
    p = zlib.decompress(msg)
    return pickle.loads(p)


class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind(PORT)

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        global server_workers
        for i in range(5):
            worker = ServerWorker(context, i)           # i will be the unique worker ID
            worker.start()
            server_workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()


class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context, ID):
        threading.Thread.__init__(self)
        self.context = context
        self.ID = ID
        self.worker = self.context.socket(zmq.DEALER)
        self.worker.connect('inproc://backend')

    def run(self):
        tprint('Worker started')
        while True:
            ID, msg = self.worker.recv_multipart()
            msg = deserialize(msg)
            tprint('Worker received %s from %s' % (msg, ID))

            # Add to queue here (both ID and message as an object)
            # or update queue if car ID already exixts

            # We include the ID of the worker who received the request so we can later use the same
            # worker to send the updated velocity back
            car = Car(length=msg.length, width=msg.width, velocityX=msg.velocityX, velocityY=msg.velocityY, startX=msg.positionX, startY=msg.positionY, ID=msg.ID, direction=msg.direction, startTime=msg.startTime)
            update_queue(car)
            #  car_queue.queue(car)
            # somequeue.queue(car)
            # worker.send_multipart([ID, msg])

        self.worker.close()


'''
# def main_func():
if __name__ == "__main__":
    server = ServerTask()
    server.start()
    server.join()
'''