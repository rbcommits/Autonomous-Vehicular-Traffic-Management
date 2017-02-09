import Calculations
from random import randint
from Car import Car
from Intersection import Intersection


def randomCarGenerator():
    direction = randint(1, 2)
    if(direction == 1):
        # Generate a vertically traveling car
        velocityX = randint(1, 4)
        car = Car(length=5, width=5, velocityX=velocityX, velocityY=0, startX=-20, startY=0)
    elif(direction == 2):
        # Generate a vertically traveling car
        velocityY = randint(1, 4)
        car = Car(length=5, width=5, velocityX=0, velocityY=velocityY, startX=0, startY=-20)

    return car


def cleanList(carList):
    for i in range(len(carList), 0):
        if(carList[i].positionX > 5 or carList[i].positionY > 5):
            del carList[i]


def simulation():
    # Initialize instance of intersection
    currIntersection = Intersection(100, 100, 10, 10)
    # Declare cars:
    # (self, length, width, velocityX, velocityY, startX, startY)
    car1 = Car(5, 5, 3.1, 0, -20, 0)
    car2 = Car(5, 5, 0, 3, 0, -20)

    # Initialize array to contain car
    carList = []                                            # initialize car array
    carList.append(car1)                                    # place car in array
    carList.append(car2)                                    # place car in array

    for i in range(0, len(carList)):
        carList[i].displayCar()

    elapsedTime = 0                                         # initialize time in seconds
    intervalTime = 1
    runSim = True                                           # bool to stop simulation

    # Begin simulation:
    while(runSim):

        # Remove processed cars from the intersection lsit 
        cleanList(carList)

        # Check to see if we should end simulation
        if(elapsedTime > 10):
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

        # Every seconds generate a new car
        if(elapsedTime % 1 is 0):
            # Generate a new car
            newCar = randomCarGenerator()
            carList.append(newCar)

        # If a car has exited the intersection remove it from the array 
    print len(carList)


simulation()
