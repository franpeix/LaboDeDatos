#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:12:35 2025

@author: Estudiante
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import duckdb as dd
from matplotlib import ticker
import seaborn as sns
from sklearn.datasets import load_iris 
from sklearn import tree


#%%

iris = load_iris(as_frame = True)

data = iris.frame
atributos = iris.data
Y = iris.target

iris.target_names
diccionario = dict(zip([0,1,2], iris.target_names))


altri = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']


# %%

nbins = 35

f, s = plt.subplots(2,2) #es de 2x2
plt.suptitle('Histogramas de los 4 atributos', size = 'large')


sns.histplot(data = data, x= 'sepal length (cm)', hue = 'target', bins = nbins, stat = 'probability', ax=s[0,0], palette = 'viridis')

sns.histplot(data = data, x= 'sepal width (cm)', hue = 'target', bins = nbins, stat = 'probability', ax=s[0,1], palette = 'viridis')

sns.histplot(data = data, x= 'petal length (cm)', hue = 'target', bins = nbins, stat = 'probability', ax=s[1,0], palette = 'viridis')

sns.histplot(data = data, x= 'petal width (cm)', hue = 'target', bins = nbins, stat = 'probability', ax=s[1,1], palette = 'viridis')

# %% Establecer Umbrales buenos


data_clasif = data.copy()

def clasificador_iris(fila):
    exactitudes = []
    pet_l = fila['petal length (cm)']
    if pet_l < 2.5 :
        clase = 0
    elif pet_l > 4.9:
        clase = 2
    else:
        clase = 1
    data_clasif['clase asignada'] = clase
    exactitud = sum(data_clasif['target'] == data_clasif['clase asignada'])
    exactitudes.append(exactitud)
        
    return clase





    
#No existen umbrales perfectos, pero si aproximaciones a ellos, errores vamos a cometer, pero nosotros queremos minimizar esos errores
#Para pensar en esto, vamos a definir una forma de cuan bien estamos diversificando: Matriz de confusion, y de alli sacamos la exactitud
# %%
# data_clasif = data.copy()






def clasificador_iris_fila(pet):
    
    umbrales = [4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9]
    
    exactitudes = []
    
    for umbral in umbrales:
        data_clasif = data.copy()
        for i, fila in data_clasif.iterrows():
            pet_l = fila['petal length (cm)']
            if pet_l < 2.5:
                clase = 0
            elif pet_l < umbral:
                clase = 1
            else:
                clase = 2
            data_clasif['clase_asignada'] = clase
            exactitud = sum(data_clasif['target'] == data_clasif['clase_asignada'])/150
            exactitudes.append(exactitud)
        
            
    return exactitudes

print(clasificador_iris_fila(data))    
    
exactitudes = clasificador_iris_fila(data)



def clasificador_iris(pet):
    
    umbrales = [4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9]
    
    exactitudes = []
    data_clasif1 = data.copy()
    for umbral in umbrales:
        
        for i, fila in data_clasif1.iterrows():
            pet_l = fila['petal length (cm)']
            if pet_l < 2.5:
                clase = 0
            elif pet_l < umbral:
                clase = 1
            else:
                clase = 2
            data_clasif1['clase_asignada'] = clase
            exactitud = sum(data_clasif['target'] == data_clasif1['clase_asignada'])/150
            exactitudes.append(exactitud)
        
            
    return data_clasif

print(clasificador_iris(data)) 

data_clasif = clasificador_iris(data) 
   
    # clases =set(data['target'])
    
    # matriz_confusion = np.zeros((3,3))
    
    # for i in range(3): #i = clase real, el target
    #     for j in range(3): #clase predicha, clase asignada
    #         filtro = (data_clasif['target'] == i) & (data_clasif['clase_asignada'] == j)
    #         cuenta = len(data_clasif[filtro])
    #         matriz_confusion[i,j] = cuenta
            
    #     matriz_confusion


# %%

#Arboles de decision: muy interpretables
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import duckdb as dd
from matplotlib import ticker
import seaborn as sns

carpeta = "~/Descargas/"


titanic = pd.read_csv(carpeta + 'titanic_training.csv')


clases = dd.sql("""
                SELECT Pclass, COUNT(*) AS cantPorClase
                FROM titanic
                Group by Pclass
                """).df()
                
                
sobrevivientes = dd.sql("""
                        SELECT Sex, SUM(Survived) AS Cantidad
                        FROM titanic
                        GROUP BY sex
                        """).df()
                        
                        
noSobrevivientes = dd.sql("""
                        SELECT Sex, COUNT(*)
                        FROM titanic
                        WHERE Survived = '0'
                        GROUP BY sex
                        """).df()
                        
                        
# %%
nbins = 35

f, ax = plt.subplots()

sns.histplot(data = titanic, x= 'Age', hue = 'Sex', bins = nbins, stat = 'probability', ax=ax, palette = 'viridis')



                        
# def clasificador_titanic(x):
#     vive = False
#     if Regla:
#         vive = True
#     return vive


def didSurvive(row):
    points = 0
    if row['Pclass'] == 1:
        points += 3
    elif row['Pclass'] == 2:
        points += 2
    else:
        points += 1
    
    if row['Sex'] == 'Female':
        points += 1
    if row['Fare'] > 60:
        points += 10
    if row['Age'] < 18:
        points +=4
    elif row['Age'] < 40:
        points += 2
        
        
    if points > 5:
        return 1
    else:
        return 0
    
titanic['predicted'] = titanic.apply(lambda row: didSurvive(row), axis=1)



# %%

from sklearn.tree import DecisionTreeClassifier

#El criterio por default es el de giny

# class sklearn.tree.DecisionTreeClassifier(*,criterion='gini',splitter='best',max_depth=None,min_samples_split=2,min_samples_leaf=1,min_weigth_fraction_leaf=0.0,max_features=None,random_state=None,max_leaf_nodes=None,min_impurity_decrease=0.0,class_weight=None,ccp_alpha=0.0)

arbol = DecisionTreeClassifier() #Crea un arbol de decision sin todavia preguntas

arbol.fit(X,y) #Lo entrena con el fit y pasandole los datos de entrenamiento. En esta linea se toman todas las decisiones. X son todos los atributos, y es la variable respuesta, el valor verdadero (unica), que es categorica. Entrenamiento del modelo

prediction = arbol.predict(X) #Se usa para predecir la linea y me genera la prediccion. Generamos las predicciones // llamamos al modelo
# %%


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import duckdb as dd
from matplotlib import ticker
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier


carpeta = "~/Descargas/"


titanic = pd.read_csv(carpeta + 'titanic_training.csv')

infoUsada = titanic[['Pclass','PassengerId','Age','SibSp', 'Parch', 'Fare']]
y = titanic['Survived']

arbol = DecisionTreeClassifier(max_depth=2)

arbol.fit(infoUsada, y)

Test = pd.read_csv(carpeta + 'test_titanic.csv') 

infoUsadaTest = Test[['Pclass','PassengerId','Age','SibSp', 'Parch', 'Fare']]

prediction = arbol.predict(infoUsadaTest)
# %%


#Representacion del arbol

from sklearn import tree

plt.figure(figsize=[20,10])
tree.plot_tree(arbol, feature_names= ['Pclass','PassengerId','Age','SibSp', 'Parch', 'Fare'], class_names =['Survived', 'No survived'] , filled = True, rounded = True, fontsize=8)

class_name =['Survived', 'No survived']




# %%KNN: 

from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris 
from sklearn import metrics
iris = load_iris(as_frame = True)

data = iris.frame
X = iris.data
Y = iris.target




model= KNeighborsClassifier(n_neighbors = 5) #Modelo en abstracto

model.fit(X,Y) #Entreno al modelo con los datos X e Y
Y_pred= model.predict(X) # me fijo que clases les asiga el modelo a mis datos

metrics.accuracy_score(Y, Y_pred)
metrics.confusion_matrix(Y, Y_pred)

# %%
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3) #70% para train y 30% para test

model= KNeighborsClassifier(n_neighbors= 5) #modelo en abstracto
model.fit(X_train, Y_train) #Entreno el modelo con los datos X_train e Y_train

Y_pred =model.predict(X_test) #me fijo que clases  les asigna el modelo a mis datos X_test

print('Exactitud del modelo:', metrics.accuracy_score(Y_test, Y_pred))


# %%

