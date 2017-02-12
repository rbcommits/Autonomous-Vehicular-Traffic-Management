# GUI
from Tkinter import Canvas, Button


class carGUI:

    carDict = {}
    carIDs = []

    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        '''
        self.label = Label(master, text="This is my first GUI!")
        #self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()
        '''

        # Initialize Canvas
        self.canv = Canvas(master)
        self.canv.pack(fill='both', expand=True)

        # Initialize X-Lane
        self.xTop = self.canv.create_line(0, 470, 1000, 470, fill='black', tags=('top'))
        self.xBottom = self.canv.create_line(0, 510, 1000, 510, fill='black', tags=('left'))

        # Initialize Y-Lane
        self.yLeft = self.canv.create_line(470, 0, 470, 1000, fill='blue', tags='right')
        self.yRight = self.canv.create_line(510, 0, 510, 1000, fill='blue', tags='bottom')

        # Highlight Intersection
        self.rect = self.canv.create_rectangle(470, 470, 510, 510, fill='green')

        # Show Regulation Lines
        self.xLimit = self.canv.create_line(470 - 20, 450, 470 - 20, 530, fill="red")
        self.yLimit = self.canv.create_line(450, 470 - 20, 530, 470 - 20, fill="red")

        # Create button to begin simulation
        b = Button(text="Start Simluation!", command=self.simClickListener)
        b.pack()

    def drawCar(self, lane, ID):

        if(lane == 1):
            # Draw an X car
            self.rect = self.canv.create_rectangle(0, 485, 10, 495, fill='yellow')
        elif(lane == 2):
            # Draw a Y car
            self.rect = self.canv.create_rectangle(485, 0, 495, 10, fill='red')

        # Register the ID of the car 
        self.carIDs.append(ID)
        # Ad the key value pair to the car dictionary for the GUI
        self.carDict[ID] = self.rect

    def moveCars(self, carList, timeInterval):

        self.master.update_idletasks()  # THIS UPDATES THE GUI

        for i in range(0, len(carList)):
            self.canv.move(self.carDict[carList[i].ID], carList[i].velocityX * timeInterval, carList[i].velocityY * timeInterval)

    def highlightCar(self, car, color):
        self.canv.itemconfig(self.carDict[car.ID], fill=color)

    def simClickListener(self):
        from Simulation import simulation as sim
        sim(self)
