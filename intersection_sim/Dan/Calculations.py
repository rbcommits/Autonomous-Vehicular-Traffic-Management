def collisionDetection(queueX, queueY):
    print "Entering Collistion Detection"

#    print queueX.qsize()
#    print queueY.qsize()

    if(not queueX.empty() and not queueY.empty()):
        carX = queueX.get()     # attain x car enterint intersection
        carY = queueY.get()     # attain y car entering intersection

        # Now determine which car entered the inersection first
        if(abs(carX.positionX) < abs(carY.positionY)):
            # X is the first car
            print "x is the first car"

        elif(abs(carY.positionY) < abs(carX.positionX)):
            # Y is the first car
            print "y is the first car"
        else:
            # Both cars have the same position on their relative axis'
            print "they are the same!"
    else:
        print "No cars in range of intersection"

def slowCar(car):

    print car.displayCar()
