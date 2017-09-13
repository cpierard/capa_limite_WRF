from numpy import genfromtxt,unique,zeros,where,nan,argmin,sqrt,array,r_,isnan
from glob import glob
    
#Leer los resultados de la simulacion
fgmax_file=u'/Users/octavio/WarningMaps/geoclaw_outputs/main/mendoza/fort.FG1.valuemax'
aux_file='/Users/octavio/WarningMaps/geoclaw_outputs/main/mendoza/fort.FG1.aux1'

#Nombre del archivo de salida con los valores RGB para cada municipio
fout='/Users/octavio/WarningMaps/geoclaw_outputs/main/mendoza/warnings/municipios_pacifico_mexico_rgb.warn'

#Varibles del script
wet_tol=0.001 #Valores por debajo de esta cantidad son considerados secos
etaclip=6     #Valores por encima de esta cantidad son puestos a nan	    

#Primero obtener la amplitud maxima de los resultados de la simulacion
lon=genfromtxt(fgmax_file,usecols=0)	#Primer columna del archivo de simulacion fgmax_file (Longitud)
lat=genfromtxt(fgmax_file,usecols=1)	#Segunda columna del archivo de simulacion fgmax_file (Latitud)
amr=genfromtxt(fgmax_file,usecols=2)	#Tercera columna del archivo de simulacion fgmax_file 
H_in=genfromtxt(fgmax_file,usecols=3)   #Cuarta columna del archivo de simulacion fgmax_file
b_in=genfromtxt(aux_file)		#Carga todo el archivo de simulacion aux_file
unique_amr=unique(amr)			#Obtiene los elementos unicos del arreglo amr
eta=zeros(len(H_in))
b=zeros(len(H_in))
H=zeros(len(H_in))
for k in range(len(unique_amr)):
    i=where(amr==unique_amr[k])[0]
    eta[i]=H_in[i]+b_in[i,unique_amr[k]+1]
    H[i]=H_in[i]
    b[i]=b_in[i,unique_amr[k]+1]
i=where(H<wet_tol)[0]
eta[i]=nan
i=where(eta>etaclip)[0]
eta[i]=nan
lat_out=lat
eta_out=eta
lon_out=lon

#Crear una clase llamada region con un metodo para llenarla
class region:
  def __init__(self):
    self.lon = None
    self.lat = None
    self.eta = []
    self.color=None

def read_region(f):
    R=open(f,'r')
    lon=[]
    lat=[]
    for line in R:
        if '>' in line:
            pass
        else:
            lon.append(float(line.split()[0]))
            lat.append(float(line.split()[1]))
    lon=array(lon)
    lat=array(lat)
    return lon,lat

#Crear las regiones
acapulco=region()
aquila=region()
armeria=region()
benito_juarez=region()
cabo_corrientes=region()
cihuatlan=region()
coahuayana=region()
copala=region()
coyuca_benitez=region()
cuajinicuilapa=region()
florencia_villareal=region()
jose_azueta=region()
la_huerta=region()
la_union=region()
lazaro_cardenas=region()
manzanillo=region()
marquelia=region()
petatlan=region()
san_marcos=region()
tecoman=region()
tecpan=region()
tomatlan=region()

#Inicializar las regiones
acapulco.lon,acapulco.lat=read_region('/Users/octavio/WarningMaps/gisfiles/acapulco.xy')
aquila.lon,aquila.lat=read_region('/Users/octavio/WarningMaps/gisfiles/aquila.xy')
armeria.lon,armeria.lat=read_region('/Users/octavio/WarningMaps/gisfiles/armeria.xy')
benito_juarez.lon,benito_juarez.lat=read_region('/Users/octavio/WarningMaps/gisfiles/benito_juarez.xy')
cabo_corrientes.lon,cabo_corrientes.lat=read_region('/Users/octavio/WarningMaps/gisfiles/cabo_corrientes.xy')
cihuatlan.lon,cihuatlan.lat=read_region('/Users/octavio/WarningMaps/gisfiles/cihuatlan.xy')
coahuayana.lon,coahuayana.lat=read_region('/Users/octavio/WarningMaps/gisfiles/coahuayana.xy')
copala.lon,copala.lat=read_region('/Users/octavio/WarningMaps/gisfiles/copala.xy')
coyuca_benitez.lon,coyuca_benitez.lat=read_region('/Users/octavio/WarningMaps/gisfiles/coyuca_benitez.xy')
cuajinicuilapa.lon,cuajinicuilapa.lat=read_region('/Users/octavio/WarningMaps/gisfiles/cuajinicuilapa.xy')
florencia_villareal.lon,florencia_villareal.lat=read_region('/Users/octavio/WarningMaps/gisfiles/florencia_villareal.xy')
jose_azueta.lon,jose_azueta.lat=read_region('/Users/octavio/WarningMaps/gisfiles/jose_azueta.xy')
la_huerta.lon,la_huerta.lat=read_region('/Users/octavio/WarningMaps/gisfiles/la_huerta.xy')
la_union.lon,la_union.lat=read_region('/Users/octavio/WarningMaps/gisfiles/la_union.xy')
lazaro_cardenas.lon,lazaro_cardenas.lat=read_region('/Users/octavio/WarningMaps/gisfiles/lazaro_cardenas.xy')
manzanillo.lon,manzanillo.lat=read_region('/Users/octavio/WarningMaps/gisfiles/manzanillo.xy')
marquelia.lon,marquelia.lat=read_region('/Users/octavio/WarningMaps/gisfiles/marquelia.xy')
petatlan.lon,petatlan.lat=read_region('/Users/octavio/WarningMaps/gisfiles/petatlan.xy')
san_marcos.lon,san_marcos.lat=read_region('/Users/octavio/WarningMaps/gisfiles/san_marcos.xy')
tecoman.lon,tecoman.lat=read_region('/Users/octavio/WarningMaps/gisfiles/tecoman.xy')
tecpan.lon,tecpan.lat=read_region('/Users/octavio/WarningMaps/gisfiles/tecpan.xy')
tomatlan.lon,tomatlan.lat=read_region('/Users/octavio/WarningMaps/gisfiles/tomatlan.xy')

#Crear un arreglo de regiones
regions=[acapulco,aquila,armeria,benito_juarez,cabo_corrientes,cihuatlan,coahuayana,copala,coyuca_benitez,cuajinicuilapa,florencia_villareal,jose_azueta,la_huerta,la_union,lazaro_cardenas,manzanillo,marquelia,petatlan,san_marcos,tecoman,tecpan,tomatlan]

#Ciclar sobre cada punto de costa, ver a que region pertenece
for k in range(len(lon_out)):
    d=[]
    print k
    for kregion in range(len(regions)):
        d.append(sqrt((lon_out[k]-regions[kregion].lon)**2+(lat_out[k]-regions[kregion].lat)**2).min())
    if argmin(d)==0:
	acapulco.eta.append(eta_out[k])
    if argmin(d)==1:
        aquila.eta.append(eta_out[k])
    if argmin(d)==2:
        armeria.eta.append(eta_out[k])
    if argmin(d)==3:
        benito_juarez.eta.append(eta_out[k])
    if argmin(d)==4:
        cabo_corrientes.eta.append(eta_out[k])
    if argmin(d)==5:
        cihuatlan.eta.append(eta_out[k])
    if argmin(d)==6:
        coahuayana.eta.append(eta_out[k])
    if argmin(d)==7:
        copala.eta.append(eta_out[k])
    if argmin(d)==8:
        coyuca_benitez.eta.append(eta_out[k])
    if argmin(d)==9:
        cuajinicuilapa.eta.append(eta_out[k])
    if argmin(d)==10:
        florencia_villareal.eta.append(eta_out[k])
    if argmin(d)==11:
        jose_azueta.eta.append(eta_out[k])
    if argmin(d)==12:
        la_huerta.eta.append(eta_out[k])
    if argmin(d)==13:
        la_union.eta.append(eta_out[k])
    if argmin(d)==14:
        lazaro_cardenas.eta.append(eta_out[k])
    if argmin(d)==15:
        manzanillo.eta.append(eta_out[k])
    if argmin(d)==16:
        marquelia.eta.append(eta_out[k])
    if argmin(d)==17:
        petatlan.eta.append(eta_out[k])
    if argmin(d)==18:
        san_marcos.eta.append(eta_out[k])
    if argmin(d)==19:
        tecoman.eta.append(eta_out[k])
    if argmin(d)==20:
        tecpan.eta.append(eta_out[k])
    if argmin(d)==21:
        tomatlan.eta.append(eta_out[k])
        
#Asignar color de alerta
def warn_color(region):    
    eta=array(region.eta)
    i=where(isnan(eta)==True)[0]
    eta[i]=0
    red='220/20/60'
    orange='255/140/0'
    yellow='255/215/0'
    green='50/205/50'
    if len(eta) < 1:
        color=green
    elif max(eta) > 3:
        color=red
    elif max(eta) > 1:
        color=orange
    elif max(eta) > 0.3:
        color=yellow
    elif max(eta) <= 0.3:
        color=green
    return color

#Obtener niveles de alerta
acapulco.color=warn_color(acapulco)
aquila.color=warn_color(aquila)
armeria.color=warn_color(armeria)
benito_juarez.color=warn_color(benito_juarez)
cabo_corrientes.color=warn_color(cabo_corrientes)
cihuatlan.color=warn_color(cihuatlan)
coahuayana.color=warn_color(coahuayana)
copala.color=warn_color(copala)
coyuca_benitez.color=warn_color(coyuca_benitez)
cuajinicuilapa.color=warn_color(cuajinicuilapa)
florencia_villareal.color=warn_color(florencia_villareal)
jose_azueta.color=warn_color(jose_azueta)
la_huerta.color=warn_color(la_huerta)
la_union.color=warn_color(la_union)
lazaro_cardenas.color=warn_color(lazaro_cardenas)
manzanillo.color=warn_color(manzanillo)
marquelia.color=warn_color(marquelia)
petatlan.color=warn_color(petatlan)
san_marcos.color=warn_color(san_marcos)
tecoman.color=warn_color(tecoman)
tecpan.color=warn_color(tecpan)
tomatlan.color=warn_color(tomatlan)

#Escribir archivo de alertas
f=open(fout,'w')
f.write('Acapulco='+acapulco.color+'\n')
f.write('Aquila='+aquila.color+'\n')
f.write('Armeria='+armeria.color+'\n')
f.write('Benito_Juarez='+benito_juarez.color+'\n')
f.write('Cabo_Corrientes='+cabo_corrientes.color+'\n')
f.write('Cihuatlan='+cihuatlan.color+'\n')
f.write('Coahuyana='+coahuayana.color+'\n')
f.write('Copala='+copala.color+'\n')
f.write('Coyuca_de_Benitez='+coyuca_benitez.color+'\n')
f.write('Cuajinicuilapa='+cuajinicuilapa.color+'\n')
f.write('Florencia_Villareal='+florencia_villareal.color+'\n')
f.write('Jose_Azueta='+jose_azueta.color+'\n')
f.write('La_Huerta='+la_huerta.color+'\n')
f.write('La_Union='+la_union.color+'\n')
f.write('Lazaro_Cardenas='+lazaro_cardenas.color+'\n')
f.write('Manzanillo='+manzanillo.color+'\n')
f.write('Marquelia='+marquelia.color+'\n')
f.write('Petatlan='+petatlan.color+'\n')
f.write('San_Marcos='+san_marcos.color+'\n')
f.write('Tecoman='+tecoman.color+'\n')
f.write('Tecpan='+tecpan.color+'\n')
f.write('Tomatlan='+tomatlan.color)
f.close()
