# Capa límite de salidas WRF

### To do list:

- [x] Interpolación velocidades.
- [x] Cálculo de altura.
- [x] Algoritmo para calcular número de Richardson.
- [x] Gráfica 1:1 (de calibración)
- [ ] Script para extraer datos de interés.
- [ ] ...

Los avances se encuentran en el `jupyter notebook` que se llama `Calculo_Richardson.ipynb`.

`BoundaryLayerToolbox.py` intentará ser un módulo con todas las funciones necesarias para trabajar en el análisis de capa límite.

`Pruebas_netCDF4.ipynb` es un cuaderno que está muy desordenado y tiene un montón de pruebas fallidas.

`mkSkewTfromWRF.py` es un radiosondeo virtual que usa el paquete `pymeteo`.
