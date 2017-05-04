import queue as Queue
import values
import random
import _thread as thread


class Intersection:

    def __init__(self, length, wid, posX, posY, gui):
        self.queueX = Queue.Queue()
        self.queueY = Queue.Queue()
        self.length = length
        self.width = wid
        self.positionX = posX
        self.positionY = posY
        self.IntersectionList = []
        self.gui = gui
        self.ID = random.randint(0, 1000)
        self.stoppedX = False
        self.stoppedY = False
        self.proceedVert = 0

    def updateIntersectionContainers(self, carList, time):
        ''' Iterate through the list of all cars in the intersection radius '''
        for i in range(0, len(carList)):
            ''' If the car is within the inner radius then it must me marked to be regulated '''
            if(carList[i].positionX >= self.positionX - self.width * 2 and carList[i].positionX <= self.positionX and 
                carList[i].direction == "horizontal" and carList[i].positionY >= self.positionY - self.length and
                carList[i].positionY <= self.positionY + self.length):

                if(not carList[i].inQueue):            # If the car is not already in queue
                    self.gui.highlightCar(carList[i], "blue")
                    self.gui.updateCarInformationDisplay(carList[i])
                    carList[i].intersectionFlag = True
                    carList[i].inQueue = True                 # Raise the car's in queue flag
                    carList[i].intersectionTimeStamp = time   # Stamp the arrival time
                    self.queueX.put(carList[i])               # Place car in queue to be regulated

            if(carList[i].positionY >= self.positionY - self.length * 2 and carList[i].positionY <= self.positionY and
             carList[i].direction == "vertical" and carList[i].positionX >= self.positionX - self.width and
              carList[i].positionX <= self.positionX + self.width):

                if(not carList[i].inQueue):                  # If the car is not already in queue
                    self.gui.highlightCar(carList[i], "blue")
                    self.gui.updateCarInformationDisplay(carList[i])
                    carList[i].intersectionFlag = True
                    carList[i].inQueue = True                # Raise the car's in queue flag
                    carList[i].intersectionTimeStamp = time  # Stamp the arrival time
                    self.queueY.put(carList[i])              # Place car in queue to be regulated

    def restoreVelocities(self, carList):

        removeList = []

        if self.IntersectionList and values.conventionalSimFlag is False:
            for i in range(0, len(self.IntersectionList)):
                if(self.IntersectionList[i].positionX > self.positionX + self.width / 2 and self.IntersectionList[i].direction == "horizontal" and self.IntersectionList[i].regulationFlag is False):
                    self.IntersectionList[i].velocityX = values.maxVelocity
                    self.IntersectionList[i].intersectionFlag = False
                    self.IntersectionList[i].inQueue = False
                    self.gui.highlightCar(self.IntersectionList[i], "black")
                    removeList.append(self.IntersectionList[i])

                elif(self.IntersectionList[i].positionY > self.positionY + self.length / 2 and self.IntersectionList[i].direction == "vertical" and self.IntersectionList[i].regulationFlag is False):
                    self.IntersectionList[i].velocityY = values.maxVelocity
                    self.IntersectionList[i].intersectionFlag = False
                    self.IntersectionList[i].inQueue = False
                    self.gui.highlightCar(self.IntersectionList[i], "black")
                    removeList.append(self.IntersectionList[i])

        elif self.IntersectionList and values.conventionalSimFlag is True:
            for i in range(len(self.IntersectionList)):

                if(values.conventionalSimFlag and self.IntersectionList[i].positionX < self.positionX and self.stoppedX and self.IntersectionList[i].velocityX > 0):
                        print("X CAR IS STOPPED")
                        self.IntersectionList[i].velocityX = 0
                elif(values.conventionalSimFlag and self.IntersectionList[i].positionY < self.positionY and self.stoppedY and self.IntersectionList[i].velocityY > 0):
                        print("Y CAR IS STOPPED")
                        self.IntersectionList[i].velocityY = 0

                elif(values.conventionalSimFlag and self.IntersectionList[i].direction == "vertical" and self.IntersectionList[i].positionX > self.positionX):      # and not self.stoppedX):
                        print("DANIEL ")
                        self.IntersectionList[i].velocityX = values.maxVelocity
                        self.IntersectionList[i].intersectionFlag = False
                        self.IntersectionList[i].inQueue = False
                        self.gui.highlightCar(self.IntersectionList[i], "red")
                        removeList.append(self.IntersectionList[i])

                elif(values.conventionalSimFlag and self.IntersectionList[i].direction == "horizontal" and self.IntersectionList[i].positionY > self.positionY):        # and not self.stoppedY):
                        print("DANIEL HAS TO ")
                        self.IntersectionList[i].velocityY = values.maxVelocity
                        self.IntersectionList[i].intersectionFlag = False
                        self.IntersectionList[i].inQueue = False
                        self.gui.highlightCar(self.IntersectionList[i], "black")
                        removeList.append(self.IntersectionList[i])
                else:
                    if(values.conventionalSimFlag):
                        print("nothing caught it")

        for i in range(len(removeList)):
            self.IntersectionList.remove(removeList[i])

        removeList.clear()

    def printIntersectionDetails(self):
        print("Center Point = (" + str(self.positionX) + ", " + str(self.positionY) + ")")
        print("Width = " + str(self.width) + " Length = " + str(self.length))
        print("X + Width = " + str(self.positionX + self.width) + " Y + Length = " + str(self.positionY + self.length))
