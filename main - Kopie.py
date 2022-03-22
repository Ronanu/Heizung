import classes


if __name__ == "__main__":
    datareader = classes.InPackage
    data = datareader.read_and_split()

    fig = plt.figure()
    years = sorted(data.keys())
    plt.bar(years, [data[year]['t'] for year in years])
    plt.show()

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

    measure_time = sum(time)*1
    Leistung_measure = 0 #Energie_nutz/measure_time
    oil_per_time = Vol_Öl/measure_time

    print("Öl pro Zeit:  " + str(round(oil_per_time, 4)) + " l/h")
    print("Leistung aus Messung:  " + str(round(Leistung_measure, 1)) + "kW")

