import importlib.util
spec = importlib.util.spec_from_file_location("bltmat", "/Users/claudiopierard/WRF/bltmat.py")
blt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blt)
import numpy as np
import scipy as spy
import scipy.io as sio
import datetime
import sys
import os

path2promedios = "/Users/claudiopierard/WRF/Datos/promedios/"
path2ceilo = "/Users/claudiopierard/WRF/Datos/ceilometro/2015_utc/"
path2wrf = "/Users/claudiopierard/WRF/Datos/WRF/"
months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
          'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'}

print('***START***')
sys.argv.pop(0) #Elimina el nombre del script de la lista de argumentos

for mm in sys.argv: #La lista de argumentos contiene los nombres de los archivos a convertir. Para todos los archivos has esto:

    print('Extracting', mm, 'file')

    month_dt, month_raw, month_filt = blt.read_ceilometro_month(path2ceilo + mm + "_2015_utc.dat")
    month_ceilo_means = blt.promedios_mensuales(month_dt, month_raw)

    file_month_24 = sio.loadmat(path2wrf + mm + '/' + months[mm] + "_24hrs_D2.mat")
    file_month_48 = sio.loadmat(path2wrf + mm + '/' + months[mm] + "_48hrs_D2.mat")

    month_24 = blt.import_var_mat(file_month_24, 'Atmos')
    month_48 = blt.import_var_mat(file_month_48, 'Atmos')

    month_wrf_means_24 = blt.promedios_mensuales_wrf(month_24)
    month_wrf_means_48 = blt.promedios_mensuales_wrf(month_48)

    blt.exportfile(path2promedios + mm + "_promedios.dat" , month_ceilo_means, month_wrf_means_24, month_wrf_means_48)

print('**DONE**')
