import logging
import queue
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from abc import abstractmethod

logger = logging.getLogger(__name__)


class TextHandler(logging.Handler):
    """This class allows to log to a tkinter text or scroleldtext widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # store a reference to the text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state="normal")
            self.text.insert(END, msg + '+n')
            self.text.configure(state="disabled")
            # autoscroll to the bottom
            self.text.yview(END)

        self.text.after(0, append)


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class Application(Frame):
    WINDOW_WIDTH = 740
    WINDOW_HEIGHT = 600
    DEFAULT_CAR_NR = 14

    def __init__(self, master=None):
        super().__init__(master)
        master.title('Page indexer')
        master.resizable(width=FALSE, height=FALSE)
        master.geometry('{}x{}'.format(Application.WINDOW_WIDTH, Application.WINDOW_HEIGHT))

        # Building the layout

        # Setting the frames
        self.index_frame = Frame(master, width=Application.WINDOW_WIDTH, height=50)
        self.date_frame = Frame(master, width=Application.WINDOW_WIDTH, height=50)
        self.cars_frame = Frame(master, width=Application.WINDOW_WIDTH, height=50)
        self.control_frame = Frame(master, width=Application.WINDOW_WIDTH, height=50)
        self.debug_frame = Frame(master, width=Application.WINDOW_WIDTH, height=50)

        # Placing frames in the window
        self.index_frame.grid(row=0)
        self.date_frame.grid(row=1)
        self.cars_frame.grid(row=2)
        self.control_frame.grid(row=3)
        self.debug_frame.grid(row=4)

        # Creating index_frame widgets
        self.bord_label = Label(self.index_frame, text="Indexul de inceput la borderou")
        self.bord_input = Entry(self.index_frame)

        self.par_label = Label(self.index_frame, text='Indexul de inceput la parcurs')
        self.par_input = Entry(self.index_frame)

        # Creating date_frame widgets
        self.date_label = Label(self.date_frame, text=" Data de inceput")
        self.date_input = Entry(self.date_frame)

        self.days_label = Label(self.date_frame, text="Nr de zile")
        self.days_input = Entry(self.date_frame)

        # Creating cars_frame widgets
        self.nr_cars_label = Label(self.cars_frame, text="Nr de masini")
        self.nr_cars_input = Entry(self.cars_frame)

        self.nr_index_label = Label(self.cars_frame, text="Nr")
        self.car_label = Label(self.cars_frame, text='Nr masinii')
        self.car_series = Label(self.cars_frame, text="Seria masinii")
        self.driver_name_label = Label(self.cars_frame, text="Numele soferului(de dorit fara diacritice)")
        self.miss_dates_label = Label(self.cars_frame, text="Zile libere")

        self.Cars = []
        for _ in range(Application.DEFAULT_CAR_NR):
            curr_label = Label(self.cars_frame, text=str(_ + 1))
            curr_car_name = Entry(self.cars_frame)
            curr_car_series = Entry(self.cars_frame)
            curr_car_driver_name = Entry(self.cars_frame)
            curr_miss_dates = Entry(self.cars_frame)
            self.Cars.append([curr_label,curr_car_series, curr_car_name, curr_car_driver_name, curr_miss_dates])

        # Creating the buttons widgets - control_frame
        self.submit_button = Button(self.control_frame, text="Submit", command=self.submit)  # todo define command function
        self.execute_button = Button(self.control_frame, text="Execute", command=self.execute)  # todo define command function

        # Placing the index_frame widgets in the frame
        self.bord_label.grid(row=0, column=0)
        self.bord_input.grid(row=0, column=1)

        self.par_label.grid(row=0, column=2)
        self.par_input.grid(row=0, column=3)

        # Placing the date_frame widgets in the frame
        self.date_label.grid(row=0)
        self.date_input.grid(row=0, column=1)

        self.days_label.grid(row=0, column=2)
        self.days_input.grid(row=0, column=3)

        # Placing the cars_frame widgets in the frame
        self.nr_cars_label.grid(row=0, column=1, sticky='e')
        self.nr_cars_input.grid(row=0, column=2, sticky='w')

        self.nr_index_label.grid(row=1)
        self.car_label.grid(row=1, column=1)
        self.car_series.grid(row=1, column=2)
        self.driver_name_label.grid(row=1, column=3)
        self.miss_dates_label.grid(row=1, column=4)
        i = 2
        for el in self.Cars:
            el[0].grid(row=i)
            el[1].grid(row=i, column=1)
            el[2].grid(row=i, column=2)
            el[3].grid(row=i, column=3)
            el[4].grid(row=i, column=4)
            i += 1

        # Placing the buttons in the control_frame
        self.submit_button.grid(row=0)
        self.execute_button.grid(row=0, column=1)

        console = ConsoleLog(self.debug_frame)
        logger.info("Interface loaded successfully")

    @abstractmethod
    def submit(self):
        logger.critical("Method submit not implemented")
        pass

    @abstractmethod
    def execute(self):
        logger.critical("Method execute not implemented")
        pass


class ConsoleLog:
    def __init__(self, frame):
        self.frame = frame
        self.scrolled_text = ScrolledText(self.frame, state="disabled", bg="dodger blue")
        self.scrolled_text.grid(row=0, column=4)
        self.scrolled_text.configure(font="tkFixedFont", state="normal")
        self.scrolled_text.tag_config("INFO", foreground="black")
        self.scrolled_text.tag_config("WARNING", foreground="OrangeRed4")
        self.scrolled_text.tag_config("DEBUG", foreground='purple4')
        self.scrolled_text.tag_config("ERROR", foreground='red')
        self.scrolled_text.tag_config("CRITICAL", foreground="red4", underline="1")
        # Create a loggin handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt="%I:%M:%S %p")
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        self.frame.after(100, self.poll_log_queue)

    def display_log(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state="normal")
        self.scrolled_text.insert(END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state="disabled")
        # autoscroll to bottom
        self.scrolled_text.yview(END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message to display in the queue
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                print(record)
                self.display_log(record)

        self.frame.after(100, self.poll_log_queue)


def main():
    logging.basicConfig(level=logging.DEBUG)
    root = Tk()
    app = Application(root)
    app.mainloop()


if __name__ == "__main__":
    main()