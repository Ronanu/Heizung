import csv
import re


MonthDict = {
    1: ["January", 31],
    2: ["February", 30],
    3: ["March", 31],
    4: ["April", 30],
    5: ["May", 31],
    6: ["June", 30],
    7: ["July", 31],
    8: ["August", 31],
    9: ["September", 30],
    10: ["October", 31],
    11: ["November", 30],
    12: ["December", 31]
}


class DayCounter:
    year = None
    month = None
    day = None

    def __init__(self, y, m, d):
        self.year, self.month, self.day = y, m, d

    def get_date_increment(self):
        max_months = 12
        max_days = MonthDict[self.month][1]
        d_hash = self.day % max_days
        if d_hash < self.day:
            nday = 1
            nmonth = self.month + 1
            nyear = self.year
            if nmonth == 13:
                nmonth = 1
                nyear = self.year + 1
        else:
            nday = self.day + 1
            nmonth = self.month
            nyear = self.year

        self.year, self.month, self.day = nyear, nmonth, nday
        return nyear, nmonth, nday




class InPackage:
    def __init__(self, filename='feeds.csv', splitter='-|:|,|T'):
        self.filename = filename
        self.splitter = splitter

    def read_and_split(self):

        def in_to_dict(date, data, time_on):
            year, month, day = date
            if year not in data.keys():
                data[year] = dict()
                data[year]['t'] = 0.
            if month not in data[year].keys():
                data[year][month] = {'t': 0.}
            if day not in data[year][month].keys():
                data[year][month][day] = {'t': 0.}
            data[year][month][day][time] = time_on
            data[year]['t'] += time_on
            data[year][month]['t'] += time_on
            data[year][month][day]['t'] += time_on
            return data

        with open('feeds.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            data = {}
            date_counter = None
            for _row in spamreader:
                try:
                    row = re.split(self.splitter, _row[0])
                    year = row[0]
                    month = int(row[1])
                    day = int(row[2])
                    time = ':'.join(row[3:6])[:-3]
                    counter = row[7]
                    time_on = float(row[8])
                    date = [year, month, day]

                    if date_counter is None:
                        date_counter = DayCounter(y=int(year), m=month, d=day)
                        next_date = [year, month, day]
                    else:
                        next_date = date_counter.get_date_increment()

                    while True:
                        if all(date[i] == date[i] for i in range(3)):
                            break
                        elif all(date[i] == next_date[i] for i in range(3)):
                            break
                        else:
                            next_date = date_counter.get_date_increment()
                            data = in_to_dict(next_date, data, time_on)
                            print(next_date)

                    data = in_to_dict(date, data, time_on)

                except:
                    pass
        return data


if __name__ == '__main__':
    y, m, d = 1995, 12, 30
    inpt = DayCounter(y=y, m=m, d=d)
    for i in range(400):
        print(inpt.get_date_increment())

    _in = InPackage()
    _in.read_and_split()