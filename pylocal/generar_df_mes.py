import importlib.util
spec = importlib.util.spec_from_file_location("bltmat", "/Users/claudiopierard/WRF/bltmat.py")
blt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blt)
import pandas as pd
import numpy as np
import scipy as spy
import scipy.io as sio
import scipy.optimize as optimization
import sys
import os

path2promedios = "/Users/claudiopierard/WRF/Datos/promedios/"
path2ceilo = "/Users/claudiopierard/WRF/Datos/ceilometro/2015_utc/"
path2graficas = "/Users/claudiopierard/WRF/Graficas/"
path2DataFrames = "/Users/claudiopierard/WRF/Datos/Dataframes/"
path2wrf = "/Users/claudiopierard/WRF/Datos/WRF/"
months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
          'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'}

def E1or30(month):
    if month in ['jan', 'mar', 'may', 'jul', 'aug', 'oct', 'dic']:
        return '31'
    elif  month in ['apr', 'jun', 'sep', 'jul', 'nov']:
        return '30'
    elif month == 'feb':
        return '28'

h_i = "00:00:00"
h_f = "23:50:00"
h_f_wrf = "23:00:00"


print('***START***')
sys.argv.pop(0) #Elimina el nombre del script de la lista de argumentos

for mm in sys.argv: #La lista de argumentos contiene los nombres de los archivos a convertir. Para todos los archivos has esto:
    #ceilometro

    date_i = '2015-' + months[mm] + '-01' + ' ' + h_i
    date_f = '2015-' + months[mm] + '-' + E1or30(mm) + ' ' + h_f
    date_f_wrf = '2015-' + months[mm] + '-' + E1or30(mm) + ' ' + h_f_wrf

    month_ceilo_df = pd.read_csv(path2ceilo + mm + '_2015_utc.dat', sep=' ', index_col=0, names=['Raw', 'Filtered'])
    month_ceilo_df.index = pd.to_datetime(month_ceilo_df.index)
    new_index = pd.date_range(date_i, date_f, freq='10Min')
    if mm == 'apr':
        month_ceilo_df = month_ceilo_df[~month_ceilo_df.index.duplicated(keep='first')]

    month_ceilo_df = month_ceilo_df.reindex(new_index)

    #wrf

    file_mm_24 = sio.loadmat(path2wrf +  mm + '/' + months[mm] + '_24hrs_D2.mat')
    month_24 = blt.import_var_mat(file_mm_24, 'Atmos')
    file_mm_48 = sio.loadmat(path2wrf +  mm + '/' + months[mm] + '_48hrs_d2.mat')
    month_48 = blt.import_var_mat(file_mm_48, 'Atmos')

    if mm == 'dic': # WRF month_t_range
        BEG = pd.date_range('2015-12-01 00:00:00', '2015-12-21 23:00:00', freq='1H')
        ENDD = pd.date_range('2015-12-23 00:00:00', '2015-12-31 23:00:00', freq='1H')
        month_t_range = BEG.union(ENDD)

    elif mm == 'jun':
        BEG = pd.date_range('2015-06-01 00:00:00', '2015-06-11 23:00:00', freq='1H')
        ENDD = pd.date_range('2015-06-13 00:00:00', '2015-06-30 23:00:00', freq='1H')
        month_t_range = BEG.union(ENDD)

    elif mm == 'apr':
        month_t_range = pd.date_range('2015-04-02 00:00:00', '2015-04-30 23:00:00', freq='1H') ##Falta esta fechas

    elif mm == 'sep':
        BEG = pd.date_range('2015-09-01 00:00:00', '2015-09-03 23:00:00', freq='1H')
        ENDD = pd.date_range('2015-09-05 00:00:00', '2015-09-30 23:00:00', freq='1H')
        month_t_range = BEG.union(ENDD)

    else:
        month_t_range = pd.date_range(date_i, date_f_wrf, freq='1H')

    wrf_df = blt.wrf2dataframe(month_24, month_48, month_t_range)
    new_index_wrf = pd.date_range(date_i, date_f_wrf, freq='1H')

    wrf_df = wrf_df.reindex(new_index_wrf)

    #Concatenating Dataframes

    B = month_ceilo_df.asfreq('1H')
    A = wrf_df
    C = month_ceilo_df.rolling(window=7, center=True).mean().asfreq('1H')
    C.columns = ['Raw_mean', 'Filt_mean']
    Month_data = pd.concat([A,B,C], axis=1)

    #Saving the dataframe to cvs.
    Month_data.to_csv(path2DataFrames + mm + '_dataframe.csv', float_format='%.3f')

    print(mm + ' -- SAVED')

print('***DONE***')
