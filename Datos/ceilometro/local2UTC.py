import csv
import numpy as np
import datetime
import os
import time

#Reading the -6UTC file
with open('claudio_mlh.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    datetimes = []
    timenums = []
    raws = []
    raws_filtered = []

    for row in readCSV:
        if row[0] == 'Datetime':
            pass
        else:
            d_t = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=6)
            datetimes.append(d_t)
            t_num = time.mktime(d_t.timetuple())
            timenums.append(t_num)


        raws.append(row[1])

        if row[2] == '':
            filtered = row[2].replace('', 'NaN')
            raws_filtered.append(filtered)
        else:
            raws_filtered.append(row[2])

    raws.pop(0)
    raws_filtered.pop(0)

#Dividing and saving the file in month files.
"""
month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dic']

main_dir = '2015_utc/'
os.makedirs(main_dir)
for mm in range(1,13):
    with open(main_dir + month_list[mm-1] + '_2015_utc.dat', 'w') as fout:
        for i in range(0, len(datetimes)):
            if datetimes[i].year == 2015 and datetimes[i].month == mm:
                fout.write(datetime.datetime.strftime(datetimes[i], '%Y-%m-%d-%H:%M:%S') + " " +  str(raws[i]) + " " + str(raws_filtered[i]) + "\n")
"""
#Saving the complete file in UTC

with open('ceilo_2015_UTC_timenum.csv', 'w') as fout:

    for i in range(0, len(datetimes)):
        fout.write(str(timenums[i]) + " " +  str(raws[i]) + " " + str(raws_filtered[i]) + "\n")

with open('ceilo_2015_UTC.csv', 'w') as fout:

    for i in range(0, len(datetimes)):
        fout.write(datetime.datetime.strftime(datetimes[i], '%Y-%m-%d-%H:%M:%S') + "," +  str(raws[i]) + "," + str(raws_filtered[i]) + "\n")
