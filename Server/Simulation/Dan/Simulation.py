import Calculations
from gui import carGUI
from random import randint
from Car import Car
from Intersection import Intersection


# Initialize array to contain cars
carList = []


def randomCarGenerator(LiveGUI):
    direction = randint(1, 2)

    # Generate a Unique ID
    generateID = True
    while(generateID):
        generateID = False
        ID = randint(0, 10000)
        for i in range(0, len(carGUI.carIDs)):
            if ID == carGUI.carIDs[i]:
                generateID = True

    if(direction == 1):
        # Generate a vertically traveling car
        velocityX = 10  # randint(1, 4)
        car = Car(length=5, width=5, velocityX=velocityX, velocityY=0, startX=-20, startY=0, ID=ID)
        LiveGUI.drawCar(direction, ID)
    elif(direction == 2):
        # Generate a vertically traveling car
        velocityY = 10    # randint(1, 4)
        car = Car(length=5, width=5, velocityX=0, velocityY=velocityY, startX=0, startY=-20, ID=ID)
        LiveGUI.drawCar(direction, ID)

    return car


def cleanList(carList, LiveGUI):
    for i in range(len(carList), 0):
        if(carList[i].positionX > 5 or carList[i].positionY > 5):
            del LiveGUI.carDict[carList[i].ID]
            del carList[i]


def simulation(gui):
    # Initialize instance of intersection
    currIntersection = Intersection(100, 100, 10, 10)

    for i in range(0, len(carList)):
        carList[i].displayCar()

    elapsedTime = 0                                         # initialize time in seconds
    intervalTime = 1
    runSim = True                                           # bool to stop simulation

    # Begin simulation:
    while(runSim):

        # Remove processed cars from the intersection list
        cleanList(carList, gui)

        # Check to see if we should end simulation
        if(elapsedTime > 1000):
            runSim = False                                  # if time condition is true runSim to false
        elapsedTime += intervalTime                         # increment 100 mili second

        # Check if cars are in intersection range
        currIntersection.updateIntersectionQueues(carList, elapsedTime)
        # Check for possible collisions
        Calculations.collisionDetection(currIntersection.queueX, currIntersection.queueY)

        # Update the positions of the cars in the list
        for i in range(0, len(carList)):
            # THIRD update position
            carList[i].updatePosition(intervalTime)
            carList[i].displayPosition()

        # Update the GUI positions
        gui.moveCars(carList)

        # Every seconds generate a new car
        print "Module is:  ", elapsedTime % 1
        if(elapsedTime % 1 is 0):
            # Generate a new car
            newCar = randomCarGenerator(gui)
            carList.append(newCar)

        # If a car has exited the intersection remove it from the array

    print len(carList)
