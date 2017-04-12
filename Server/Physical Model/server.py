import zmq
import sys
import threading
import time
import Car
from queue import *
# import Queue
import zlib, pickle as pickle

PORT = 'tcp://*:5570'   # change this to whatever port you want your server to run on
"""
 Server code for the Atuonomous Car system.
 Accepts a data packet of the format {[length], [linear velocity, angular velocity]} from cars in range
 and then modulates(increases/decreases) their velocities accordingly to make sure that each car can cross the intersection without crashing 
 or stopping
"""
"""
 We will use Asyncronous, non blocking message passing interface here to send messages between multiple clients and the server
 This is because we want to make sure we have the identity of each client as we receive data and that the request does not block the program
 until a response is sent. ( In a blocking assignment, you cannot proceed until a response is sent immidiately back to the sender)

 A basic idea to follow here:
    -> A client gets in range and connects to the server sending it's identity and initial velocities
    -> Server accepts it and adds that to a working queue
    -> As more cars connect and send their data, they get added to the same queue
    -> As those same cars send updated information about their velocities, the server updates the queue instead of adding them to the queue again
    -> Calculate velocities that would allow all the cars connected to the server to pass through the intersection without crashing
    -> Asyncronously send the data back to the cars
    -> Remove the car from the queue and soon after the client disconnects from the server as well
"""


"""
 For simulation purposes, if you want to work with the terminal, you can use a 2D numpy array like
 0 0 0 0 0
 0 0 1 0 0
 1 0 0 1 0
 0 0 0 0 0
 0 0 1 0 0

 where each 1 represents a car object with a unique ID and velocities.
 To make it dynamic, a dedicated thread will have to take care of the array
. ie update it every second by moving the cars according to their velocities.

Assuming each car has a velocity of 1 unit/second, and the above initial array at time 0,
the updated array at time 1 should be:
 0 0 1 0 0
 0 0 0 0 0
 0 1 0 0 1
 0 0 1 0 0
 0 0 0 0 0

 Where the cars just moved 1 unit in their respective direction

 At time 2, a crash should occur since 2 cars will be at the same position.
 One easy way to determine that would be to check what the value of the index is before
 updating it. So one of the cars moves to the center and puts a 1 there, when the updater
 tries to put the second car at the same place it realizes that there is already a 1 at index [3,3]
 and so a crash occurred.

 To fix it, whichever car was higher in the queue gets to go first and the other one gets slowed down
 Lets assume car at [3,4] came in first so it's velocity remains unmodified, but the velocity of [2,3] gets reduced from 1 to
 say a 0.5 which allows [3,4] to pass safely

 A different thread will have to take care of the queue as well since there will be more than 1 car at a time and
 we want to make sure each and every car passes through safe and sound

 A prospective solution to the problem can be to simulate the queue at every frame, if a crash occurs, fix it, simulate again
 The new simulation should have 1 less crash than before since we fixed one of them. keep simulating till there is no impending crash
 and then finally send the speeds to the cars

 This is kind of tricky since you would have to do the multiple iterations of the simulation very quickly before the real cars actually
 crash. If created in an optimised fashion, the simulation can be done in atomic time and delays avoided.

 I'm sure there's a bunch of solutions to it. This just came to me as I was typing and I figured i'd leave this here for you to read.
 If you have a better solution, feel free to implement that and add a tiny explanation as comments

"""
"""
 Since you are working with multiple threads, you either need to work with event listeners that alert the simulation thread to re simulate as
 the queue thread adds new cars to the queue or you can simply have the simulation running forever and referencing the queue at every step.
 The latter might consume more resources as there will be time when the simulator will try to simulate empty roads but it's an easy way to
 avoid event listeners in my opinion
"""

"""
 Also since we sort of decided to have the car update velocities about 25 times per second, it would be unreal to have a single server
 handle that many requests from multiple cars at a time so I decided to have a cluster of server workers running to balance the load.
 It will take real testing for us to decide the optimal number of workers for load balancing but for now I am going with about 5 workers
"""

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