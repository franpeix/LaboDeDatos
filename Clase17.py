#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:45:48 2025

@author: Estudiante
"""

carpeta = '~/Descargas/Clase_17_ContRLS/'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import tree
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
from sklearn.metrics import accuracy_score

#La variable se mide siempre en los atributos y no en la variable explicativa 
#Siempre con knn recortamos la variable explicativa.
# %%
# X = data_roundup[['RU']]MSE_neigh
# Y = data_roundup[['ID']]
 
# modelo_knn = KNeighborsRegressor() #El k en principio es a criterio, y se suelen utilizar muchos k
# modelo_knn.fit(X,Y) #Lo ajustamos
 
# Y_pred = modelo_knn.predict(X) #Para hacer el predict, les pasamos un conjunto de atributos
# mse = mean_squared_error(Y, Y_pred)



data_roundup = pd.read_csv(carpeta + 'datos_roundup.txt', delim_whitespace=' ')

datos = pd.read_csv(carpeta + 'alturas.csv', index_col=0) #Le decimos que indice de columna queda como indice, sino me lo crea automaticamente

datos = datos.iloc[:,:3]
datos_varones= datos[datos['Sexo al nacer (M/F)'] == 'M']
X=datos_varones[['altura madre']]

alturas = datos[['Altura (cm)']]
Y=alturas[datos['Sexo al nacer (M/F)'] == 'M']

neigh = KNeighborsRegressor(n_neighbors=5)
neigh.fit(X, Y) #Ajusta y entrena el modelo

datonuevo= pd.DataFrame([{'altura madre':156}])
YDeUnSoloDato= neigh.predict(datonuevo)
Y_pred= neigh.predict(X) #Me predice el valor de la altura 

mean_squared_error(Y, Y_pred) #para cada fila Y e Y_pred, calcula la diferencia, la eleva al cuadrado y las promedia, promedio de las diferencias al cuadrado calculando asi la diferencia ente los valores reales y los valores predichos

# %%Cambio cantidad de k (A mayor k, mayor cantidad de error)

data_roundup = pd.read_csv(carpeta + 'datos_roundup.txt', delim_whitespace=' ')

datos = pd.read_csv(carpeta + 'alturas.csv', index_col=0) #Le decimos que indice de columna queda como indice, sino me lo crea automaticamente

datos = datos.iloc[:,:3]
datos_varones= datos[datos['Sexo al nacer (M/F)'] == 'M']
X=datos_varones[['altura madre']]

alturas = datos[['Altura (cm)']]
Y=alturas[datos['Sexo al nacer (M/F)'] == 'M']

neigh = KNeighborsRegressor(n_neighbors=5)
neigh.fit(X, Y) #Ajusta y entrena el modelo

datonuevo= pd.DataFrame([{'altura madre':156}])
YDeUnSoloDato= neigh.predict(datonuevo)
Y_pred= neigh.predict(X) #Me predice el valor de la altura 

mean_squared_error(Y, Y_pred) #para cada fila Y e Y_pred, calcula la diferencia, la eleva al cuadrado y las promedia, promedio de las diferencias al cuadrado calculando asi la diferencia ente los valores reales y los valores predichos

# %% La diferencia con Regresion lineal es que con KNN no estamos asumiendo de una distribucion de los datos en particular, los datos pueden ser cualquier cosa y el modelo funciona igual. KNN no asume una forma esoecufuca para la f en Y=f(x)+E no asume el como estan distribuidos los datos.


def listaDistintosK():
    lista = []
    for k in range(1,21,1):
        neigh = KNeighborsRegressor(n_neighbors=k)
        neigh.fit(X, Y)
        Y_pred= neigh.predict(X)
        
        mse = mean_squared_error(Y, Y_pred)
        lista.append(mse)
        
    return lista
    
listaError = listaDistintosK()

plt.plot(list(range(1,21)), listaError)

dicInfo = {'ValoresK':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 'ListaError': listaError}

info= pd.DataFrame(data = dicInfo)

sns.lineplot(data=dicInfo, x='ValoresK', y='ListaError')
plt.show()

#Cuando yo promedio mas cosas, voy a tener un modelo menos complejo(menos saltos, mas aproximado a uno lineal)

# %%

carpeta16 = '~/Descargas/Clase_16_RLS/'

mpg = pd.read_csv(carpeta16 + "auto-mpg.xls")

#X = mpg[['acceleration']]
#Y = mpg[['mpg']]

# neigh = KNeighborsRegressor(n_neighbors=5)
# neigh.fit(X, Y) #Ajusta y entrena el modelo

# Y_pred= neigh.predict(X) #Me predice el valor del mpg

# mse = mean_squared_error(Y, Y_pred)

def listaDistintosK():
    X = mpg[['acceleration']]
    Y = mpg[['mpg']]
    lista = []
    for k in range(1,21,1):
        neigh = KNeighborsRegressor(n_neighbors=k)
        neigh.fit(X, Y)
        Y_pred= neigh.predict(X)
        
        mse = mean_squared_error(Y, Y_pred)
        lista.append(mse)
        
    return lista
    
listaError = listaDistintosK()

dicInfo = {'ValoresK':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 'ListaError': listaError}

info= pd.DataFrame(data = dicInfo)

sns.lineplot(data=dicInfo, x='ValoresK', y='ListaError',)
plt.show()

fig,ax =plt.plot()

#ax.plot(dicInfo[])
# %% Mas de una variable considerada

def listaDistintosK():
    X = mpg[['acceleration', 'weight', 'displacement', 'horsepower']]
    Y = mpg[['mpg']]
    lista = []
    for k in range(1,21,1):
        neigh = KNeighborsRegressor(n_neighbors=k)
        neigh.fit(X, Y)
        Y_pred= neigh.predict(X)
        
        mse = mean_squared_error(Y, Y_pred)
        lista.append(mse)
        
    return lista
    
listaError = listaDistintosK()

dicInfo = {'ValoresK': list(range(1,21)), 'ListaError': listaError}

info= pd.DataFrame(data = dicInfo)

sns.lineplot(data=dicInfo, x='ValoresK', y='ListaError',)
plt.show()

# %% Reescalar los datos

var = ['acceleration','acceleration', 'weight', 'displacement', 'horsepower']

for v in var+["mpg"]:
    mpg[v] = (mpg[v] - mpg[v].min()) / (mpg[v].max() - mpg[v].min())

X=mpg[var]
Y=mpg[['mpg']]

MSE_neigh = pd.DataFrame(columns=['MSE', 'n_neighbors'])

for i in range(1,21):
    neigh = KNeighborsRegressor(n_neighbors=i)
    neigh.fit(X, Y)
    Y_pred= neigh.predict(X)
    MSE = mean_squared_error(Y, Y_pred)
    MSE_neigh.loc[i-1] = [MSE, i]
    
fig,ax = plt.subplots()

ax.plot(MSE_neigh['n_neighbors'], MSE_neigh['MSE'], 'bo-')
ax.set_xlabel('K neighbors')
ax.set_ylabel('MSE')

#--------------------------------------


#data['acceleration'] = 

# %%

var = ['acceleration','acceleration', 'weight', 'displacement', 'horsepower']

for v in var+["mpg"]:
    mpg[v] = (mpg[v] - mpg[v].min()) / (mpg[v].max() - mpg[v].min())

X = mpg[['acceleration', 'weight', 'displacement', 'horsepower']]
Y = mpg[['mpg']]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2) #Quiero q el test sea 20% y el train sea el 80%

listaErroresTrain = []
listaErroresTest = []
for i in range(1,21,1):
    modelo = KNeighborsRegressor(n_neighbors=i)
    modelo.fit(X_train, Y_train)
    Y_pred_train= modelo.predict(X_train)
    Y_pred_test= modelo.predict(X_test)
        
        
    error_train = mean_squared_error(Y_train, Y_pred_train)
    error_test = mean_squared_error(Y_test, Y_pred_test)
        
    listaErroresTrain.append(error_train)
    listaErroresTest.append (error_test)
        

dicInfo = {'ValoresK': list(range(1,21)), 'ListaErrorTrain': listaErroresTrain, 'ListaErrorTest': listaErroresTest}

info= pd.DataFrame(data = dicInfo)


plt.figure(figsize=(10,6))
plt.plot(list(range(1,21)), listaErroresTrain, label='train')
plt.plot(list(range(1,21)), listaErroresTest, label='test')
plt.legend()
plt.xticks(list(range(1,21)))
plt.xlabel('cantidad de vecinos')
plt.ylabel('MSE')
plt.title('MSE segun cantidad de vecinos')
plt.grid()

# %% K folding: distinto k a KNN. No se usa para comparar modelos
# Cross-validation: Usualmente se separa a el dataset en 5 k; en cada vuelta cambio los conjuntos de train y test. Asi considero 5 escenarios distintos de la muestra, y para cada experimento calculo la performance(error, exactitud, lo que yo busco para medir la performance). Una vez hallada cada performance, calculo el promedio entre todos ellos 

# %%Con arboles de decision: modelos de seleccion/clasificacion



modelos = pd.read_csv(carpeta + 'seleccion_modelos.csv')

X =modelos.drop('Y', axis=1)
y = modelos.Y

X_dev, X_eval, y_dev, y_eval = train_test_split(X, y, random_state=1,test_size=0.1)

alturas= [1,2,3,5,8,13,21]
nsplits = 10
kf = KFold(n_splits=nsplits)

resultados = np.zeros((nsplits, len(alturas)))

for i, (train_index, test_index) in enumerate(kf.split(X_dev)):
    
    kf_X_train, kf_X_test = X_dev.iloc[train_index], X_dev.iloc[test_index]
    kf_y_train, kf_y_test = y_dev.iloc[train_index], y_dev.iloc[test_index]
    
    for j, hmax in enumerate(alturas):
        
        arbol=tree.DecisionTreeClassifier(max_depth= hmax)
        arbol.fit(kf_X_train, kf_y_train)
        pred=arbol.predict(kf_X_test)
        
        score = accuracy_score(kf_y_test, pred)
        
        resultados[i, j] = score

#%% promedio scores sobre los folds        
scores_promedio = resultados.mean(axis = 0)

# %%

for i,e in enumerate(alturas):
    print(f'Score promedio del modelo con hmax = {e}: {scores_promedio[i]:.4f}')

#%% entreno el modelo elegido en el conjunto dev entero
arbol_elegido = tree.DecisionTreeClassifier(max_depth = 1)
arbol_elegido.fit(X_dev, y_dev)
y_pred = arbol_elegido.predict(X_dev)

score_arbol_elegido_dev = accuracy_score(y_dev, y_pred)
print(score_arbol_elegido_dev)

#%% pruebo el modelo elegid y entrenado en el conjunto eval
y_pred_eval = arbol_elegido.predict(X_eval)       
score_arbol_elegido_eval = accuracy_score(y_eval, y_pred_eval)
print(score_arbol_elegido_eval)


# %%Con KNN: en este caso no se puede calcular el score_accuracy porq es modelo de regresion
carpeta16 = '~/Descargas/Clase_16_RLS/'

mpg = pd.read_csv(carpeta16 + "auto-mpg.xls")

X = mpg[['acceleration', 'weight', 'displacement', 'horsepower']]
y = mpg[['mpg']]

X_dev, X_eval, y_dev, y_eval = train_test_split(X, y, random_state=7,test_size=0.1) #Un 10% de held  out, el reporte final

kNeighbors = list(range(1,51))

nsplits = 10
kf = KFold(n_splits=nsplits)

resultados = np.zeros((nsplits, len(kNeighbors)))


for i, (train_index, test_index) in enumerate(kf.split(X_dev)):
    
    kf_X_train, kf_X_test = X_dev.iloc[train_index], X_dev.iloc[test_index]
    kf_y_train, kf_y_test = y_dev.iloc[train_index], y_dev.iloc[test_index]
    
    for j, n in enumerate(kNeighbors):
        
        neigh = KNeighborsRegressor(n_neighbors= n)
        neigh.fit(kf_X_train, kf_y_train)
        pred=neigh.predict(kf_X_test)
        
        mse = mean_squared_error(kf_y_test, pred)
        
        resultados[i, j] = mse

#%% promedio scores sobre los folds
mse_promedio = resultados.mean(axis = 0)
#%% 
for i,e in enumerate(kNeighbors):
    print(f'MSE promedio del modelo con kmax = {e}: {mse_promedio[i]:.4f}')
    

#%% entreno el modelo elegido en el conjunto dev entero
Kneighbors_elegido = KNeighborsRegressor(n_neighbors= 1)
Kneighbors_elegido.fit(X_dev, y_dev)
y_pred = Kneighbors_elegido.predict(X_dev)

mse_Kneighbors_elegido_dev = mean_squared_error(y_dev, y_pred)
print(mse_Kneighbors_elegido_dev)

#%% pruebo el modelo elegid y entrenado en el conjunto eval
y_pred_eval = Kneighbors_elegido.predict(X_eval)       
mse_Kneighbors_elegido_eval = mean_squared_error(y_eval, y_pred_eval)
print(mse_Kneighbors_elegido_eval)


#Preguntas:
#1) Es necesario mezclar al azar? 
#Depende de si esta ordenado el set de datos. Lo ideal es que en la mezcla se reresenten las particiones de cada clase. Se respete un balance de las clases, se mantenga la proporcion de clases
#2) Es bueno mezclar al azar?

#3)Como estan ordenado los datos?

#4)Como estan balanceadas las clases?

        