from classes import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    entries = in_data()
##################################################################################
    # Vergleich mit Kenndaten
    Wirkungsgrad = 0.852
    leistung = 70000  # WE
    leistung = leistung / 860  # umrechnung in kW

    print("Leistung aus Kenndaten: " + str(round(leistung, 1)) + "kW")
##################################################################################
    # Vergleich mit Ölstand

    Vol_Öl = 15 * 30 * (13.7 - 6.85)  # in l
    Heitzwert = 10.9  # kWh/l
    Energie_Öl = Vol_Öl * Heitzwert  # kWh
    Energie_nutz = Energie_Öl * Wirkungsgrad

    d = 6
    m = 10
    j = 2019

    time = list()
    for e in entries:
        if e.date >= d and e.month >= m or e.year > j:
            time.append(e.time_on)

    measure_time = sum(time)*1
    Leistung_measure = Energie_nutz/measure_time
    oil_per_time = Vol_Öl/measure_time

    print("Öl pro Zeit:  " + str(round(oil_per_time, 4)) + " l/h")
    print("Leistung aus Messung:  " + str(round(Leistung_measure, 1)) + "kW")
##################################################################################
    monthly = list()
    monthly.append(Monthly(entries[0]))
    times = list()
    old_date = entries[0].date
    old_month = entries[0].month
    for entry in entries:
        if not(entry.month == old_month):  # neuer Monat:
            monthly[-1].set(times, old_date)  # Monat beenden
            month_counter = old_month
            while not(month_counter % 12 + 1 == entry.month):
                # leere Monate einfügen
                month_counter += 1
                monthly.append(Monthly(entry))
                monthly[-1].set_empty(monthly[-1].year, month_counter)

            monthly.append(Monthly(entry))  # Monat beenden

            times = list()
            old_date = 0
        old_date = entry.date
        old_month = entry.month
        times.append(entry.time_on)
    monthly[-1].set(times, entry.date)

##################################################################################
    # leere Monate interpolieren
    i = 0
    for month in monthly:
        j = i+1
        time_right = 0
        if month.time_on == 0:
            time_left = monthly[i-1].actual_time
            while time_right <= 0:
                time_right = monthly[j].actual_time
                j += 1

            monthly[i].actual_time = (time_left+time_right)/2
        i += 1
##################################################################################
    fig = plt.figure()
    i = 0
    names = list()
    av_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    average_year = dict.fromkeys(av_keys, [])
    for k in av_keys:
        average_year[k] = {'time': 0, 'anz': 0}
    average_year['average'] = {'sum_time': 0, 'sum_oil': 0}
    for month in monthly:
        average_year[str(month.month)]['anz'] += 1
        average_year[str(month.month)]['time'] += month.actual_time
        names.append(MonthDict[month.month])
    for month in monthly:
        plt.bar(i, month.actual_time, width=0.8, color="green")
        plt.bar(i, month.time_on, width=0.4, color="blue")
        i += 1
    i = 1
    for k in av_keys:
        average_year['average']['sum_time'] += average_year[k]['time']/average_year[k]['anz']
        plt.bar(i, average_year[k]['time']/average_year[k]['anz'], width=0.2, color="red")
        i += 1
    average_year['average']['sum_oil'] = average_year['average']['sum_time'] * oil_per_time
    plt.ylabel('Betriebsstunden bezogen auf 30 Tage')
    plt.xticks(np.arange(i), names, rotation=90)
    plt.grid(True)
    print(average_year['average'])
    print('aktueller Ölstand: ' + str(Vol_Öl))
    print(average_year['average']['sum_oil']-Vol_Öl)
    plt.show()


    #i = 0
    #for day in daily:
    #    i += 1
    #    plt.plot(i, day.time_on, 'X')
    #
    #plt.show()