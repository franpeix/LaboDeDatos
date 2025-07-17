# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 14:12:57 2025

@author: franp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import duckdb as dd
from matplotlib import ticker
import seaborn as sns 
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



carpeta = '~/OneDrive\Escritorio\LaboDeDatos\Practicas\GuiaPractica14_Clasificacion\Archivos/'

arboles = pd.read_csv(carpeta + 'arboles.csv')

# Cada árbol tiene 3 atributos (altura, ancho, inclinación) y la variable a predecir es la especie.

# %% 1)Explorar los datos, graficar histogramas de los atributos.

nbins = 35

f, s = plt.subplots()
plt.suptitle('Histogramas de los 3 atributos', size = 'large')


sns.histplot(data = arboles, x= 'altura_tot', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis')

sns.histplot(data = arboles, x= 'diametro', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis')

sns.histplot(data = arboles, x= 'inclinacio', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis')


# %% 2) Graficar scatterplot diámetro-altura con colores por especie.

sns.scatterplot(data=arboles, x='diametro', y='altura_tot', hue='nombre_com')

# %% 3) Entrenar un árbol de decisión para clasificar árboles

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# class sklearn.tree.DecisionTreeClassifier(*,criterion='gini',splitter='best',max_depth=None,min_samples_split=2,min_samples_leaf=1,min_weigth_fraction_leaf=0.0,max_features=None,random_state=None,max_leaf_nodes=None,min_impurity_decrease=0.0,class_weight=None,ccp_alpha=0.0)

#a. probar con distintas profundidades
infoUsada = arboles[['diametro','altura_tot','inclinacio']]
y = arboles['nombre_com']

# Dividir el conjunto de datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(infoUsada, y, test_size=0.2, random_state=42)

arbol = DecisionTreeClassifier(criterion = 'entropy', max_depth=2)

arbol.fit(X_train, y_train)

# Predecir los resultados con el conjunto de prueba
y_pred = arbol.predict(X_test)

# Calcular la precisión del modelo
exactitud = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {exactitud:.2f}')

plt.figure(figsize=[20,10])
tree.plot_tree(arbol, feature_names= ['altura_tot','diametro','inclinacio'], class_names =['Ceibo', 'Jacarandá', 'Eucalipto', 'Pindó'] , filled = True, rounded = True, fontsize=8)
plt.show()

#--------------------------------------------------

infoUsada = arboles[['diametro','altura_tot','inclinacio']]
y = arboles['nombre_com']

# Dividir el conjunto de datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(infoUsada, y, test_size=0.2, random_state=42)

arbol = DecisionTreeClassifier(criterion = 'entropy', max_depth=6)

arbol.fit(X_train, y_train)

# Predecir los resultados con el conjunto de prueba
y_pred = arbol.predict(X_test)

# Calcular la precisión del modelo
exactitud = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {exactitud:.2f}')

plt.figure(figsize=[20,10])
tree.plot_tree(arbol, feature_names= ['altura_tot','diametro','inclinacio'], class_names =['Ceibo', 'Jacarandá', 'Eucalipto', 'Pindó'] , filled = True, rounded = True, fontsize=8)
plt.show()

#b. probar con criterio de información y de gini
#Gini: gini
infoUsada = arboles[['diametro','inclinacio']]
y = arboles['nombre_com']

# Dividir el conjunto de datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(infoUsada, y, test_size=0.2, random_state=42)

arbol = DecisionTreeClassifier(criterion = 'gini', max_depth=2)

arbol.fit(X_train, y_train)

# Predecir los resultados con el conjunto de prueba
y_pred = arbol.predict(X_test)

# Calcular la precisión del modelo
exactitud = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {exactitud:.2f}')

plt.figure(figsize=[20,10])
tree.plot_tree(arbol, feature_names= ['altura_tot','diametro','inclinacio'], class_names =['Ceibo', 'Jacarandá', 'Eucalipto', 'Pindó'] , filled = True, rounded = True, fontsize=8)
plt.show()

#--------------------------------------------------
#Info Gain: entropy
infoUsada = arboles[['diametro','altura_tot','inclinacio']]
y = arboles['nombre_com']

# Dividir el conjunto de datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(infoUsada, y, test_size=0.2, random_state=42)

arbol = DecisionTreeClassifier(criterion = 'entropy', max_depth=2)

arbol.fit(X_train, y_train)

# Predecir los resultados con el conjunto de prueba
y_pred = arbol.predict(X_test)

# Calcular la precisión del modelo
exactitud = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {exactitud:.2f}')

plt.figure(figsize=[20,10])
tree.plot_tree(arbol, feature_names= ['altura_tot','diametro','inclinacio'], class_names =['Ceibo', 'Jacarandá', 'Eucalipto', 'Pindó'] , filled = True, rounded = True, fontsize=8)
plt.show()


#c. probar no utilizar todos los atributos

infoUsada = arboles[['diametro','inclinacio']]
y = arboles['nombre_com']

# Dividir el conjunto de datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(infoUsada, y, test_size=0.2, random_state=42)

arbol = DecisionTreeClassifier(criterion = 'gini', max_depth=2)

arbol.fit(X_train, y_train)

# Predecir los resultados con el conjunto de prueba
y_pred = arbol.predict(X_test)

# Calcular la precisión del modelo
exactitud = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {exactitud:.2f}')

plt.figure(figsize=[20,10])
tree.plot_tree(arbol, feature_names= ['altura_tot','diametro','inclinacio'], class_names =['Ceibo', 'Jacarandá', 'Eucalipto', 'Pindó'] , filled = True, rounded = True, fontsize=8)
plt.show()

#--------------------------------------------------
 
infoUsada = arboles[['altura_tot','inclinacio']]
y = arboles['nombre_com']

# Dividir el conjunto de datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(infoUsada, y, test_size=0.2, random_state=42)

arbol = DecisionTreeClassifier(criterion = 'gini', max_depth=2)

arbol.fit(X_train, y_train)

# Predecir los resultados con el conjunto de prueba
y_pred = arbol.predict(X_test)

# Calcular la precisión del modelo
exactitud = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {exactitud:.2f}')

plt.figure(figsize=[20,10])
tree.plot_tree(arbol, feature_names= ['altura_tot','diametro','inclinacio'], class_names =['Ceibo', 'Jacarandá', 'Eucalipto', 'Pindó'] , filled = True, rounded = True, fontsize=8)
plt.show()

#En cada caso graficar el árbol de decisión y registrar la exactitud.



# %% 4) Elegir uno de los modelos entrenados

X = arboles[['diametro','altura_tot','inclinacio']]
Y = arboles['nombre_com']

model = DecisionTreeClassifier(criterion = 'gini', max_depth=10)
model.fit(X,Y) #Entreno al modelo con los datos X e Y
Y_pred= model.predict(X) # me fijo que clases les asiga el modelo a mis datos

metrics.accuracy_score(Y, Y_pred)
print('Exactitud del modelo:', metrics.accuracy_score(Y, Y_pred))

#a. graficar el árbol de decisión
plt.figure(figsize=[20,10])
tree.plot_tree(model, feature_names= ['altura_tot','diametro','inclinacio'], class_names =['Ceibo', 'Jacarandá', 'Eucalipto', 'Pindó'] , filled = True, rounded = True, fontsize=8)
plt.show()

#b. ¿cuál es el atributo utilizado en el primer corte?
#El atributo utilizado es si el diametro es <= a 19.5


# %% 5) Dado un árbol que mide 22 m, diámetro 56 e inclinación 8º: ¿cuál especie es?

# Características del árbol dado
arbol_dado = pd.DataFrame(data = {'diametro':[56],'altura_tot':[22], 'inclinacio':[8]})

# Utilizar el modelo para predecir la especie del árbol dado
especie_predicha = model.predict(arbol_dado[['diametro','altura_tot','inclinacio']])

print('La especie del árbol dado es:', especie_predicha[0])
#La especie de arbol predicha es Jacaranda




##OTRA FORMA MAS RAPIDA: 
# Características del árbol dado
arbol_dado = np.array([[56, 22, 8]])

# Utilizar el modelo para predecir la especie del árbol dado
especie_predicha = model.predict(arbol_dado)

print('La especie del árbol dado es:', especie_predicha[0])
