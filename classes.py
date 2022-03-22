import numpy as np
import csv

class Monthly:
    def __init__(self, _entry):
        self.month = _entry.month
        self.year = _entry.year
        self.date_begin = _entry.date
        self.date_end = None
        self.time_on = None
        self.days = None
        self.actual_time = None

    def set(self, _times, _date):
        self.date_end = _date
        self.times = _times
        self.time_min = min(_times)
        self.time_max = max(_times)
        self.time_on = sum(_times)
        self.days = self.date_end-self.date_begin+1
        if self.days > 0:
            self.actual_time = 30*self.time_on/self.days
        else:
            self.actual_time = 0

    def set_empty(self, _year, _month):
        self.month = _month
        self.year = _year
        self.date_begin = 0
        self.date_end = 0
        self.time_on = 0
        self.days = 0
        self.actual_time = 0


class Entry:
    def __init__(self, _year, _month, _date, _time, _counter, _time_on):
        self.year = int(_year)
        self.month = int(_month)
        self.date = int(_date)
        self.time = _time
        self.counter = int(_counter)
        self.time_on = float(_time_on)/3600


def in_data():
    with open('feeds.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        entries = list()
        for row in spamreader:
            try:
                year = row[0].split("-")[0]
                month = row[0].split("-")[1]
                date = row[0].split("-")[2]
                time = row[1]
                counter = row[2].split(",")[1]
                time_on = row[2].split(",")[2]
                entries.append(Entry(year, month, date, time, counter, time_on))
            except:
                pass
    return entries


MonthDict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}
