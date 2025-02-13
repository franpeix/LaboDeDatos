#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:00:47 2025

@author: Estudiante
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


carpeta = '/home/Estudiante/Descargas/'

wine= pd.read_csv(carpeta+ 'wine.csv', sep = ";") #Algunos csv estan separados por ; por lo que hay que especificarlo a veces



#Genera el grafico que relaciona la acidez (no volatil) y el contenido de acido citrico de cada vino
plt.scatter(data = wine, x='fixed acidity', y='residual sugar')


fig, ax = plt.subplots() #Devuelve una tupla

plt.rcParams['font.family'] = 'sans-serif'
ax.scatter(data = wine,
           x= 'fixed acidity',
           y= 'citric acid',
           s= 8,                #Tamaño de los puntos
           color= 'magenta')    #Color de los puntos

ax.set_title('Acidez vs contenido de acido citrico') #Titulo de grafico
ax.set_xlabel('Acidez (g/dm3)', fontsize = 'medium') #Nombre eje X
ax.set_ylabel('Contenido de acido citrico (g/dm3)', fontsize = 'medium') #Nombre eje Y



# %%


arbolado = pd.read_csv(carpeta + 'arbolado-en-espacios-verdes.csv', index_col = 2)
#1)#Cuantas variables tiene el dataset? De que tipo son?
#El dataset posee 17 variables
#categorico: nombre cientfico, tipo de follaje, espacio verde
#cuantitativas: latitud, longitud, inclinacion
#Ordinal: No hay, indica un orden, un ordinal nunca es continuo

#Cuantas filas tiene?Contenido de acido citrico (g/dm3)
#Las columnas de tipo categorico, que valores toman? Con que frecuencia?
#Las columnas de tipo numerico? Que representan? Como se distribuyen los valores?


#2)

especieCantidad = list(arbolado['nombre_com'].value_counts().index)[:30]

#Aplico filtros
filtro  = arbolado['nombre_com'].isin(especieCantidad)
resultado = arbolado[filtro]
plt.scatter(data = resultado, x='diametro', y='altura_tot')
plt.scatter(data = resultado, x='long', y='lat')
# %%


fig, ax = plt.subplots() #Devuelve una tupla

plt.rcParams['font.family'] = 'sans-serif'
ax.scatter(data = resultado,
           x= 'diametro',
           y= 'altura_tot',
           s= 8,                #Tamaño de los puntos
           color= 'red')    #Color de los puntos

ax.set_title('Altura respecto del diametro') #Titulo de grafico
ax.set_xlabel('Altura (m)', fontsize = 'medium') #Nombre eje X
ax.set_ylabel('Diámetro (m)', fontsize = 'medium') #Nombre eje Y

# %%


fig, ax = plt.subplots() #Devuelve una tupla

plt.rcParams['font.family'] = 'sans-serif'
ax.scatter(data = resultado,
           x= 'long',
           y= 'lat',
           s= 8,                #Tamaño de los puntos
           color= 'darkturquoise')    #Color de los puntos

ax.set_title('Longitud y Latitud') #Titulo de grafico
ax.set_xlabel('Longitud (°)', fontsize = 'medium') #Nombre eje X
ax.set_ylabel('Latitud (°)', fontsize = 'medium') #Nombre eje Y
# %%

ax.scatter(data= df_selecc[df_selecc['origen']] == origen], x = 'diametro', y= 'altura_tot', c = colores[origen], alpha = 0.5, label = origen)

colores = dict(zip(['Exótico', 'Nativo/Autóctono', 'No determinado'], ['darkorange', 'green', 'black']))

fig, ax = plt.subplots()
for origen in ['Exótico', 'Nativo/Autóctono', 'No determinado']:
    ax.scatter(data= df_selecc['origen'] == origen])

plt.rcParams['font.family'] = 'sans-serif'

tamanoBurbuja = 5 #Cuanto queremos modificar el tamaño de cada burbuja

ax.scatter(data = wine,
           x= 'fixed acidity',
           y= 'citric acid',
           s= wine['residual sugar'] * tamanoBurbuja,                #Tamaño de los puntos
           color= 'darkturquoise')    #Color de los puntos

ax.set_title('Relacion entre tres variables') #Titulo de grafico
ax.set_xlabel('Acidez (g/dm3)', fontsize = 'medium') #Nombre eje X
ax.set_ylabel('Contenido de acido citrico (g/dm3)', fontsize = 'medium') #Nombre eje Y

# %% Grafico de globos/burbujas (bubble chart). En este caso añadimos la variable residual sugar, que determina la cantidad de azucar que hay en cada puntito 

fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'

tamanoBurbuja = 5 #Cuanto queremos modificar el tamaño de cada burbuja

ax.scatter(data = wine,
           x= 'fixed acidity',
           y= 'citric acid',
           s= wine['residual sugar'] * tamanoBurbuja,                #Tamaño de los puntos
           color= 'darkturquoise')    #Color de los puntos

ax.set_title('Relacion entre tres variables') #Titulo de grafico
ax.set_xlabel('Acidez (g/dm3)', fontsize = 'medium') #Nombre eje X
ax.set_ylabel('Contenido de acido citrico (g/dm3)', fontsize = 'medium') #Nombre eje Y

# %%Grafico de torta

fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9.0

wine['type'].value_counts.plot(kind = 'pie',
                               ax= ax,
                               autopct = '%1.1f%%',             #Añadir porcentajes
                               colors= ['#66b3ff', '#ff9999'],  #Cambiar los colores
                               startangle = 90,                 #Iniciar en ángulo 90
                               shadow = True,                   #Añadir sombra
                               explode = (0.1, 0),              #Separar la primera slice
                               legend = False #Evitar leyenda
                               )        
ax.set_ylabel('') #Remover el label del eje Y
ax.set_title('Distribución de Tipos de VIno') #Añadir un título
