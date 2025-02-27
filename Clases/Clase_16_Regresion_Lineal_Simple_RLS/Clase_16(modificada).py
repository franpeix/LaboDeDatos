#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 13:47:28 2025

@author: Estudiante
"""

import pandas as pd
import duckdb as dd
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import r2_score, mean_squared_error

carpeta = '~/Descargas/Clase_16_RLS/'


# %%roundup


ru= pd.read_csv(carpeta +'datos_roundup.txt', delim_whitespace=' ')

# %%Aproximar recta

# Y= a + b*X (a=ordenada al origen, b=pendiente)

X = np.linspace(min(ru['RU']), max(ru['RU']))
a=106.5
b=0.037
Y= a + b*X

plt.scatter(ru['RU'], ru['ID'])
plt.plot(X, Y, 'r')
plt.show()

#%% Obtener recta de cuadrados minimos

# promX= sum(ru['RU'])

# promY= sum(ru['ID'])

b, a = np.polyfit(ru['RU'], ru['ID'], 1) #Me devuelve la recta mas exacta, devuelve los valores al reves, es decir, RU es a e ID es b

Y= a + b*X


plt.scatter(ru['RU'], ru['ID'])
plt.plot(X, Y, 'k')
plt.show()



#%% Calcular score R²// Wue tanto se parece a una recta los puntos

# x: valores de RU
# Y: valores segun x

X= ru['RU'] #antes x era nuestro linspace
Y= ru['ID']
Y_pred = a + b*X

r2 = r2_score(Y, Y_pred)
print("R²: " + str(r2))


mse= mean_squared_error(Y, Y_pred) #Promedio de cuantos se desvian de la recta, pero es un promedio segun el ID, el error esperado sobre la recta



# %%
ruLibreta= pd.read_csv(carpeta +'datos_libreta_2524.txt', delim_whitespace=' ')



X = np.linspace(min(ruLibreta['RU']), max(ruLibreta['RU']))


bLibreta, aLibreta = np.polyfit(ruLibreta['RU'], ruLibreta['ID'], 1)
Y= a+b*X

plt.scatter(ruLibreta['RU'], ruLibreta['ID'])
plt.plot(X, Y, 'r')
plt.show()


X= ruLibreta['RU']
Y= ruLibreta['ID']
Y_pred= a + b*X




r2 = r2_score(Y, Y_pred)
print("R²: " + str(r2))


mse= mean_squared_error(Y, Y_pred)

# %%===========================================================================
# Anascombe
# =============================================================================
df = sns.load_dataset("anscombe")


# %%===========================================================================
# mpg(miles per galon)
# =============================================================================

mpg = pd.read_csv(carpeta + "auto-mpg.xls")

"""
mpg: miles per galon
displacement: Cilindrada

"""

print(mpg.dtypes) #Imprime los tipos de las columnas

mpgSeleccionada = mpg.drop(['car name'], axis=1)

# %% Comparar variables con graficos



def versus(col1, col2):
    sns.scatterplot(data=mpgSeleccionada, x=col1, y=col2)
    plt.show()
    

versus('mpg', 'horsepower')

#%% Comparar variables y calcular recta de cuadrados minimos

def reg_lineal(col1, col2, grado=1):
    X = np.linspace(min(col1), max(col1))
    b, a = np.polyfit(col1, col2, grado)
    Y= a+b*X
    plt.scatter(col1, col2)
    plt.plot(X, Y, 'r')
    plt.show()
    
reg_lineal(mpg['weight'], mpgSeleccionada['horsepower'])
    
#%% Comparar variables, calcular recta de cuadrados minimos y calcular R²

def reg_lineal_r2(col1, col2, grado=1):
    X = np.linspace(min(col1), max(col1))
    b, a = np.polyfit(col1, col2, grado)
    Y= a+b*X
    plt.scatter(col1, col2)
    plt.plot(X, Y, 'r')
    Xr2= col1
    Yr2= col2
    Y_predr2= a + b*X
    r2 = r2_score(Yr2, Y_predr2)
    plt.title("R²: " + str(r2))
    plt.show()

reg_lineal(mpg['mpg'], mpgSeleccionada['weight'])

# %%




# Obtener recta de cuadrados minimos


plt.scatter(ru['RU'], ru['ID'])
plt.plot(X, Y, 'k')
plt.show()