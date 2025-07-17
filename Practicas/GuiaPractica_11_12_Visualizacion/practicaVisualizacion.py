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


carpeta = '~/OneDrive/Escritorio/LaboDeDatos/Practicas/'



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

# Realizar lo mismo con las demás variables corporales de los pingüinos. A partir de estos gráficos, responder:
# a. ¿Se puede determinar la especie de un pingüino a partir de una sola característica?
# b. ¿Hay alguna característica que permita discernir entre especies mejor que otras?


#Longitud del pico
f, s = plt.subplots(2,2)
plt.suptitle('Histogramas de las 3 especies y global', size = 'large')

sns.histplot(data = data_ping, x= 'bill_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,0], palette = 'viridis')

sns.histplot(data = dataChinstrap, x= 'bill_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,1], palette = 'viridis')

sns.histplot(data = dataAdelie, x= 'bill_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[1,0], palette = 'viridis')

sns.histplot(data = dataGentoo, x= 'bill_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[1,1], palette = 'viridis')


#Longitud de la aleta
f, s = plt.subplots(2,2)
plt.suptitle('Histogramas de las 3 especies y global', size = 'large')

sns.histplot(data = data_ping, x= 'flipper_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,0], palette = 'viridis')

sns.histplot(data = dataChinstrap, x= 'flipper_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,1], palette = 'viridis')

sns.histplot(data = dataAdelie, x= 'flipper_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[1,0], palette = 'viridis')

sns.histplot(data = dataGentoo, x= 'flipper_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[1,1], palette = 'viridis')



#Masa corporal
f, s = plt.subplots(2,2)
plt.suptitle('Histogramas de las 3 especies y global', size = 'large')

sns.histplot(data = data_ping, x= 'body_mass_g', hue = 'species', bins=17, stat = 'probability', ax=s[0,0], palette = 'viridis')

sns.histplot(data = dataChinstrap, x= 'body_mass_g', hue = 'species', bins=17, stat = 'probability', ax=s[0,1], palette = 'viridis')

sns.histplot(data = dataAdelie, x= 'body_mass_g', hue = 'species', bins=17, stat = 'probability', ax=s[1,0], palette = 'viridis')

sns.histplot(data = dataGentoo, x= 'body_mass_g', hue = 'species', bins=17, stat = 'probability', ax=s[1,1], palette = 'viridis')


#a) No, no es posible determinar una especie por una caracteristica en especifico, pues entre ellas se superponen

#b)
f, s = plt.subplots(2,2)
plt.suptitle('Histogramas de las 3 especies y global', size = 'large')

sns.histplot(data = data_ping, x= 'bill_depth_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,0], palette = 'viridis')

sns.histplot(data = data_ping, x= 'bill_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[0,1], palette = 'viridis')

sns.histplot(data = data_ping, x= 'flipper_length_mm', hue = 'species', bins=17, stat = 'probability', ax=s[1,0], palette = 'viridis')

sns.histplot(data = data_ping, x= 'body_mass_g', hue = 'species', bins=17, stat = 'probability', ax=s[1,1], palette = 'viridis')

#Quizas, puede resultar mas sencillo identificar a la especie Gentoo en aquel asociado a la profundidad del pico, la longitud de la aleta o la masa corporal, pero ninguno sirve para determinar una especie


# %% Ejecricio 6

# Realizar ahora histogramas de las variables observadas, separadas por sexo (f/m). De manera análoga, considerar si hay alguna variable que permita deducir el sexo de un pingüino.

f, s = plt.subplots(2,2)
plt.suptitle('Histogramas de las 3 especies y global', size = 'large')

sns.histplot(data = data_ping, x= 'bill_depth_mm', hue = 'sex', bins=17, stat = 'probability', ax=s[0,0], palette = 'viridis')

sns.histplot(data = data_ping, x= 'bill_length_mm', hue = 'sex', bins=17, stat = 'probability', ax=s[0,1], palette = 'viridis')

sns.histplot(data = data_ping, x= 'flipper_length_mm', hue = 'sex', bins=17, stat = 'probability', ax=s[1,0], palette = 'viridis')

sns.histplot(data = data_ping, x= 'body_mass_g', hue = 'sex', bins=17, stat = 'probability', ax=s[1,1], palette = 'viridis')


#Observo que, con respecto a la longitud del pico, aquellos que posean una longitud mayor a 52mm seran machos; y tambien para aquellos que pesen mas a 5300g, mientras que si pesan menores a 3100g sean de sexo femenino, asi como si tiene una profundidad de pico por menor a 14mm.

# %% Ejercicio 7

# Realizar scatterplots de pares de variables corporales, separadas por sexo. A partir de los gráficos, responder: 
#     a. ¿Hay algún par de variables que permita deducir el sexo?
#     b. ¿Y si se fija una especie en particular?

# sns.scatterplot(x=aux_graf2['Poblacion_Jardin'], y=aux_graf2['Jardines'], 
#                 color='#1f77b4', label='Inicial', s=50, edgecolor='black', alpha=0.5)


colores = dict(zip(['Male', 'Female'], ['blue', 'pink']))

sns.scatterplot(data=data_ping, x= 'bill_depth_mm', y='bill_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=data_ping, x= 'bill_depth_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=data_ping, x= 'bill_depth_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=data_ping, x= 'bill_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=data_ping, x= 'bill_length_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=data_ping, x= 'flipper_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

#a) No, si bien en algunos casos hay extremos en los que hay un solo genero, no es posible determinar el sexo segun un opar de variables

#b)
sns.scatterplot(data=dataAdelie, x= 'bill_depth_mm', y='bill_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataAdelie, x= 'bill_depth_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataAdelie, x= 'bill_depth_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=dataAdelie, x= 'bill_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=dataAdelie, x= 'bill_length_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataAdelie, x= 'flipper_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

#Aqui, se puede apreciar en la comparacion entre la longitud de la aleta y la masa corporal que hay cierta division entre el genero

sns.scatterplot(data=dataBiscoe, x= 'bill_depth_mm', y='bill_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataBiscoe, x= 'bill_depth_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataBiscoe, x= 'bill_depth_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=dataBiscoe, x= 'bill_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=dataBiscoe, x= 'bill_length_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataBiscoe, x= 'flipper_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

#Aqui, se puede apreciar en la comparacion entre la profundidad del pico y la masa corporal que hay cierta division entre el genero, o tambien entre la profundidad y la longitud de la aleta y longitud del pico

sns.scatterplot(data=dataChinstrap, x= 'bill_depth_mm', y='bill_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataChinstrap, x= 'bill_depth_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataChinstrap, x= 'bill_depth_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=dataChinstrap, x= 'bill_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

sns.scatterplot(data=dataChinstrap, x= 'bill_length_mm', y='flipper_length_mm', hue= 'sex', palette= colores)

sns.scatterplot(data=dataChinstrap, x= 'flipper_length_mm', y='body_mass_g', hue= 'sex', palette= colores)

#Aqui, se puede apreciar en la comparacion entre la profundidad del pico y la longitud del pico que hay cierta division entre el genero, o tambien entre la profundidad y la longitud de la aleta 


# %% Ejercicio 9

# Para los pingüinos hembra, a partir de una de sus característica en particular (obviamente que no sea a partir del campo especie), ¿se puede predecir a qué especie pertenece? ¿Y combinando más de una característica?


colores = dict(zip(['Adelie', 'Gentoo', 'Chinstrap'], ['red', 'green', 'blue']))

soloHembras = data_ping[data_ping['sex'] == 'Female']

sns.scatterplot(data=soloHembras, x= 'bill_depth_mm', y='body_mass_g', hue= 'species', palette= colores)

#Si, si combinamos por ejemplo a la profundidad del pico y la masa corporal, podemos detectar que se puede predecir si una hembra es Gentoo

sns.scatterplot(data=soloHembras, x= 'bill_length_mm', y='body_mass_g', hue= 'species', palette= colores)
#En este, se pueden clasificar casi a la perfeccion a la especie segun sus dichos rasgos fisicos

# %% Ejercicio 10

#Repetir el punto anterior pero para pingüinos macho.

colores = dict(zip(['Adelie', 'Gentoo', 'Chinstrap'], ['red', 'green', 'blue']))

soloMachos = data_ping[data_ping['sex'] == 'Male']

sns.scatterplot(data=soloMachos, x= 'flipper_length_mm', y='body_mass_g', hue= 'species', palette= colores)

#De igual forma, con estos mismos se pueden detectar si es Gentoo

sns.scatterplot(data=soloMachos, x= 'bill_length_mm', y='body_mass_g', hue= 'species', palette= colores)
#En este, se pueden clasificar casi a la perfeccion a la especie segun sus dichos rasgos fisicos



# %% Ejercicio 11

# Realizar un gráfico (de línea) donde se vea la relación entre la variable largo del pico y masa corporal, para la especie Adelie. Sugerencia: reordenar el subconjunto de pingüinos Adelie por la variable largo del pico, y utilizarlo para graficar.

dataAdelie = dd.sql("""
                    SELECT *
                    FROM dataAdelie
                    ORDER BY bill_length_mm
                    """).df()

sns.lineplot(data = dataAdelie, x='body_mass_g', y= 'bill_length_mm')

# %% Ejercicio 12

# %% Ejercicio 12

# Realizar un gráfico de barras apiladas para visualizar la cantidad de pingüinos de cada sexo dentro de cada especie.


# Contar la cantidad de cada combinación de especie y sexo
df_counts = data_ping.groupby(['species', 'sex']).size().unstack(fill_value=0)

# Calcular el acumulado (bottom) para apilar barras
df_cumsum = df_counts.cumsum(axis=1)

# Crear el gráfico
fig, ax = plt.subplots(figsize=(8, 6))

# Graficar ambos sexos de una sola vez
sns.barplot(x=df_counts.index, y=df_counts["Female"], color="red", label="Female", ax=ax)
sns.barplot(x=df_counts.index, y=df_counts["Male"], color="blue", label="Male", ax=ax, bottom=df_cumsum["Female"])

# Etiquetas y leyenda
ax.set_ylabel("Cantidad")
ax.set_title("Gráfico de Barras Apiladas por Sexo y Especie")
ax.legend(title="Sexo")

plt.show()


# %% Ejercicio 13

# Realizar un boxplot de la variable ancho del pico, separado por sexo. ¿Qué se observa?

sns.boxplot(data=data_ping, x='sex', y='bill_depth_mm',  palette={'Female': 'orange', 'Male': 'skyblue'})

# Se observa que los machos poseen una mediana mayor de anchura de pico

# %% Ejercicio 14

# Realizar un boxplot de la variable largo de aleta, separado por especie. ¿Qué se observa?

sns.boxplot(data=data_ping, x='species', y='flipper_length_mm',  palette={'Adelie': 'orange', 'Gentoo': 'skyblue', 'Chinstrap': 'red'})

#Se observa que la especie Gentoo posee una gran mayor mediana en el largo de aleta con respecto a las otras dos especies; y Chinstrap es la siguiente especie con mayor largo de aleta

# %% Ejercicio 15

# Realizar un violinplot de la variable largo de aleta, separado por sexo

sns.violinplot(data=data_ping, x='sex', y='flipper_length_mm', palette={'Female': 'orange', 'Male': 'skyblue'})


# %% Ejercicio 16

# Realizar un violinplot de la variable masa corporal, separado por especie.


sns.violinplot(data=data_ping, x='species', y='body_mass_g',  palette={'Adelie': 'orange', 'Gentoo': 'skyblue', 'Chinstrap': 'red'})