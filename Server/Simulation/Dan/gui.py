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
        self.top = self.canv.create_line(0, 470, 1000, 470, fill='black', tags=('top'))
        self.left = self.canv.create_line(0, 510, 1000, 510, fill='black', tags=('left'))

        # Initialize Y-Lane
        self.right = self.canv.create_line(470, 0, 470, 1000, fill='blue', tags='right')
        self.bottom = self.canv.create_line(510, 0, 510, 1000, fill='blue', tags='bottom')

        # Create button to begin simulation
        b = Button(text="click me", command=self.simClickListener)
        b.pack()

    def drawCar(self, lane, ID):

        if(lane == 1):
            # Draw an X car
            self.rect = self.canv.create_rectangle(0, 480, 10, 490, fill='yellow')
        elif(lane == 2):
            # Draw a Y car
            self.rect = self.canv.create_rectangle(480, 0, 490, 10, fill='red')

        # Register the ID of the car 
        self.carIDs.append(ID)
        # Ad the key value pair to the car dictionary for the GUI
        self.carDict[ID] = self.rect

    def moveCars(self, carList):

        self.master.update_idletasks()  # THIS UPDATES THE GUI

        for i in range(0, len(carList)):
            self.canv.move(self.carDict[carList[i].ID], carList[i].velocityX, carList[i].velocityY)

    def simClickListener(self):
        from Simulation import simulation as sim
        sim(self)
