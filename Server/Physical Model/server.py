import zmq
import sys
import threading
import time
from Car import Car
from queue import *
import Simulation
from tkinter import Tk
from gui import carGUI
import zlib, pickle as pickle
import _thread as thread
import values
import signal

PORT = 'tcp://*:5570'   # change this to whatever port you want your server to run on

# define a list of server workers
server_workers = []
car_queue = Queue()         # feel free to change the name! I just needed a dummy placeholder to send messages back lol
velocity_queue = Queue()


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


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

    '''
    print("server for loop")
    for workers in server_workers:
        print("workers.ID = ", workers.ID, "worker_ID = ", worker_ID)
        if worker_ID == workers.ID:
            worker = workers
    '''

    # Create packet
    # msg = "Hello from worker " + str(worker.ID)

    # Send packet to car
    print("about to send message")
    #server_workers[0].send_multipart([ID, msg])
    #worker.worker.send_multipart([ID, msg])

def update_queue(myObj):
    print("UPDATED QUEUE")

    newObjFlag = True
    for i in range(len(values.carList)):
        if(myObj.ID == values.carList[i].ID):
            newObjFlag = False

    if(newObjFlag):
        values.gui.receiveCar(myObj)
        values.carList.append(myObj)

    send_response(1)    # send 1 as dummy velociity

def send_response(msg):
    worker = server_workers[0]
    #worker.worker.send_multipart([1, msg])


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
            print("Spinning up worker")
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
            tprint('Worker received %s from %s' % (msg.velocityX, ID))

            # Add to queue here (both ID and message as an object)
            # or update queue if car ID already exixts

            # We include the ID of the worker who received the request so we can later use the same
            # worker to send the updated velocity back
            car = msg
            #car = Car(length=msg.length, width=msg.width, velocityX=msg.velocityX, velocityY=msg.velocityY, startX=msg.positionX, startY=msg.positionY, ID=msg.ID, direction=msg.direction, startTime=msg.startTime)
            update_queue(car)
            # worker.send_multipart([ID, msg])

        self.worker.close()


# def main_func():
# if __name__ == "__main__":
    # dan = ServerTask()
    # s.server = ServerTask()
    # thread.start_new_thread(dan.start,())
