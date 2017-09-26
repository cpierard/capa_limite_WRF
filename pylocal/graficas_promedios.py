
import importlib.util
spec = importlib.util.spec_from_file_location("bltmat", "/Users/claudiopierard/WRF/bltmat.py")
blt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blt)
import numpy as np
import scipy as spy
import scipy.io as sio
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
path2wrf = "/Users/claudiopierard/WRF/Datos/WRF/"
months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
          'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'}

print('***START***')
sys.argv.pop(0) #Elimina el nombre del script de la lista de argumentos

for mm in sys.argv: #La lista de argumentos contiene los nombres de los archivos a convertir. Para todos los archivos has esto:
    print('Graficando', mm)
    # **Extraer datos**
    month_avg = np.loadtxt(path2promedios + mm + "_promedios.dat")
    path_month_graficas = path2graficas + mm + '_graficas/'
    os.makedirs(path_month_graficas)

    plt.rcParams.update({'font.size': 13}) #Tamaño letra

    # 24h
    os.makedirs(path_month_graficas + '24h')
    ## Gráfica de ceilo en cada hora  y PBLH en coordenada más cercana al CCA

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    plt.fill_between(h_range, month_avg[:,0] - month_avg[:,1], month_avg[:,0] + month_avg[:,1], facecolor='#F0F8FF', alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,0], label = 'LIDAR')
    plt.fill_between(h_range, month_avg[:,4] - month_avg[:,5], month_avg[:,4] + month_avg[:,5], facecolor= h24_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,4], c = 'g', label='PBLH 24h')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))

    plt.savefig(path_month_graficas + '24h/' + mm + '_cei_hora_pblh_cca')



    ## Gráfica de ceilo en pormediado en el intervalo  y PBLH coordenada más cercana al CCA

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    plt.fill_between(h_range, month_avg[:,2] - month_avg[:,3], month_avg[:,2] + month_avg[:,3], facecolor='#F0F8FF', alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,2], label = 'LIDAR')
    plt.fill_between(h_range, month_avg[:,4] - month_avg[:,5], month_avg[:,4] + month_avg[:,5], facecolor= h24_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,4], c = 'g', label='PBLH 24h')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))
    plt.savefig(path_month_graficas + '24h/' + mm + '_cei_int_pblh_cca')


    ## Gráfica de ceilo en hora y PBLH coordenada más cercana al CCA con promedio espacial

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    plt.fill_between(h_range, month_avg[:,0] - month_avg[:,1], month_avg[:,0] + month_avg[:,1], facecolor='#F0F8FF', alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,0], label = 'LIDAR')
    plt.fill_between(h_range, month_avg[:,6] - month_avg[:,7], month_avg[:,6] + month_avg[:,7], facecolor=h24_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,6], c = 'g', label='PBLH 24h')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))
    plt.savefig(path_month_graficas + '24h/' + mm + '_cei_hora_pblh_esp')


    ## Gráfica de ceilo en pormediado en el intervalo  y PBLH con promedio espacial a coordenada más cercana al CCA

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    plt.fill_between(h_range, month_avg[:,2] - month_avg[:,3], month_avg[:,2] + month_avg[:,3], facecolor='#F0F8FF', alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,2], label = 'LIDAR')
    plt.fill_between(h_range, month_avg[:,6] - month_avg[:,7], month_avg[:,6] + month_avg[:,7], facecolor=h24_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,6], c = 'g', label='PBLH 24h')
    #plt.title('Promedios mensuales, espaciales y temporales en diciembre ')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))
    plt.savefig(path_month_graficas + '24h/' + mm + '_cei_int_pblh_esp')

    # 48 h
    os.makedirs(path_month_graficas + '48h')

    ## ceilo promedio en hora y pblh en 1 coord.

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #ceilo
    plt.fill_between(h_range, month_avg[:,0] - month_avg[:,1], month_avg[:,0] + month_avg[:,1], facecolor=ceilo_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,0], label = 'LIDAR')
    #48h
    plt.fill_between(h_range, month_avg[:,8] - month_avg[:,9], month_avg[:,8] + month_avg[:,9], facecolor=h48_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,8], c = 'r', label='PBLH 48h')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))
    plt.savefig(path_month_graficas + '48h/' + mm + '_cei_hora_pblh_cca')



    ### ceilo promedio 1 h y pblh promedio espacial

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #ceilo
    plt.fill_between(h_range, month_avg[:,0] - month_avg[:,1], month_avg[:,0] + month_avg[:,1], facecolor=ceilo_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,0], label = 'LIDAR')
    #48h
    plt.fill_between(h_range, month_avg[:,10] - month_avg[:,11], month_avg[:,10] + month_avg[:,11], facecolor=h48_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,10], c = 'r', label='PBLH 48h')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))
    plt.rcParams.update({'font.size': 13})
    plt.savefig(path_month_graficas + '48h/' + mm + '_cei_hora_pblh_esp')

    ## ceilo promedio en intervalo de tiempo y pblh en 1 coord.

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #ceilo
    plt.fill_between(h_range, month_avg[:,2] - month_avg[:,3], month_avg[:,2] + month_avg[:,3], facecolor=ceilo_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,2], label = 'LIDAR')
    #48h
    plt.fill_between(h_range, month_avg[:,8] - month_avg[:,9], month_avg[:,8] + month_avg[:,9], facecolor=h48_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,8], c = 'r', label='PBLH 48h')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))
    plt.savefig(path_month_graficas + '48h/' + mm + '_cei_int_pblh_cca')


    ## ceilo promedio en intervalo de tiempo y pblh promedio en el espacio

    h_range= range(6,24)
    plt.figure(figsize=(8,6))
    #plt.plot(h_range, B)
    #ceilo
    plt.fill_between(h_range, month_avg[:,2] - month_avg[:,3], month_avg[:,2] + month_avg[:,3], facecolor=ceilo_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,2], label = 'LIDAR')
    #48h
    plt.fill_between(h_range, month_avg[:,10] - month_avg[:,11], month_avg[:,10] + month_avg[:,11], facecolor=h48_color, alpha=1.0, edgecolor='none')
    plt.plot(h_range, month_avg[:,10], c = 'r', label='PBLH 48h')
    plt.ylabel('Altura (m)')
    plt.xlabel('Hora (UTC)')
    plt.legend(loc=(0.05,0.83))
    plt.savefig(path_month_graficas + '48h/' + mm + '_cei_int_pblh_esp')

print('***DONE***')
