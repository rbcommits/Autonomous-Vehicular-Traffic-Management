import values
import random


def collisionDetection(queueX, queueY, gui):

    if(not queueX.empty() and not queueY.empty()):
        print "Two Cars To Regulate"
        carX = queueX.get()     # attain x car enterint intersection
        carY = queueY.get()     # attain y car entering intersection

        # Now determine which car entered the inersection first
        if(abs(carX.positionX) < abs(carY.positionY)):
            # X is the first car
            print "x is the first car"
            gui.highlightCar(carY, "black")
            slowCar(carSlow=carY, carFull=carX, slowY=True)

        elif(abs(carY.positionY) < abs(carX.positionX)):
            # Y is the first car
            print "y is the first car"
            gui.highlightCar(carX, "black")
            slowCar(carSlow=carX, carFull=carY, slowY=False)

        else:
            # Both cars have the same position on their relative axis'
            print "they are the same!"
            rollSlow = random.randint(1, 2)
            if(rollSlow == 1):
                slowCar(carSlow=carY, carFull=carX, slowY=True)
            elif(rollSlow == 2):
                slowCar(carSlow=carX, carFull=carY, slowY=False)

    # If the cars in the queue and past the intersection without being regulated yet pop it
    # We dont need it
    elif(not queueX.empty()):
        if(queueX.queue[0].positionX > 490):
            carX = queueX.get()

    elif(not queueY.empty()):
        if(queueY.queue[0].positionY > 490):
            carY = queueY.get()


# Function to reduce velocity of a car
def slowCar(carSlow, carFull, slowY):
    print "Slow Car"
    if(slowY):
        print "Slow down the Y car"
        while(True):
            carSlow.velocityY = carSlow.velocityY - 0.4
            print "Slowed"
            if(collide(carX=carFull, carY=carSlow) is False):
                break

    elif(not slowY):
        print "Slow down the X car"
        while(True):
            carSlow.velocityX = carSlow.velocityX - 0.4
            print "Slowed"
            if(collide(carX=carSlow, carY=carFull) is False):
                break


# Function to detect a possible collision
def collide(carX, carY):
    print "Check for a test collision"
    # Create two copies of cars to test
    carTestX = carX
    carTestY = carY

    while(True):
    # for i in range(0, 100):
        if(((carTestX.positionX >= carTestY.positionX - 1) and (carTestX.positionX <= carTestY.positionX + 1)) or ((carTestX.positionY >= carTestY.positionY - 1) and (carTestX.positionY <= carTestY.positionY - 1))):
            print "Test collision occured"
            return True
        if(abs(carTestX.positionX > 600)):
            print "Test succesful regulation"
            return False

        carTestX.updatePosition(values.timeInterval)
        carTestY.updatePosition(values.timeInterval)
