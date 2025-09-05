import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker




# Funciones matemáticas

def sen(x):
    seno=np.sin(np.deg2rad(x))
    return seno
def cos(x):
    coseno=np.cos(np.deg2rad(x))
    return coseno
def arcos(x):
    arcos=np.rad2deg(np.arccos(x))
    return arcos
def adsin(x):
    return np.rad2deg(np.arcsin(x))
def adcos(x):
    return np.rad2deg(np.arccos(x))
def adtan(x):
    return np.rad2deg(np.arctan(x))

# Geometría solar

gsc = 1361.1


def rad_extraterrestre(dia):
    b=(dia-1)*360/365
    epsilon=1.00011+0.034221*cos(np.deg2rad(b))+0.00128*np.sin(np.deg2rad(b))+0.000719*np.cos(np.deg2rad(2*b))+0.000077*np.sin(np.deg2rad(2*b))
    gon=gsc*epsilon
    return gon
def declinacion(dia):
    declinacion=23.45*sen(360*(284+dia)/366)
    return declinacion
def ecuacion_del_tiempo(dia):
    b=(dia-1)*360/365
    e=229.2*10**(-5)*(7.5+186*cos(b)-3200.7*sen(b)-1461.5*cos(2*b)-4089*sen(2*b))
    return e
def long_std(utc):
    long=(utc)*15
    return(long)
def t_solar(t_local, long_loc, long_std, dia):
    solar=t_local*60+4*(long_loc-long_std)+ecuacion_del_tiempo(dia)
    return(solar)
def ang_horario(t):
    w=-180+t*15/60
    return(w)
def cenit_solar(lat, dec, w):
    cenit=np.rad2deg(np.arccos(cos(lat)*cos(dec)*cos(w)+sen(lat)*sen(dec)))
    return(cenit)
def azimut_solar(w, cen, dec, lat):
    azimut=np.rad2deg(np.sign(w)*np.abs(np.arccos((cos(cen)*sen(lat)-sen(dec))/(sen(cen)*cos(lat)))))+180
    return azimut
def incidencia(cenit, beta, azimut, acip):
    theta=np.rad2deg(np.arccos(cos(cenit)*cos(beta)+sen(cenit)*sen(beta)*cos(azimut-acip)))
    return theta

# Crear fechas y horas

año = pd.date_range(start='1/1/2025', end='1/1/2026', freq='d')
dias = pd.date_range(start='4/1/2025', end='4/2/2025', freq='h')

longstgo = -70
latstgo = -33.5
utc = -3

# Aplicar geometría solar

elevacionstgo = []
azimutstgo = []
incidenciastgo = []
cenitstgo = []
horaa = []

for hora in dias:
    dia = hora.day_of_year
    hora = hora.hour+0.5
    horaa.append(hora)
    dec = declinacion(dia)
    tsolar = t_solar(hora, longstgo, long_std(-4), dia)
    w = ang_horario(tsolar)
    cenitsolar = cenit_solar(latstgo, dec, w)
    cenitstgo.append(cenitsolar)
    elevacionstgo.append(90 - cenitsolar)
    azimut = azimut_solar(w, cenitsolar, dec, latstgo)
    azimutstgo.append(azimut)
    theta = incidencia(cenitsolar, 0, azimut, 0)
    incidenciastgo.append(theta)

Elevacion_solar_snE = []
c=0
for i in elevacionstgo:
    c=c+1
    if c<=24:
        if i<=0:
            Elevacion_solar_snE.append(0)
        else:
            Elevacion_solar_snE.append(i)

c=0
Azimut_solar_snE = []
for i in azimutstgo:
    c=c+1
    if c<=24:
        Azimut_solar_snE.append(i)


plt.figure()
plt.scatter(horaa, incidenciastgo, label='Angulo Incidencia', c='red', marker='_')
plt.scatter(horaa, cenitstgo, label='Cenit', c='red', marker='+')
plt.scatter(horaa, elevacionstgo, label='Elevacion', c='blue', marker='*')
plt.xlabel('Tiempo')
plt.ylabel('Cenit')
plt.title('Cenit según el tiempo')
plt.legend(loc = 'upper right')
plt.ylim([0, 90])
plt.show()




plt.figure()
plt.scatter(Azimut_solar_snE, Elevacion_solar_snE, label='Elevación', c='green', marker='H')
plt.xlabel('Azimut')
plt.ylabel('Elevación')
plt.title('Elevación según Azimut')
plt.legend(loc = 'upper right')
plt.ylim([0, 90])
plt.show()



# Abrir Archivos

datos = pd.read_excel("")
datos.columns = datos.iloc[0]
datos = datos.iloc[1:]

