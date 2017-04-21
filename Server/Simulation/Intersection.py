import queue as Queue
import values
import random


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

    def updateIntersectionQueues(self, carList, time):
        ''' Iterate through the list of all cars in the intersection radius '''
        for i in range(0, len(carList)):
            ''' If the car is within the inner radius then it must me marked to be regulated '''
            if(carList[i].positionX >= self.positionX - self.width and carList[i].positionX <= self.positionX and carList[i].direction == "horizontal"):
                if(not carList[i].inQueue):            # If the car is not already in queue
                    self.gui.highlightCar(carList[i], "blue")
                    self.gui.updateCarInformationDisplay(carList[i])
                    carList[i].intersectionFlag = True
                    carList[i].inQueue = True                 # Raise the car's in queue flag
                    carList[i].intersectionTimeStamp = time   # Stamp the arrival time
                    self.queueX.put(carList[i])               # Place car in queue to be regulated

            if(carList[i].positionY >= self.positionY - self.length and carList[i].positionY <= self.positionY and
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

        print(len(self.IntersectionList))

        if self.IntersectionList:
            for i in range(0, len(self.IntersectionList)):
                if(self.IntersectionList[i].positionX > self.positionX + self.width / 2 and self.IntersectionList[i].direction == "horizontal" and self.IntersectionList[i].regulationFlag is False):
                    self.IntersectionList[i].velocityX = values.maxVelocity
                    self.IntersectionList[i].intersectionFlag = False
                    self.IntersectionList[i].inQueue = False
                    self.gui.highlightCar(self.IntersectionList[i], "black")
                    removeList.append(self.IntersectionList[i])
                    # self.IntersectionList.remove(self.IntersectionList[i])

                elif(self.IntersectionList[i].positionY > self.positionY + self.length / 2 and self.IntersectionList[i].direction == "vertical" and self.IntersectionList[i].regulationFlag is False):
                    self.IntersectionList[i].velocityY = values.maxVelocity
                    self.IntersectionList[i].intersectionFlag = False
                    self.gui.highlightCar(self.IntersectionList[i], "red")
                    removeList.append(self.IntersectionList[i])
                    # self.IntersectionList.remove(self.IntersectionList[i])
            for i in range(len(removeList)):
                self.IntersectionList.remove(removeList[i])

            removeList.clear()

        elif(values.conventionalSimFlag and carList[i].positionX < self.positionX and values.conventionalStoppedX and carList[i].velocityX > 0):
                print("X CAR IS STOPPED")
                carList[i].velocityX = 0
        elif(values.conventionalSimFlag and carList[i].positionY < self.positionY and values.conventionalStoppedY and carList[i].velocityY > 0):
                print("Y CAR IS STOPPED")
                carList[i].velocityY = 0

        elif(values.conventionalSimFlag and carList[i].direction is "vertical" and carList[i].positionX < self.positionX and not values.conventionalStoppedX):
                carList[i].velocityX = values.maxVelocity

        elif(values.conventionalSimFlag and carList[i].direction is "horizontal" and carList[i].positionY < self.positionY and not values.conventionalStoppedY):
                carList[i].velocityY = values.maxVelocity


    def printIntersectionDetails(self):
        print("Center Point = (" + str(self.positionX) + ", " + str(self.positionY) + ")")
        print("Width = " + str(self.width) + " Length = " + str(self.length))
        print("X + Width = " + str(self.positionX + self.width) + " Y + Length = " + str(self.positionY + self.length))