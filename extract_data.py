import numpy as np
from netCDF4 import Dataset

## Extraer datos salida netCDF
A = np.array([1,2],[3,4])

#Guardar archivo .dat .wrf .ri
np.writetxt('arreglo.wrf', A, fmt='%s')

#para importart el archivo haces

B = np.loadtxt('arreglo.wrf')

#FIN
