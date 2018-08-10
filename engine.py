from data import EngineRecord
import os
from ui_interface import *
import openpyxl
import pickle


class Engine(Application):
    PATH = "generated"
    PATH_TO_TEMPLATE_1 = "src/parcurs_template.xlsx"
    PATH_TO_TEMPLATE_2 = "src/borderou_template.xlsx"
    PATH_TO_DATABASE = "src/database.pkl"
    DIRECTION_1 = "Chisinau-Hancesti"
    DIRECTION_2 = "Chisinau-Rusestii Noi"
    DIRECTION_3 = "Chisinau-Ulmu"

    def __init__(self, master=None):
        super().__init__(master)
        self.database = EngineRecord()
        # load the template workbook
        self.parcurs_template = openpyxl.load_workbook(filename=self.PATH_TO_TEMPLATE_1)
        self.borderou_template = openpyxl.load_workbook(filename=self.PATH_TO_TEMPLATE_2)
        self.dir = list()
        self.set_previous()

    def set_previous(self):
        with open(self.PATH_TO_DATABASE, 'rb') as input:
            __database = pickle.load(input)
            self.bord_input.insert(0, str(__database.bord_index))
            self.par_input.insert(0, str(__database.parc_index))
            self.date_input.insert(0, str(__database.start_date))
            self.days_input.insert(0, str(__database.days_nr))
            self.nr_cars_input.insert(0, str(__database.cars_nr))
            # print('Printing database cars')
            # for el in __database.cars:
            #     print(str(el.name))
            #     attrs = vars(el)
            #     for k, val in attrs.items():
            #         print(k,' ', end='')
            i = 0
            for el in __database.cars:
                if i > 13:
                    break
                print(el)
                self.Cars[i][1].insert(0, str(el.name))
                self.Cars[i][2].insert(0, str(el.series))
                self.Cars[i][3].insert(0, str(el.driver_name))
                self.Cars[i][4].insert(0, str((",".join(str(item) for item in el.miss_dates))))
                i += 1


    def submit(self):
        self.database.empty()
        logger.debug("Starting submitting the data...")
        __bord_index = self.bord_input.get()
        self.database.set_bord_index(__bord_index)
        __parc_index = self.par_input.get()
        self.database.set_par_index(__parc_index)
        __date = self.date_input.get()
        self.database.set_date(__date)
        __nr = self.days_input.get()
        self.database.set_days_nr(__nr)
        __nr_cars = self.nr_cars_input.get()
        self.database.set_cars_nr(__nr_cars)
        i = 1
        for rec in self.Cars:
            if i > self.database.cars_nr:
                break
            __tmp = list()
            __tmp.append(i)
            __tmp += [(x.get()) for x in rec[1:]]
            self.database.set_car(*__tmp)
            i += 1
        with open(self.PATH_TO_DATABASE, 'wb') as output:
            __database = self.database
            for el in __database.cars:
                print(el)
            pickle.dump(__database, output)


    def execute(self):
        logger.debug("Starting generating the data...")
        if not self.database.is_valid:
            logger.error("Datele sunt incorecte, introduceti din nou")
            return
        for car in self.database.cars:
            car.create_dir(self.PATH)
        self.generate_parcurs()
        self.generate_borderou()
        # todo implement further

    def generate_borderou(self):
        __bord_index = self.database.bord_index
        __date = self.database.start_date
        __wb = self.borderou_template
        for _day in range(self.database.days_nr):
            i = 0
            for _car in self.database.cars:
                if i == 0:
                    self.change_direction_borderou(__wb, self.DIRECTION_1)
                if i == 6:
                    self.change_direction_borderou(__wb, self.DIRECTION_2)
                if i == 12:
                    self.change_direction_borderou(__wb, self.DIRECTION_3)
                self.set_car_name_borderou(__wb, _car)
                self.set_driver_name_borderou(__wb, _car)
                self.change_date_borderou(__wb, __date)
                self.change_index_borderou(__wb, __bord_index)
                __wb.save(_car.dir + "/" + str('borderou') + str(_day + 1) + ".xlsx")
                __bord_index += 1
            __date.next_day()

    def generate_parcurs(self):
        __parc_index = self.database.parc_index
        __date = self.database.start_date
        __wb = self.parcurs_template
        for _day in range(self.database.days_nr):
            i = 0
            for _car in self.database.cars:
                if i == 0:
                    self.change_direction_parcurs(__wb, self.DIRECTION_1)
                if i == 6:
                    self.change_direction_parcurs(__wb, self.DIRECTION_2)
                if i == 12:
                    self.change_direction_parcurs(__wb, self.DIRECTION_3)
                self.set_car_name_parcurs(__wb, _car)
                self.set_driver_name_parcurs(__wb, _car)
                self.change_date_parcurs(__wb, __date)
                self.change_index_parcurs(__wb, __parc_index)
                __wb.save(_car.dir + "/" + str('parcurs') + str(_day + 1) + ".xlsx")
                __parc_index += 1
            __date.next_day()

    @staticmethod
    def change_direction_parcurs(wb, direction):
        __sheet = wb['Parcurs']
        __sheet['C17'].value = direction

    @staticmethod
    def set_driver_name_parcurs(wb, car):
        __sheet = wb['Parcurs']
        __sheet['B14'] = car.driver_name

    @staticmethod
    def change_date_parcurs(wb, date):
        __sheet = wb['Parcurs']
        __sheet['H7'].value = date.display()

    @staticmethod
    def change_index_parcurs(wb, code):
        __sheet = wb['Parcurs']
        __sheet['L14'].value = code

    @staticmethod
    def set_car_name_parcurs(wb, car):
        __sheet = wb['Parcurs']
        __sheet['L8'].value = str(car.series) + "   " + str(car.name)

    @staticmethod
    def change_direction_borderou(wb, direction):
        __sheet = wb['Borderou']
        __sheet['C8'].value = direction
        __sheet['C27'].value = direction

    @staticmethod
    def set_driver_name_borderou(wb, car):
        __sheet = wb["Borderou"]
        __sheet["E7"].value = car.driver_name

    @staticmethod
    def change_date_borderou(wb, date):
        __sheet = wb['Borderou']
        __date = date.display().split()

        __sheet['E3'].value = __date[0]
        __sheet["G3"].value = __date[1]
        __sheet["J3"].value = __date[2][2:]

        __sheet["G22"].value = __date[0]
        __sheet["H22"].value = __date[1]
        __sheet["K22"].value = __date[2][2:]

    @staticmethod
    def change_index_borderou(wb, index):
        __sheet = wb['Borderou']
        __sheet["I6"].value = index
        __sheet["G27"].value = index

    @staticmethod
    def set_car_name_borderou(wb, car):
        __sheet = wb["Borderou"]
        __sheet["E7"] = car.name







def main():
    logging.basicConfig(level=logging.DEBUG)
    print("Engine main started")
    root = Tk()
    app = Engine(root)
    logger.info('Program started')
    app.mainloop()


if __name__ == "__main__":
    main()