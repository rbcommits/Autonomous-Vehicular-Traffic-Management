import Queue
import values


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
            if(abs(carList[i].positionX) >= self.positionX - self.width and carList[i].velocityY == 0):
                # print("X Lane: CAR MUST BE REGULATED")
                if(not carList[i].inQueue):            # If the car is not already in queue
                    gui.highlightCar(carList[i], "blue")
                    carList[i].displayCar()
                    gui.updateCarInformationDisplay(carList[i])
                    carList[i].inQueue = True                 # Raise the car's in queue flag
                    carList[i].intersectionTimeStamp = time   # Stamp the arrival time
                    self.queueX.put(carList[i])               # Place car in queue to be regulated

            if(abs(carList[i].positionY) >= self.positionY - self.length and carList[i].velocityX == 0):
                # print("Y Lane: CAR MUST BE REGULATED")
                if(not carList[i].inQueue):                  # If the car is not already in queue
                    gui.highlightCar(carList[i], "blue")
                    gui.updateCarInformationDisplay(carList[i])
                    carList[i].inQueue = True                # Raise the car's in queue flag
                    carList[i].intersectionTimeStamp = time  # Stamp the arrival time
                    self.queueY.put(carList[i])              # Place car in queue to be regulated

            '''
            if(carList[i].velocityX != values.maxVelocity and carList[i].velocityX > 0 and carList[i].positionX > self.positionX + 80):
                # We must adjust this x car to max velocity it has left the interscetion
                carList[i].velocityX = values.maxVelocity
                carList[i].displayCar()
                gui.highlightCar(carList[i], "green")
                print "ADJUSTING X VEL"
                return

            if(carList[i].velocityY != values.maxVelocity and carList[i].velocityY > 0):
                # We must adjust this y car to max velocity it has left the interscetion
                carList[i].velocityY = values.maxVelocity
                gui.highlightCar(carList[i], "green")
                print "ADJUSTING Y VEL"
                return
            '''
    def restoreVelocities(self, carList):
        for i in range(0, len(carList)):
            if(carList[i].positionX > 600 + self.width and carList[i].velocityX < 1 and carList[i].velocityX > 0):
                carList[i].velocityX = values.maxVelocity
                carList[i].displayCar()
                print self.positionX, " and ", self.width

            elif(carList[i].positionY > self.positionY + self.length * 2 and carList[i].velocityY < 1 and carList[i].velocityY > 0):
                carList[i].velocityY = values.maxVelocity
                carList[i].displayCar()
