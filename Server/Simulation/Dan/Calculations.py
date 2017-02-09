def collisionDetection(queueX, queueY):
    print "Entering Collistion Detection"

    print queueX.qsize()
    print queueY.qsize()

    if(not queueX.empty() and not queueY.empty()):
        carX = queueX.get()     # attain x car enterint intersection
        carY = queueY.get()     # attain y car entering intersection

        # Now determine which car entered the inersection first
        if(abs(carX.positionX) < abs(carY.positionY)):
            # X is the first car
            print "x is the first car"
            slowCar(carSlow=carY, carFull=carX, slowY=True)

        elif(abs(carY.positionY) < abs(carX.positionX)):
            # Y is the first car
            print "y is the first car"
            slowCar(carSlow=carX, carFull=carY, slowY=False)

        else:
            # Both cars have the same position on their relative axis'
            print "they are the same!"
    else:
        print "No cars in range of intersection"


# Function to reduce velocity of a car
def slowCar(carSlow, carFull, slowY):
    print "Slow Car"
    if(slowY):
        print "Slow down the Y car"
        while(True):
            carSlow.velocityY = carSlow.velocityY - 0.1
            if(collide(carX=carFull, carY=carSlow) is False):
                break

    elif(not slowY):
        print "Slow down the X car"
        while(True):
            carSlow.velocityX = carSlow.velocityX - 0.1
            if(collide(carX=carSlow, carY=carFull) is False):
                break


# Function to detect a possible collision
def collide(carX, carY):
    print "Check for a test collision"
    # Create two copies of cars to test
    carTestX = carX
    carTestY = carY
    while(True):
        carTestX.displayCar()
        if((carTestX.positionX == carTestY.positionX) and (carTestX.positionY == carTestY.positionY)):
            print "Test collision occured"
            return True
        if(abs(carTestX.positionX > 5)):
            print "Test succesful regulation"
            return False

        carTestX.updatePosition(0.1)
        carTestY.updatePosition(0.1)
