import importlib.util
spec = importlib.util.spec_from_file_location("bltmat", "/Users/claudiopierard/WRF/bltmat.py")
blt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blt)
import numpy as np
import pandas as pd
import scipy as spy
import scipy.io as sio
import matplotlib
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import datetime
import sys
import os

ceilo_color = '#F0F8FF'
h48_color = '#FBC0C0'
h24_color = '#defec8'

path2promedios = "/Users/claudiopierard/WRF/Datos/promedios/"
path2graficas = "/Users/claudiopierard/WRF/Graficas/"
path2DataFrames = "/Users/claudiopierard/WRF/Datos/Dataframes/"
path2wrf = "/Users/claudiopierard/WRF/Datos/WRF/"
months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
          'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'}

keys_24 = ['PBLH_24',  'PBLH_avg_24']
keys_48 = ['PBLH_48', 'PBLH_avg_48']
keys_ceilo = ['Raw', 'Raw_mean']

print('***START***')
sys.argv.pop(0) #Elimina el nombre del script de la lista de argumentos

for mm in sys.argv: #La lista de argumentos contiene los nombres de los archivos a convertir. Para todos los archivos has esto:
    print('Graficando gunshot plots', mm)
    # **Extraer datos**

    month_df = pd.read_csv(path2DataFrames +  mm + "_dataframe.csv", index_col=0)
    month_df.index = pd.to_datetime(month_df.index)
    path2gunshot = path2graficas + mm + "_graficas/gunshot_plots/"
    os.makedirs(path2gunshot)
    os.makedirs(path2gunshot + '24h/')
    os.makedirs(path2gunshot + '48h/')
    #RAW vs keys()

    for key in keys_24:
        for ceilo in keys_ceilo:
            df_temp = pd.DataFrame(month_df, columns=[ceilo, key])
            #fig, ax = plt.subplots(1,1)
            #fig.set_size_inches(7,6)

            # Datos
            x = df_temp[ceilo]  #dic_df.asfreq('1H').between_time('06:00:00', '23:00:00').Raw
            y = df_temp[key]  #dic_wrf_df.between_time('06:00:00', '23:00:00')[key]
            tag = (df_temp.index.hour-6)%24#dic_wrf_df.between_time('06:00:00', '23:00:00').index.hour

            ##Ajuste lineal
            popt, pcov = optimization.curve_fit(blt.ajuste_lineal, df_temp.dropna()[ceilo], df_temp.dropna()[key])

            # define the colormap
            cmap = plt.cm.rainbow #matplotlib.colors.ListedColormap(['black','yellow', 'red', 'blue', 'white', 'green'])
            # extract all colors from the .rainbow map
            cmaplist = [cmap(i) for i in range(cmap.N)]
            # create the new map
            cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
            # define the bins and normalize
            bounds = np.linspace(0,24, 9)
            norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

            # make the scatter
            plt.figure(figsize = (7,6))
            scat = plt.scatter(x,y, cmap=cmap, norm=norm, c=tag, edgecolors='none', s = 35)

            # create a second axes for the colorbar
            #ax2 = plt.add_axes([0.95, 0.1, 0.03, 0.8])
            #cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')

            #Format
            plt.ylim(-100, 3500)
            plt.xlim(-100, 3500)
            plt.xlabel('LIDAR')
            plt.ylabel('PBLH')
            xx = np.linspace(-100, 3500, 10)

            plt.plot(xx, blt.ajuste_lineal(xx, *popt), c = 'k') #plot linear fit
            plt.plot(xx, blt.ajuste_lineal(xx, 0, 1), '--') #Plot identity
            plt.rcParams.update({'font.size': 14})
            plt.title('UTC-6')
            plt.grid()
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(path2gunshot + '24h/' + mm + '_' + ceilo + 'vs' + key + '.png', format='png')

    for key in keys_48:
        for ceilo in keys_ceilo:
            df_temp = pd.DataFrame(month_df, columns=[ceilo, key])
            #fig, ax = plt.subplots(1,1)
            #fig.set_size_inches(7,6)

            # Datos
            x = df_temp[ceilo]  #dic_df.asfreq('1H').between_time('06:00:00', '23:00:00').Raw
            y = df_temp[key]  #dic_wrf_df.between_time('06:00:00', '23:00:00')[key]
            tag = (df_temp.index.hour-6)%24#dic_wrf_df.between_time('06:00:00', '23:00:00').index.hour

            ##Ajuste lineal
            popt, pcov = optimization.curve_fit(blt.ajuste_lineal, df_temp.dropna()[ceilo], df_temp.dropna()[key])

            # define the colormap
            cmap = plt.cm.rainbow #matplotlib.colors.ListedColormap(['black','yellow', 'red', 'blue', 'white', 'green'])
            # extract all colors from the .rainbow map
            cmaplist = [cmap(i) for i in range(cmap.N)]
            # create the new map
            cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
            # define the bins and normalize
            bounds = np.linspace(0,24, 9)
            norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

            # make the scatter
            plt.figure(figsize = (7,6))
            scat = plt.scatter(x,y, cmap=cmap, norm=norm, c=tag, edgecolors='none', s = 35)

            # create a second axes for the colorbar
            #ax2 = plt.add_axes([0.95, 0.1, 0.03, 0.8])
            #cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')

            #Format
            plt.ylim(-100, 3500)
            plt.xlim(-100, 3500)
            plt.xlabel('LIDAR')
            plt.ylabel('PBLH')
            xx = np.linspace(-100, 3500, 10)

            plt.plot(xx, blt.ajuste_lineal(xx, *popt), c = 'k') #plot linear fit
            plt.plot(xx, blt.ajuste_lineal(xx, 0, 1), '--') #Plot identity
            plt.rcParams.update({'font.size': 14})
            plt.title('UTC-6')
            plt.grid()
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(path2gunshot + '48h/' + mm + '_' +ceilo + 'vs' + key + '.png', format='png')


print('***DONE***')
