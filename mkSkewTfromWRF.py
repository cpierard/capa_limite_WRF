import numpy as np
import pymeteo.skewt as skewt

file = 'wrfout_d03_2017-01_19'

lat = 19.2692
lon = -99.7071
time = 1
outFile = 'test'
skewt.plot_wrf(file,lat,lon,time,outFile)


