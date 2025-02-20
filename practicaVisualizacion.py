# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:57:36 2025

@author: franp
"""

import pandas as pd
import duckdb as dd
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


carpeta = '/home/Estudiante/Descargas/'



# %% Ejercicio 2

data_ping = sns.load_dataset('penguins')
# a. ¿Qué representa cada línea del dataframe?
# Cada una de ellas representa a un pinguino en particular, describiendo algunos rasgos que posee

# b. ¿Cuántas muestras hay en total?
muestrasTot = data_ping.dropna()

#Hay 333 muestras completas; pero 344 totales(quitando aquellas que poseen valores nulos)


# c. ¿Cuáles son las especies de pingüinos consideradas?
especies = dd.sql("""
                  SELECT DISTINCT species
                  FROM data_ping
                  """).df()

# Hay 3 especies: Adelie, Gentoo y Chinstrap

# d. ¿Cuáles son las islas estudiadas?
islas = dd.sql("""
                  SELECT DISTINCT island
                  FROM data_ping
                  """).df()

# Las islas estudiadas son 3: Torgersen, Biscoe y Dream

# e. Para cada pingüino, ¿con qué datos contamos?
data_ping.columns

# Si bien no todos los pinguinos tienen todos sus datos asignados, contamos con los atributos: species(especie), island(isla), bill_length_mm(longitud del pico en milimetros), bill_depth_mm(profundidad del pico en milimetros), flipper_length(longitud de la aleta en milimetros), body_mass(masa del cuerpo en gramos) y  sex(sexo)

# %% Ejercicio 3
# Averiguar si las islas están pobladas mayormente por alguna especie en particular, o si éstas coexisten, y en ambos casos deberá notificar en qué proporciones. Es importante mencionar que deberá reportar sus descubrimientos de manera resumida a través de gráficos de barra y de torta.

dataTorgersen = dd.sql("""
                       SELECT * 
                       FROM data_ping
                       WHERE island = 'Torgersen'
                       """).df()
                       
dataBiscoe = dd.sql("""
                       SELECT * 
                       FROM data_ping
                       WHERE island = 'Biscoe'
                       """).df()
                       
dataDream = dd.sql("""
                       SELECT * 
                       FROM data_ping
                       WHERE island = 'Dream'
                       """).df()

#Graficos de barra
fig, ax= plt.subplots()
dataTorgersen['species'].value_counts(normalize = True).plot.bar(ax = ax)

ax.set_title('Frecuencia Especies de Pinguinos en Torgersen')
ax.set_xlabel('Especies de pinguinos')
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
ax.tick_params(axis='x', labelrotation=0)

#------------------------
fig, ax= plt.subplots()
dataBiscoe['species'].value_counts(normalize = True).plot.bar(ax = ax)

ax.set_title('Frecuencia Especies de Pinguinos en Torgersen')
ax.set_xlabel('Especies de pinguinos')
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
ax.tick_params(axis='x', labelrotation=0)

#------------------------
fig, ax= plt.subplots()
dataDream['species'].value_counts(normalize = True).plot.bar(ax = ax)

ax.set_title('Frecuencia Especies de Pinguinos en Torgersen')
ax.set_xlabel('Especies de pinguinos')
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
ax.tick_params(axis='x', labelrotation=0)

#Graficos de torta

fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9.0

dataTorgersen['species'].value_counts().plot(kind = 'pie',
                               ax= ax,
                               autopct = '%1.1f%%',             #Añadir porcentajes
                               colors= ['#66b3ff', '#ff9999'],  #Cambiar los colores
                               startangle = 90,                 #Iniciar en ángulo 90
                               shadow = True,                   #Añadir sombra
                               #Separar la primera slice
                               legend = False #Evitar leyenda
                               )        
ax.set_ylabel('') #Remover el label del eje Y
ax.set_title('Distribución de especies de pinguino') #Añadir un título

#------------------------
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9.0

dataBiscoe['species'].value_counts().plot(kind = 'pie',
                               ax= ax,
                               autopct = '%1.1f%%',             #Añadir porcentajes
                               colors= ['#66b3ff', '#ff9999'],  #Cambiar los colores
                               startangle = 90,                 #Iniciar en ángulo 90
                               shadow = True,                   #Añadir sombra
                               explode = (0.1, 0),              #Separar la primera slice
                               legend = False #Evitar leyenda
                               )        
ax.set_ylabel('') #Remover el label del eje Y
ax.set_title('Distribución de especies de pinguino') #Añadir un título


#------------------------
fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9.0

dataDream['species'].value_counts().plot(kind = 'pie',
                               ax= ax,
                               autopct = '%1.1f%%',             #Añadir porcentajes
                               colors= ['#66b3ff', '#ff9999'],  #Cambiar los colores
                               startangle = 90,                 #Iniciar en ángulo 90
                               shadow = True,                   #Añadir sombra
                               explode = (0.1, 0),              #Separar la primera slice
                               legend = False #Evitar leyenda
                               )        
ax.set_ylabel('') #Remover el label del eje Y
ax.set_title('Distribución de especies de pinguino') #Añadir un título



# %% Ejercicio 4

dataChinstrap = dd.sql("""
                       SELECT * 
                       FROM data_ping
                       WHERE species = 'Chinstrap'
                       """).df()
                       
dataAdelie = dd.sql("""
                       SELECT * 
                       FROM data_ping
                       WHERE species = 'Adelie'
                       """).df()
                       
dataGentoo = dd.sql("""
                       SELECT * 
                       FROM data_ping
                       WHERE species = 'Gentoo'
                       """).df()

f, s = plt.subplots(2,2)
plt.suptitle('Histogramas de las 3 especies y global', size = 'large')

sns.histplot(data = data_ping, x= 'bill_depth_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,0], palette = 'viridis')

sns.histplot(data = dataChinstrap, x= 'bill_depth_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,1], palette = 'viridis')

sns.histplot(data = dataAdelie, x= 'bill_depth_mm', hue = 'species', bins=17, stat = 'probability', ax=s[1,0], palette = 'viridis')

sns.histplot(data = dataGentoo, x= 'bill_depth_mm', hue = 'species', bins=17, stat = 'probability', ax=s[1,1], palette = 'viridis')

# %% Ejercicio 5

