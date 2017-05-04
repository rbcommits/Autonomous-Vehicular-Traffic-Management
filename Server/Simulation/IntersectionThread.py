from threading import Thread
import Calculations


class InterThread(Thread):

    def __init__(self, intersection, gui, carList):

        Thread.__init__(self)
        self.intersection = intersection
        self.gui = gui
        self.carList = carList

    def run(self):
        # print("self inter = " + str(self.intersection) + "self gui = " + str(self.gui) + "self carList = " + str(self.carList))
        # print("running")
        Calculations.collisionDetection(self.intersection.queueX, self.intersection.queueY, self.gui, self.intersection, self.carList)
