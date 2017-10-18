import scipy.interpolate as interpolate
import numpy as np
import datetime

def compute_height(PH, PHB):

    '''
    compute_height(PH, PHB)

        PH y PHB deben ser prporcionados como una matriz con todas sus dimensiones.

    '''

    g = 9.8
    z_shape = (PH.shape[0], PH.shape[1], PH.shape[2]-1, PH.shape[3], PH.shape[4])
    Z = np.zeros(z_shape, dtype='float32')

    for d in range(0, PH.shape[4]):
        for t in range(0, PH.shape[3]):
            for h in range(0, PH.shape[2]-1):

                Z[:, :, h, t, d] = ((PH[:, : , h, t, d] + PHB[:, :, h, t, d]) + (PH[:, : , h+1, t, d] + PHB[:, :, h+1, t, d]))/(g*2)

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

def compute_vel_promedio(u):

    '''
    compute_vel_promedio(U)

        U deben ser proporcionado como una matriz contodas sus dimensiones.

    '''
    z_shape = (1, u.shape[2], u.shape[3], u.shape[4])
    u_promedio = np.zeros(z_shape, dtype='float32')
    u_std = np.zeros(z_shape, dtype='float32')

    for d in range(0, u.shape[4]):
        for t in range(0, u.shape[3]):
            for h in range(0, u.shape[2]):

                u_promedio[0, h, t, d] = np.average(u[:,:, h, t, d])
                u_std[0, h, t, d] = np.std(u[:,:, h, t, d])

    return u_promedio, u_std

def compute_pblh_promedio(pblh):

    '''
        procjnafa
    '''
    z_shape = (1, pblh.shape[2], pblh.shape[3])
    pblh_promedio = np.zeros(z_shape, dtype='float32')
    pblh_std = np.zeros(z_shape, dtype='float32')

    for d in range(0, pblh.shape[3]):
        for t in range(0, pblh.shape[2]):

            pblh_promedio[0, t, d] = np.average(pblh[:,:, t, d])
            pblh_std[0, t, d] = np.std(pblh[:,:, t, d])

    return pblh_promedio, pblh_std


def import_var_mat(file, station):
    """
    import_var_mat(file, station):
        Imports the variables in a .mat file previously read using scipy.io.loadmat() function.
        The argument station is the name or acronym of the station, it must be a string.
        It returns a directory containing these variables: 'PBLH', 'XLONG', 'U_std', 'V_std', 'HGT', 'V', 'Z', 'V_avg', 'XLAT', 'T', 'T2', 'PHB', 'U', 'U_avg', 'PH'.
    """

    variables = ["PBLH","T","T2","U","V","PH","PHB","HGT","XLAT","XLONG"]#,"XLAT_U","XLONG_U","XLAT_V","XLONG_V"]
    d = {}
    for i in variables:
        d[i] = file["s"][station][0][0][0][0][i]
    d['Z'] = compute_height(d['PH'], d['PHB'])
    #d['U_avg'], d['U_std'] = compute_vel_promedio(d['U'])
    #d['V_avg'], d['V_std'] = compute_vel_promedio(d['V'])
    d['PBLH_avg'], d['PBLH_std'] = compute_pblh_promedio(d['PBLH'])

    return d

def import_var_mat_VC(file):
    """
    import_var_mat(file):
        Imports the variables in a VC .mat file previously read using scipy.io.loadmat() function.
        It returns a directory containing these variables: 'PBLH', 'XLONG','XLAT', 'HGT', 'V', 'U', 'Z' , 'PHB', 'PH'.
    """

    variables = ["PBLH","U","V","PH","PHB","HGT","XLAT","XLONG"]#,"XLAT_U","XLONG_U","XLAT_V","XLONG_V"]
    d = {}
    for i in variables:
        d[i] = file["s"][0][0][0][0][0][i]
    d['Z'] = compute_height(d['PH'], d['PHB'])
    #d['U_avg'], d['U_std'] = compute_vel_promedio(d['U'])
    #d['V_avg'], d['V_std'] = compute_vel_promedio(d['V'])
    #d['PBLH_avg'], d['PBLH_std'] = compute_pblh_promedio(d['PBLH'])

    return d


def read_ceilometro_month(file_path):
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
        raws.append(float(raw))
        filtereds.append(float(filtered))

    filtereds = np.array(filtereds)
    raws = np.array(raws)

    return datetimes, raws, filtereds


def search_hours(hh, DT):
    indexes = []
    for i in range(0, len(DT)):
        if DT[i].hour == hh and DT[i].minute == 0:
            indexes.append(i)
    return indexes

def promedios_mesuales_hora(hh, DT, RAW):

    index_array = search_hours(hh, DT)

    mensuales = []
    mensuales_std = []
    mensuales_hora = []
    mensuales_hora_std = []

    for i in index_array:
        mensuales.append(RAW[i])
        intervalo_hora = []

        for j in range(-3, 4):
            intervalo_hora.append(RAW[i + j])

        mean_hora = np.mean(intervalo_hora)
        std_hora = np.std(intervalo_hora)
        mensuales_hora.append(mean_hora)
        mensuales_hora_std.append(std_hora)


    mean_mesuales = np.mean(mensuales)
    std_mensuales = np.std(mensuales)
    mean_mensuales_hora = np.mean(mensuales_hora)
    std_mensuales_hora = np.mean(mensuales_hora_std)

    return mean_mesuales, std_mensuales, mean_mensuales_hora, std_mensuales_hora

def promedios_mensuales(DT, RAW):
    mes = []
    mes_std = []
    mes_inteval = []
    mes_inteval_std = []
    for h in range(6, 24):
        mean_mm, std_mm, mean_mm_intv, std_mm_intv = promedios_mesuales_hora(h, DT, RAW)
        mes.append(mean_mm)
        mes_std.append(std_mm)
        mes_inteval.append(mean_mm_intv)
        mes_inteval_std.append(std_mm_intv)

    mes = np.array(mes)
    mes_std = np.array(mes_std)
    mes_inteval = np.array(mes_inteval)
    mes_inteval_std = np.array(mes_inteval_std)

    return  [mes, mes_std, mes_inteval, mes_inteval_std]

def promedios_mensuales_wrf(mat_file):
    month = []
    month_std = []
    month_spc = []
    month_spc_std = []

    for h in range(6, 24):

        h_mean = np.mean(mat_file['PBLH'][1,1, h, :])
        h_std = np.std(mat_file['PBLH'][1,1, h, :])
        month.append(h_mean)
        month_std.append(h_std)

        mean_spc_days = []
        std_spc_days = []

        for day in range(0,len(mat_file['PBLH'][0,0,0,:])):

            h_spc_mean = np.mean(mat_file['PBLH'][:,:, h, day])
            h_spc_std = np.std(mat_file['PBLH'][:,:, h, day])
            mean_spc_days.append(h_spc_mean)
            std_spc_days.append(h_spc_std)

        month_spc.append(np.mean(mean_spc_days))
        month_spc_std.append(np.std(std_spc_days))

    month = np.array(month)
    month_std = np.array(month_std)
    month_spc = np.array(month_spc)
    month_spc_std = np.array(month_spc_std)

    return  [month, month_std, month_spc , month_spc_std]

def exportfile(name, ceilo, wrf_24, wrf_48):
    Arr = np.zeros((12, 18))
    Arr[0,:] = ceilo[0]
    Arr[1,:] = ceilo[1]
    Arr[2,:] = ceilo[2]
    Arr[3,:] = ceilo[3]
    Arr[4,:] = wrf_24[0]
    Arr[5,:] = wrf_24[1]
    Arr[6,:] = wrf_24[2]
    Arr[7,:] = wrf_24[3]
    Arr[8,:] = wrf_48[0]
    Arr[9,:] = wrf_48[1]
    Arr[10,:] = wrf_48[2]
    Arr[11,:] = wrf_48[3]

    np.savetxt(name, Arr.T, fmt="%10.3f")
    return Arr.T

def ajuste_lineal(x, a, b):
    return a + b*x
