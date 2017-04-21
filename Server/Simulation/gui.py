# GUI
from tkinter import Canvas, Button, Checkbutton, IntVar
import values


class carGUI:

    carDict = {}
    carIDs = []

    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        # Initialize Canvas
        self.canv = Canvas(master)
        self.canv.pack(fill='both', expand=True)

        # Call Drawing functions
        self.drawLanes()

        # Create button to begin simulation
        b = Button(text="Start Simluation!", command=self.simClickListener)
        b.pack()

        # Create checkbox to differentiate real world sim from autonomous sim
        self.CheckVar = IntVar()
        self.checkConventional = Checkbutton(text="Conventional System", variable=self.CheckVar, onvalue=1, offvalue=0, height=5)
        self.checkConventional.pack()

        # Create text fields to show first in queue cars
        self.carDisplayX = self.canv.create_text(10, 10, anchor="nw", fill="red")
        self.carDisplayY = self.canv.create_text(600, 10, anchor="nw", fill="black")

    def drawCar(self, lane, ID, dirNumber):

        # If this a horizontally travelling car draw it
        if(lane == 1):
            self.rect = self.canv.create_rectangle(0, 485, 10, 495, fill='black')

        # This is a vertically travelling car in the first lane
        elif(lane == 2 and dirNumber == 0):
            self.rect = self.canv.create_rectangle(485, 0, 495, 10, fill='red')

        # This is a vertically travelling car in the second lane
        elif(lane == 2 and dirNumber == 1):
            self.rect = self.canv.create_rectangle(1015, 0, 1025, 10, fill='red')


        self.canv.addtag_below(self.rect, "HELLO")

        # Register the ID of the car
        self.carIDs.append(ID)
        # Ad the key value pair to the car dictionary for the GUI
        self.carDict[ID] = self.rect

    def moveCars(self, carList, timeInterval):

        self.master.update_idletasks()  # THIS UPDATES THE GUI

        for i in range(0, len(carList)):
            self.canv.move(self.carDict[carList[i].ID], carList[i].velocityX * timeInterval, carList[i].velocityY * timeInterval)

    def moveCar(self, car, timeInterval):
        self.master.update_idletasks()
        self.canv.move(self.carDict[car.ID], car.velocityX * timeInterval, car.velocityY * timeInterval)

    def highlightCar(self, car, color):
        self.canv.itemconfig(self.carDict[car.ID], fill=color)
        self.master.update_idletasks()


    def simClickListener(self):
        from Simulation import simulation as sim
        sim(self)

    def updateCarInformationDisplay(self, car):
        carData = "position X = " + str(car.positionX) + "\nposition Y = " + \
            str(car.positionY) + "\nvelocity X = " + str(car.velocityX) + \
            "\nvelocity Y = " + str(car.velocityY)

        if(car.velocityX > 0):
            self.canv.itemconfig(self.carDisplayX, text=carData)

        else:
            self.canv.itemconfig(self.carDisplayY, text=carData)

    def drawLanes(self):

        # Initialize X-Lane
        self.xTop = self.canv.create_line(0, 470, 10000, 470, fill='black', tags=('top'))
        self.xBottom = self.canv.create_line(0, 510, 10000, 510, fill='black', tags=('left'))

        # Initialize first Y-Lane
        self.yLeft = self.canv.create_line(470, 0, 470, 10000, fill='blue', tags='right')
        self.yRight = self.canv.create_line(510, 0, 510, 10000, fill='blue', tags='bottom')

        # Initialize second Y - Lane
        self.yLeft = self.canv.create_line(1000, 0, 1000, 10000, fill='blue', tags='right')
        self.yRight = self.canv.create_line(1040, 0, 1040, 10000, fill='blue', tags='bottom')

    def drawIndicationLines(self, Intersection):

        # Draw the entrance lines
        self.entranceX = self.canv.create_line(Intersection.positionX - Intersection.width, Intersection.positionY - Intersection.length, Intersection.positionX - Intersection.width, Intersection.positionY + Intersection.length, fill="red")
        self.entranceX = self.canv.create_line(Intersection.positionX - Intersection.width, Intersection.positionY - Intersection.length, Intersection.positionX + Intersection.width, Intersection.positionY - Intersection.length, fill="red")

        # Paint the intersection
        self.rect = self.canv.create_rectangle(Intersection.positionX - Intersection.width / 2, Intersection.positionY - Intersection.length / 2, Intersection.positionX + Intersection.width / 2, Intersection.positionY + Intersection.length / 2, fill="green")