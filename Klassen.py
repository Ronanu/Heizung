import csv
import re
from datetime import datetime
import statistics
import numpy as np

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
            if nmonth == max_months + 1:
                nmonth = 1
                nyear = self.year + 1
        else:
            nday = self.day + 1
            nmonth = self.month
            nyear = self.year

        self.year, self.month, self.day = nyear, nmonth, nday
        return nyear, nmonth, nday

    def get_date_diff(self, date: list):
        for i in range(3000):
            next_date = self.get_date_increment()
            if all(date[j] == next_date[j] for j in range(3)):
                return i + 1
        raise IOError('date_diff not found')


class InPackage:
    data = None
    data_median = None

    def __init__(self, filename='feeds.csv', splitter='-|:|,|T'):
        self.filename = filename
        self.splitter = splitter

    def read_and_split(self):

        def in_to_dict(data, date, time_on):
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

        def init_data_dict(start_date):
            curr_date = datetime.today().strftime('%Y-%m-%d')
            curr_date = [int(d) for d in curr_date.split('-')]
            cnt = DayCounter(y=start_date[0], m=start_date[1], d=start_date[2])
            date = start_date
            data = {}
            for i in range(3000):
                data = in_to_dict(data, date, 0.)
                date = cnt.get_date_increment()
                if all(d == c for d, c in zip(date, curr_date)):
                    break
            if i > 2900:
                raise IOError('Enddate not found')
            return data

        with open('feeds.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            data = None
            for _row in spamreader:
                try:
                    row = re.split(self.splitter, _row[0])
                    year = int(row[0])
                    month = int(row[1])
                    day = int(row[2])
                    time = ':'.join(row[3:6])[:-3]
                    counter = row[7]
                    time_on = float(row[8])
                    date = [year, month, day]

                    if data is None:
                        data = init_data_dict(date)
                    data = in_to_dict(data, date, time_on)

                except:
                    pass
        self.data = data
        return data

    def median_missing_links(self):
        years = sorted(self.data.keys())
        months = sorted(MonthDict.keys())
        data_median = {m: {d: 0. for d in range(MonthDict[m][1])} for m in months}

        for m in months:
            for d in range(MonthDict[m][1]):
                daydata = []
                for y in years:
                    try:
                        daytime = self.data[y][m][d+1]['t']
                        if not daytime == 0.:
                            daydata.append(daytime)
                    except:
                        pass
                if bool(daydata):
                    data_median[m][d] = statistics.median(daydata)
        self.data_median = data_median
        return data_median



if __name__ == '__main__':
    y, m, d = 2018, 12, 30
    inpt = DayCounter(y=y, m=m, d=d)
    diff = inpt.get_date_diff([2019, 4, 6])

    inpt = InPackage()
    data = inpt.read_and_split()
    data_median = inpt.median_missing_links()
    print(data)

