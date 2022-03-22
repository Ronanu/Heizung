import numpy as np
import csv
import re


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


class InPackage:
    def __init__(self, filename, splitter='-|:|,|T'):
        self.filename = filename
        self.splitter = splitter

    def read_and_split(self):
        with open('feeds.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            data = {}
            for _row in spamreader:
                try:
                    row = re.split(self.splitter, _row[0])
                    year = row[0]
                    month = row[1]
                    date = row[2]
                    time = ':'.join(row[3:6])[:-3]
                    counter = row[7]
                    time_on = float(row[8])
                    # entries.append(Entry(year, month, date, time, counter, time_on))
                    if year not in data.keys():
                        data[year] = dict()
                        data[year]['t'] = 0.
                    if month not in data[year].keys():
                        data[year][month] = {'t': 0.}
                    if date not in data[year][month].keys():
                        data[year][month][date] = {'t': 0.}
                    data[year][month][date][time] = time_on
                    data[year]['t'] += time_on
                    data[year][month]['t'] += time_on
                    data[year][month][date]['t'] += time_on
                except:
                    pass
        return data

import sympy as sp
import sympy.abc as abc

class Oeltank:
    # Dimensionen:
    lx = 3    # m
    ly = 1.5  # m
    lz = abc.h
    vol = lx * ly * lz