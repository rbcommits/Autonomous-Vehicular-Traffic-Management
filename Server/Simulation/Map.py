import Intersection
import gui


class Map:

    def __init__(self, intersectionCount):
        self.intersectionCount = intersectionCount

    def generateMap(self):
        for i in range(len(self.intersectionCount)):
            # Procedurarly position intersection count:

            if(len(self.intersectionCount) == 1):
                print("Map has one intersection")

                # We will generate one intersection in the middle of the map. This is the base case
                currIntersection = Intersection(length=40, wid=40, posX=490, posY=490)

            elif(len(self.intersectionCount) == 2):
                print("Map has two intersections")

            elif(len(self.intersectionCount) == 3):
                print("Map has three intersections")

            elif(len(self.intersectionCount == 5)):
                print("Map has three intersectoins")



