#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:00:47 2025

@author: Estudiante
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


carpeta = '~/Downloads/Clase11_12_Visualizacion/'

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

ax.scatter(data= df_selecc[df_selecc['origen'] == origen], x = 'diametro', y= 'altura_tot', c = colores[origen], alpha = 0.5, label = origen)

colores = dict(zip(['Exótico', 'Nativo/Autóctono', 'No determinado'], ['darkorange', 'green', 'black']))

fig, ax = plt.subplots()
for origen in ['Exótico', 'Nativo/Autóctono', 'No determinado']:
    ax.scatter(data= df_selecc['origen'] == origen)

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

wine['type'].value_counts().plot(kind = 'pie',
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
# %%Grafico de barras

cheetahRegion = pd.read_csv(carpeta + 'cheetahRegion.csv')

fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-seriff'

ax.bar(data = cheetahRegion, x='Anio', height='Ventas')

ax.set_title('Ventas de la compañia Cheetah Sports')
ax.set_xlabel('Año', fontsize='medium')
ax.set_ylabel('Ventas (millones de $)', fontsize='medium')
ax.set_xlim(0, 11)
ax.set_ylim(0, 250)

ax.set_xticks(range(1,11,1)) #Muestra todos los ticks del eje x
ax.set_yticks([]) #Remueve los ticks del eje y
ax.bar_label(ax.containers[0], fontsize=8) #Agrega la etiqueta a cada barra

# %% Barras agrupadas

fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-seriff'

cheetahRegion.plot(x='Anio',
                   y=['regionEste', 'regionOeste'],
                   kind='bar',
                   label=['Region Este', 'Region Oeste'],
                   ax=ax)


# %% Barras apiladas

fig, ax = plt.subplots()

#Grafica la serie regionEste
ax.bar(cheetahRegion['Anio'], cheetahRegion['regionEste'],
       label='Region Este', color='#4A4063')
#Grafica la serie regionOeste
ax.bar(cheetahRegion['Anio'], cheetahRegion['regionOeste'],
       bottom=cheetahRegion['regionEste'], label='Region Oeste',
       color='skyblue')

# %% Grafico de linea

fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-seriff'

ax.plot('Anio', 'Ventas', data=cheetahRegion, marker = 'o')
ax.set_title('Ventas de la compañia Cheetah Sports')
ax.set_xlabel('Año', fontsize='medium')
ax.set_ylabel('Ventas (millones de $)', fontsize='medium')
ax.set_xlim(0, 12)
ax.set_ylim(0, 250)

# %% Grafico de lineas

fig, ax = plt.subplots()

plt.rcParams['font.family'] = 'sans-seriff'

#Grafica la serie regionEste
ax.plot('Anio', 'regionEste', data=cheetahRegion,
        marker = '.',
        linestyle='-',
        linewidth=0.5,
        label='Region Este',
        )

#Grafica la serie regionOeste
ax.plot('Anio', 'regionOeste', data=cheetahRegion,
        marker = '.',
        linestyle='-',
        linewidth=0.5,
        label='Region Oeste',
        )


# %% Distribucion de Datos Categoricos

gaseosas = pd.read_csv(carpeta + 'gaseosas.csv')

fig, ax= plt.subplots()
gaseosas['Compras_gaseosas'].value_counts(normalize = True).plot.bar(ax = ax)

ax.set_title('Frecuencia Venta de Gaseosas')
ax.set_xlabel('Marcas de gaseosas')
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
ax.tick_params(axis='x', labelrotation=0)

# %%


#Frecuencia relativa de las ventas de gaseosas
fig, ax = plt.subplots()

gaseosas['Compras_gaseosas'].value_counts(normalize=True).plot.bar
ax.set_title('Frecuencia Venta de Gaseosas')
ax.set_xlabel('Marcas de gaseosas')
ax.set_yticks([])
ax.bar_label(ax.containers[0], fontsize=8)
ax.tick_params(axis='x', labelrotation=0)

# %%Histogramas - Distribucion de datos continuos

ageAtDeath = pd.read_csv(carpeta + 'ageAtDeath.csv')

fig, ax = plt.subplots()

sns.histplot(data = ageAtDeath['AgeAtDeath'], bins=17)


# %%Estadística descriptiva: Medidas de tendencia y dispersión

tips = pd.read_csv(carpeta + 'tips.csv')

#Media
tips['tip'].mean()

#Mediana
tips['tip'].median()

#Moda
tips['tip'].mode()

#Rango
rango_tips = max(tips['tip']) - min(tips['tip'])
print(rango_tips)

#Desviacion Estandar
tips['tip'].std()

#Comando muy util: metodo describe()
tips['tip'].describe()

# %% Boxplot


ventaCasas = pd.read_csv(carpeta + 'ventaCasas.csv')

fig, ax = plt.subplots()

ax.boxplot(ventaCasas['PrecioDeVenta'], showmeans = True)

#Agrega titulo, etiquetas a los ejes
#y limita el rango de valores de los ejes
ax.set_title('Precio de venta de casas')
ax.set_xticks([])
ax.set_ylabel('Precio de compra ($)')
# ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('$ {x:,.2f}'))
ax.set_ylim(0,500)

# %% Boxplot-2 clases cualitativas con variable cuantitativa en y


fig, ax = plt.subplots()

tips.boxplot(by=['sex'], column=['tip'],
             ax=ax, grid=False, showmeans=True)

#Agrega titulo, etiquetas a los ejes
fig.suptitle('')
ax.set_title('Propinas')
ax.set_xlabel('Sexo')
ax.set_ylabel('Valor de la Propina ($)')

# %% Boxplot-2 Clases cualitativas con variable temporal en x y variable cuantitativa en y


ax = sns.boxplot(x='day',
                 y='tip',
                 hue='sex',
                 data=tips,
                 order=['Thur', 'Fri', 'Sat', 'Sun'],
                 palette={'Female': 'orange', 'Male': 'skyblue'})


ax.set_title('Popinas')
ax.set_xlabel('Dia de la Semana')
ax.set_ylabel('Valor de la Propina ($)')
ax.set_ylim(0,12)
ax.legend(title='Sexo')
ax.set_xticklabels(['Jueves', 'Viernes', 'Sabado', 'Domingo'])


# %% Violinplot

ax = sns.violinplot(x='sex',
                 y='tip',
                 data=tips,
                 palette={'Female': 'orange', 'Male': 'skyblue'})


ax.set_title('Popinas')
ax.set_xlabel('Sexo')
ax.set_ylabel('Valor de la Propina ($)')
# ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('$ {x:,.2f}'))
ax.set_ylim(0,12)
ax.set_xticklabels(['Femenino', 'Masculino'])
