from tkinter import Tk
import Simulation
import server
from server import ServerTask
from server import Car
from server import ServerWorker
import _thread as thread
import values
import signal
if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
    root = Tk()
    values.init(root)
    server = server.ServerTask()
    thread.start_new_thread(server.start, ())
    root.mainloop()
