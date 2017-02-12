import Queue


class Intersection:
    queueX = Queue.Queue()                          # Initialize Queue to hold incoming X cars
    queueY = Queue.Queue()                          # Initialize Queue to hold incoming Y cars

    def __init__(self, length, wid, posX, posY):
        self.length = length
        self.width = wid
        self.positionX = posX
        self.positionY = posY

    def updateIntersectionQueues(self, carList, time, gui):
        for i in range(0, len(carList)):
            # Check to see if car it within range of intersection to be regulated
            if(abs(carList[i].positionX) >= self.positionX - 40 and carList[i].velocityY == 0):
                # print("X Lane: CAR MUST BE REGULATED")
                gui.highlightCar(carList[i], "blue")
                if(not carList[i].inQueue):            # If the car is not already in queue
                    carList[i].inQueue = True                 # Raise the car's in queue flag
                    carList[i].intersectionTimeStamp = time   # Stamp the arrival time
                    self.queueX.put(carList[i])               # Place car in queue to be regulated

            elif(abs(carList[i].positionY) >= self.positionY - 80 and carList[i].velocityX == 0):
                # print("Y Lane: CAR MUST BE REGULATED")
                gui.highlightCar(carList[i], "blue")
                if(not carList[i].inQueue):                  # If the car is not already in queue
                    carList[i].inQueue = True                # Raise the car's in queue flag
                    carList[i].intersectionTimeStamp = time  # Stamp the arrival time
                    self.queueY.put(carList[i])              # Place car in queue to be regulated
