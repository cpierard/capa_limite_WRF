import scipy.interpolate as interpolate
import numpy as np
import datetime

def interpolate_velocity(XLONG, XLAT, XLONG_U, XLAT_U, U, uu = True, Kind = 'linear'):

    '''
    interpolate_velocity(XLONG, XLAT, XLONG_U, XLAT_U, U, uu = True, Kind = 'linear')

        `XLON`, `XLAT`, `XLONG_U`, `XLAT_U, U` van con su dimensión temporal.
        `U` va con su dimensión temporal.
        `uu` define si se trata de velocidad zonal o meridional, es decir si se está interpolando 'u', uu = True.
        `Kind`, tipo de interpolación. Por default es linear.

        ej:
            interpolate_velocity(xlong, xlat, xlong_v, xlat_v, v, uu = False)

    '''

    x_old = XLONG_U[0, 1, :]
    y_old = XLAT_U[0, :, 1]
    x_new = XLONG[0, 1, :]
    y_new = XLAT[0, :, 1]

    if uu == True:
        u_shape = (U.shape[0], U.shape[1], U.shape[2], U.shape[3]-1)

    else:
        u_shape = (U.shape[0], U.shape[1] ,U.shape[2] - 1, U.shape[3])


    U_out = np.zeros(u_shape, dtype='float32')
    #U_out = np.zeros(u_shape, dtype='float32')

    for t in range(0, U.shape[0]):
        for h in range(0, U.shape[1]):

            f = interpolate.interp2d(x_old, y_old, U[t, h, :, :], kind = Kind)
            U_out[t, h, :, :] = f(x_new, y_new)

    return U_out

def compute_height(PH, PHB):

    '''
    compute_height(PH, PHB)

        PH y PHB deben ser prporcionados como una matriz de 4 dimensiones es decir no hay especificar su variable temporal.

    '''

    g = 9.8
    z_shape = (PH.shape[0], PH.shape[1]-1, PH.shape[2], PH.shape[3])
    Z = np.zeros(z_shape, dtype='float32')

    for t in range(0, PH.shape[0]):
        for h in range(0, PH.shape[1]-1):

            Z[t, h, :, :] = ((PH[t, h, :, :] + PHB[t, h, :, :]) + (PH[t, h+1, :, :] + PHB[t, h+1, :, :]))/(g*2)

    return Z

def compute_Richardson(T_s, θ, Z, u, v):

    '''
    compute_Richardson(T_s, θ, Z, u, v):
        OUT: Ri

        T_s = Temperatura superficial
        θ = Temperatura potencial. Tiene que ser un arreglo 1d con una temperatura potencial por cada nivel.
        Z = Arreglo con las alturas para una ubicación.
        u = Arreglo de 1d con los vientos u en cada nivel.
        v = Arreglo de 1d con los vientos v en cada nivel.

        Ri = un arreglo con las mismas dimensiones que Z, con los Richardson calculados para cada altura.

    '''

    g = 9.8
    Ri = np.zeros(Z.shape, dtype='float32')

    for i in range(1,len(θ)-2):

        Vu = np.sqrt(u[i+1]**2 + v[i+1]**2)
        Vd = np.sqrt(u[i-1]**2 + v[i-1]**2)

        Ri[i] = g / T_s * ((θ[i+1] - θ[i-1])*(Z[i+1] - Z[i-1]))/(Vu - Vd)**2

    return Ri


def compute_Richardson_2(θ, Z, u, v):

    '''
        compute_Richardson_2(θ, Z, u, v):
            Especificar tiempo y localización
    '''

    g = 9.8
    Ri = np.zeros(Z.shape, dtype='float32')

    for i in range(0,len(θ)-1):

        Ri[i] = (g*(θ[i] - θ[0])*(Z[i] - Z[0]))/(θ[i] * (u[i]**2 + v[i]**2))

    return Ri

def near_coord(xlong, xlat, loclong, loclat):

    '''
        near_coord(xlong, xlat, loclong, loclat)
        OUT: nx, ny

            Busca los índices más cercanos a una coordenada.

    '''

    distlog = np.abs(xlong[0,0,:] - loclong)
    distlat = np.abs(xlat[0,:,0] - loclat)
    nx = 0
    ny = 0

    for i in range(0, len(xlong[0,0,:])):

        if distlog[i] < distlog[ny]:
            ny = i

    for j in range(0, len(xlat[0,:,0])):

        if distlat[j] < distlat[nx]:
            nx = j

    return nx, ny

def detecta_PBL(Ri, Z, Ric):

    '''
        detecta_PBL(Ri, Z, Ric):
            OUT: n, z

            Decta el índice de la primera capa donde el gradiente es igual al valor crítico. n es el índice y z es la atura donde está la capa límite.
            Ri = perfil vertical de Richardon.
            Z = alturas para una coordenada
            Ric = valor crítico de Richardson. Usualmente es 0.21.
    '''

    n = 0

    for i in range(0,len(Ri)-1):

        if Ri[i] < Ric and Ri[i+1] > Ric:
            n = i
            break
        elif Ri[i] > Ric and Ri[i+1] < Ric:
            n = i
            break

    print('Capa límite: ', Z[i], '. Ínidce: ', n)
    return n, Z[n]

def detecta_PBL_indices(Ri, Z, Ric):

    '''
        detecta_PBL_indices(Ri, Z, Ric):
            OUT: n

            Decta el conjunto de índices donde el gradiente es igual al valor crítico. n es un arreglo que contiene todos los índices.
            Ri = perfil vertical de Richardon.
            Z = alturas para una coordenada
            Ric = valor crítico de Richardson. Usualmente es 0.21.
    '''

    n = []

    for i in range(0,len(Ri)-1):

        if Ri[i] < Ric and Ri[i+1] > Ric:
            n.append(i)

        elif Ri[i] > Ric and Ri[i+1] < Ric:
            n.append(i)

        elif Ri[i] == 0.21:
            n.append(i)
            print('índice ', i, ' == ', Ric)

    #print('Capa límite: ', Z[i], '. Ínidce: ', n)
    return n #, Z[n]

class region:
    """
    Declares a new class specific for geografical polygons. The main purpose is to locate which points in a grid are inside of the polygon.
    ATRIBUTES:
        self.lon: Is an array with all the longitudinal coordinates of the polygon.
        self.lat: Is an array with all the latitude coordinates of the polygon.
        self.max_lon: gives the max longitud of the polygon.
        self.max_lat: gives the max longitud of the polygon.
        self.min_lon: gives the min longitud of the polygon.
        self.min_lat: gives the min longitud of the polygon.
        self.name: Is the name of the region, in a string.
        self.nx: All the x indices
        self.ny:
    """
    def __init__(self):
        self.lon = None
        self.lat = None
        self.max_lon = None
        self.max_lat = None
        self.min_lon = None
        self.min_lat = None
        self.name = None
        self.nx = None
        self.ny = None

def read_region(region, f):
    """
    read_region(region, f):
        The function reads an .txt file and fills up its attributes, except region.nx and region.ny.
        'region' is an object class region, previously declared as region(). f is the file location, it must be a string.

    """
    n = f.find('.')
    region.name = f[0:n]
    R=open(f,'r')
    lon=[]
    lat=[]
    for line in R:
        if '>' in line:
            pass
        else:
            lon.append(float(line.split()[0]))
            lat.append(float(line.split()[1]))
    region.lon=np.array(lon)
    region.lat=np.array(lat)
    region.max_lon = max(region.lon)
    region.max_lat = max(region.lat)
    region.min_lon = min(region.lon)
    region.min_lat = min(region.lat)

def in_or_out(region, x, y):
    """
    in_or_out(region, x, y):
        Checks if the point x and y, is inside of the polygon region. The polygon must be an object class region.
        OUT: boolean.
    """
    crossings = 0
    for i in range(0,len(region.lon)-1):
        if x < region.lon[i] and x < region.lon[i+1] or x > region.lon[i] and x > region.lon[i+1]:
            pass

        elif y > region.lat[i] and y > region.lat[i+1]:
            pass

        elif y < region.lat[i] and y < region.lat[i+1]:
            if x < region.lon[i] and x > region.lon[i+1] or x > region.lon[i] and x < region.lon[i+1]:
                crossings += 1

        elif y > region.lat[i] and y < region.lat[i+1]:
            if x > region.lon[i] and x < region.lon[i+1]:
                y_c = region.lat[i] + (region.lat[i+1] - region.lat[i])*(x - region.lon[i])/(region.lon[i+1] - region.lon[i])
                if y_c > y:
                    crossings += 1

        elif y < region.lat[i] and y > region.lat[i+1]:
            if x < region.lon[i] or x > region.lon[i+1]:
                y_c = region.lat[i+1] + (region.lat[i] - region.lat[i+1])*(x - region.lon[i+1])/(region.lon[i] - region.lon[i+1])
                if y_c > y:
                    crossings += 1

    if crossings % 2 == 0:
        return False

    elif crossings % 2 != 0:
        return True

def points_in_region(region, x_long, x_lat):
    """
    points_in_region(region, x_long, x_lat):
        Looks for the points inside a polygon. 'region' is the polygon it must be an object region.
        x_long is an array containing all the longitud coordinates of the grid.
        x_lat is an array containing all the latitud coordinates of the grid.
            OUT: nothing. It appends the nx and ny indices of the points inside of the polygon to the atribitute region.nx and region.ny .
    """
    nx = []
    ny = []
    for i in range(0,29):
        for j in range(0,29):
            if blt.in_or_out(region, x_long[i,j], x_lat[i,j]) == True:
                nx.append(i)
                ny.append(j)
    #return nx, ny
    region.nx = nx
    region.ny = ny

def import_var_mat(file, station):
    """
    import_var_mat(file, station):
        Imports the variables in a .mat file previously read using scipy.io.loadmat() function.
        The argument station is the name or acronym of the station, it must be a string.
        It returns a directory containing all the arrays.
    """


    variables = ["PBLH","T","T2","U","V","PH","PHB","HGT","XLAT","XLONG"]#,"XLAT_U","XLONG_U","XLAT_V","XLONG_V"]
    d = {}
    for i in variables:
        d[i] = file["s"][station][0][0][0][0][i]

    return

def read_celiomentro_month(file_path):
    """
    read_celiomentro_month(file_path)
         OUT: datetime format array, pblh_raw, pblh_filtered
    Is a function that imports data of the ceilometer data per month. You can find the data in the
    folder Datos/ceilometro/215_utc.
    """
    datetimes = []
    raws = []
    filtereds = []
    file = open(file_path, 'r')
    for line in file:
        date, raw, filtered = line.split()
        date = datetime.datetime.strptime(date, '%Y-%m-%d-%H:%M:%S')
        datetimes.append(date)
        raws.append(raw)
        filtereds.append(filtered)

    filtereds = np.array(filtereds)
    raws = np.array(raws)
    return datetimes, raws, filtereds
