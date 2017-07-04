'''

    `XLON`, `XLAT`, ...  van con su dimensión temporal.
    `U` no va con su dimensión temporal, sólo las dimensiones espaciales correspondientes a un tiempo.
    `ej: U[1, :, :, :]`

'''


def interpolate_velocity(XLONG, XLAT, XLONG_U, XLAT_U, U, u = True, Kind = 'linear'):

    x_old = XLONG_U[0, 1, :]
    y_old = XLAT_U[0, :, 1]
    x_new = XLONG[0, 1, :]
    y_new = XLAT[0, :, 1]

    if u == True:
        u_shape = (U.shape[0], U.shape[1], U.shape[2]-1)

    else:
        u_shape = (U.shape[0], U.shape[1] - 1, U.shape[2])


    U_out = np.zeros(u_shape, dtype='float32')
    #U_out = np.zeros(u_shape, dtype='float32')

    for h in range(0, U.shape[0]):

        f = interpolate.interp2d(x_old, y_old, U[h, :, :], kind = Kind)
        U_out[h, :, :] = f(x_new, y_new)

    return U_out

'''
    compute_height(PH, PHB)

    PH y PHB deben ser prporcionados como una matriz de tres dimensiones es decir hay especificar su variable temporal.
    Por ejemplo: Para el tiempo t = 0, se debe introducir PH[0, :, :, :] y PHB[0, :, :, :].
'''

def compute_height(PH, PBH):

    g = 9.8
    z_shape = (PH.shape[0]-1, PH.shape[1], PH.shape[2])
    Z = np.zeros(z_shape, dtype='float32')


    for h in range(0, PH.shape[0]-1):

        Z[h, :, :] = ((PH[h, :, :] + PBH[h, :, :]) + (PH[h+1, :, :] + PBH[h+1, :, :]))/g

    return Z

def compute_Richardson(T_s, θ, Z, u, v):
    g = 9.8
    Ri = np.zeros(Z.shape, dtype='float32')

    for i in range(1,len(θ)-2):

        Vu = np.sqrt(u[i+1]**2 + v[i+1]**2)
        Vd = np.sqrt(u[i-1]**2 + v[i-1]**2)

        Ri[i] = g / T_s * ((θ[i+1] - θ[i-1])*(Z[i+1] - Z[i-1]))/(Vu - Vd)**2

    return Ri
