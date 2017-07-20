import scipy.interpolate as interpolate
import numpy as np

def interpolate_velocity(XLONG, XLAT, XLONG_U, XLAT_U, U, uu = True, Kind = 'linear'):

    '''
    interpolate_velocity(XLONG, XLAT, XLONG_U, XLAT_U, U, uu = True, Kind = 'linear')

        `XLON`, `XLAT`, `XLONG_U`, `XLAT_U`...  van con su dimensión temporal.
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

            Z[t, h, :, :] = ((PH[t, h, :, :] + PHB[t, h, :, :]) + (PH[t, h+1, :, :] + PHB[t, h+1, :, :]))/g

    return Z

def compute_Richardson(T_s, θ, Z, u, v):

    '''
        compute_Richardson(T_s, θ, Z, u, v):
            Especificar tiempo y localización.

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
