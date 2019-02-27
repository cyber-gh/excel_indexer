import datetime
from ui_interface import logger
import os
from time import sleep


class DataRec(object):

    def __init__(self):
        self.bord_index = 1
        self.parc_index = 1
        self.days = 7


class CarRecord(object):

    def __init__(self, index=1, name='', series='', driver_name='', miss_dates=()):
        self.index = index
        self.name = name
        self.series = series
        self.driver_name = driver_name
        self.miss_dates = miss_dates
        self.direction =''
        self.is_valid = True
        self.used = False
        self.dir = ''

    def __repr__(self):
        return (str(self.index) + "  " + str(self.name) + "  " + str(self.series) +
                "  " + str(self.driver_name))

    def create_dir(self, path):
        complete_path = path + '/' + str(self.index) + " " + self.name
        if not os.path.exists(complete_path):
            os.makedirs(complete_path)
        self.dir = complete_path

    def print_parcurs(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.dir):
            files.extend(filenames)
            break
        parcurs_fiels = [file for file in files if 'parcurs' in file]
        parcurs_fiels.sort()
        for file in parcurs_fiels:
            os.startfile(self.dir + "\\" + file, 'print')
            sleep(1)

    def print_borderou(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.dir):
            files.extend(filenames)
            break
        parcurs_fiels = [file for file in files if 'borderou' in file]
        parcurs_fiels.sort()
        for file in parcurs_fiels:
            os.startfile(self.dir + "\\" + file, 'print')
            sleep(1)


class Date(datetime.date):

    def __init__self(self, year, month, day):
        super().__init__(year, month, day)

    def next_day(self):
        curr = self
        curr += datetime.timedelta(days=1)
        return Date(curr.year, curr.month, curr.day)

    @staticmethod
    def string_to_default(s):
        __tmp = list()
        splitter = ''
        for el in s:
            if not el.isdigit():
                splitter = el
                break
        for el in s.split(splitter):
            if el.isdigit():
                __tmp.append(int(el))
        if len(__tmp) != 3:
            raise Exception("Eroare la convertirea datei")
        return __tmp

    def display(self):
        months = {
            1: 'Ianuarie',
            2: 'Februarie',
            3: 'Martie',
            4: 'Aprilie',
            5: 'Mai',
            6: 'Iunie',
            7: 'Iulie',
            8: 'August',
            9: 'Septembrie',
            10: 'Octombrie',
            11: 'Noiembrie',
            12: 'Decembrie'

        }
        return "%02d %s %d" % (self.day, months[self.month], self.year)


class EngineRecord(object):
    def __init__(self):
        self.bord_index = 1
        self.parc_index = 1
        self.bord_index_miss_dates = []
        self.parc_index_miss_dates = []
        self.start_date = Date(2018, 1, 1)
        self.days_nr = 1
        self.cars_nr = 0
        self.cars = list()
        self.is_valid = True

    def set_bord_index(self, s):
        if s.isdigit() and int(s) >= 1:
            self.bord_index = int(s)
            logger.debug("Indexul la borderou a fost setat cu succes")
        else:
            self.is_valid = False
            logger.warning("Indexul la borderoul este invalid")

    def set_bord_index_miss_dates(self, s):
        if not s:
            return

        temp = list(s.split('-'))
        if len(temp) == 2 and temp[0].isdigit() and temp[1].isdigit():
            self.bord_index_miss_dates = [int(x) for x in temp]
            print(temp)
            logger.debug("Indexurile lipsa setate cu success")
        else:
            self.is_valid = False
            logger.warning("Indexruile la data lipsa nu pot fi setate")

    def set_par_index(self, s):
        if s.isdigit() and int(s) >= 1:
            self.parc_index = int(s)
            logger.debug("Indexul la parcurs a fost setat cu succes")
        else:
            self.is_valid = False
            logger.warning("indexul la parcurs este invalid")

    def set_parc_index_miss_dates(self, s):
        if not s:
            return

        temp = list(s.split('-'))
        if len(temp) == 2 and temp[0].isdigit() and temp[1].isdigit():
            self.parc_index_miss_dates = [int(x) for x in temp]
            print(temp)
            logger.debug("Indexurile lipsa setate cu success")
        else:
            self.is_valid = False
            logger.warning("Indexruile la data lipsa nu pot fi setate")

    def set_date(self, s):
        try:
            self.start_date = Date(*Date.string_to_default(s))
        except Exception as ERR:
            logger.warning("Eroare la setarea datei: " + str(ERR))
            self.is_valid = False
        else:
            logger.debug("Data a fost setata cu succes")

    def set_days_nr(self, s):
        if s.isdigit() and int(s) >= 1:
            self.days_nr = int(s)
            logger.debug("nr de zile a fost setat cu succes")
        else:
            self.is_valid = False
            logger.warning("Nr de zile este invalid")

    def set_cars_nr(self, s):
        if s.isdigit() and int(s) >= 0:
            self.cars_nr = int(s)
            logger.debug("nr de masini a fost setat cu succes")
        else:
            self.is_valid = False
            logger.warning("Nr de masini")

    def set_car(self, index, car_name, car_series, driver_name, missing_days, direction):
        __car = CarRecord()
        __car.index = index
        __car.name = car_name
        __car.series = car_series
        __car.direction = direction
        if driver_name == '':
            logger.error("Numele soferului %d este invalid" % index)
            __car.is_valid = False
        if driver_name[0].isupper() and all(x.isalpha() or x == " " for x in driver_name[1:]):
            __car.driver_name = driver_name
        else:
            logger.warning("Eroare la numele soferului: " + str(index))
            __car.is_valid = False
        __tmp = list()
        if not missing_days == '':
            for el in missing_days.split(','):
                if el.isdigit():  # todo implement additional checking according to date limits
                    __tmp.append(int(el))
                else:
                    logger.warning("Eroare in procesarea zilelor libere pentru masina: " + str(index))
                    __car.is_valid = False
            __car.miss_dates = __tmp
        logger.debug("Masina " + str(index) + " a fost procesata")
        self.cars.append(__car)

    def empty(self):
        self.__init__()


if __name__ == "__main__":
    date = Date(2018, 1, 1)
    print(date.display().split())
