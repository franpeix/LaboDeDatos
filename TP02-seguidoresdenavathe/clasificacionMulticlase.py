"""
Materia: Laboratorio de datos - FCEyN - UBA
Nombre del Grupo: Seguidores de Navathe
Autores  : Francisco Peix, Kamala Jimeno Leiton, Carolina Cuiña
Descripción: Clasificación Multiclase
"""

# %% Imports utilizados en esta sección

from clasificacionBinaria import (pixeles_claros) #Función utilizada en el ejercicio 2

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier

# %% Funciones propias definidas para esta sección

#%% EJERCICIO 3A- armado de los conjuntos de dev y held out

def armar_conjuntos_dev_held_out(mnistc_normalizado, promedios_numeros, labels):
    X = mnistc_normalizado.copy()
    X.columns = range(1,786)
    X = X[pixeles_claros(promedios_numeros)]
    y = labels
    return train_test_split(X, y, random_state=1, test_size=0.25)

#%% EJERCICIO 3B- ajuste de modelo de arbol de decisión
def ajuste_modelo_arbol_decision(X_dev, y_dev):
    
    scores = []
    
    for altura in range(1, 11):
        arbol_elegido = DecisionTreeClassifier(max_depth=altura)
        arbol_elegido.fit(X_dev, y_dev)
        y_pred = arbol_elegido.predict(X_dev)
        score_arbol_elegido_dev = accuracy_score(y_dev, y_pred)
        print(f'Accuracy del árbol con altura {altura}: {score_arbol_elegido_dev}')
        scores.append(score_arbol_elegido_dev)

    
    #Graficamos los resultados obtenidos
    plt.plot(range(1, 11), scores, marker='o', linestyle='dashed', color='b')
    plt.xlabel('Profundidad del árbol de desarrollo')
    plt.ylabel('Accuracy Score')
    plt.grid()
    plt.show()
    
    return


#%% EJERCICIO 3C- comparación y selección de distintos árboles, mediante el uso de K-folding
def comparacion_seleccion_arboles_kfold(X_dev, y_dev):
    
    alturas = range(1, 11)
    nsplits = 8  # Cantidad de particiones del conjunto, del mismo tamaño
    kf = KFold(n_splits=nsplits)
    
    resultados = np.zeros((nsplits, len(alturas)))  # Inicializamos la matriz con todos 0
    
    
    for i, (train_index, test_index) in enumerate(kf.split(X_dev)):
        kf_X_train, kf_X_test = X_dev.iloc[train_index], X_dev.iloc[test_index]
        kf_y_train, kf_y_test = y_dev.iloc[train_index], y_dev.iloc[test_index]
        for j, hmax in enumerate(alturas):
            arbol = DecisionTreeClassifier(max_depth=hmax)
            arbol.fit(kf_X_train, kf_y_train)
            pred = arbol.predict(kf_X_test)
            score = accuracy_score(kf_y_test, pred)
            resultados[i, j] = score

    # Calculamos el promedio de las métricas obtenidas (promedio scores sobre los folds)
    scores_promedio = resultados.mean(axis=0)
    
    # Elegimos la mejor profundidad basada en validación cruzada
    mejor_h = 7
    
    
    #Graficamos lo hallado
    plt.figure(figsize=(8, 5))
    plt.plot(alturas, scores_promedio, marker='o', linestyle='dashed', color='b', label="Accuracy promedio")
    plt.axvline(mejor_h, color='r', linestyle='--', label=f"Mejor hmax = {mejor_h}")
    plt.xlabel("Profundidad del Árbol")
    plt.ylabel("Accuracy Score Promedio en Validación Cruzada")
    plt.legend()
    plt.grid()
    plt.show()
    
    return mejor_h


#%% EJERCICIO 3D- Entrenamiento del modelo elegido

#Entrenamos al mejor modelo obtenido segun lo hallado en el proceso de K-folding para observar la performance del mismo
def entrenamiento_modelo_elegido(X_dev, y_dev, mejor_h, X_eval, y_eval):
    resultados = []
    
    arbol_elegido = DecisionTreeClassifier(max_depth=mejor_h)
    arbol_elegido.fit(X_dev, y_dev)
    y_pred = arbol_elegido.predict(X_dev)
    
    score_arbol_elegido_dev = accuracy_score(y_dev, y_pred)
    
    # Probamos el modelo elegido y entrenado en el conjunto eval
    y_pred_eval = arbol_elegido.predict(X_eval)
    score_arbol_elegido_eval = accuracy_score(y_eval, y_pred_eval)
    
    #Reportamos la performance hallada  
    resultados.append({ 'conjunto': 'conjunto de Desarrollo (dev)', 'Accuracy score promedio': score_arbol_elegido_dev})
    resultados.append({ 'conjunto': 'conjunto de Evaluación (held-out)', 'Accuracy score promedio': score_arbol_elegido_eval})
    dataResultados = pd.DataFrame(resultados)
    print(dataResultados)
    
    return score_arbol_elegido_dev, score_arbol_elegido_eval, y_pred_eval


#%% EJERCICIO 3D: EXTRA
# Matriz de confusión : para poder visualizar de una manera más óptima la clasificación realizada por el modelo, implementamos una matriz de confusión
#Con esta, podemos evaluar los distintos tipos de errores que fueron obtenidos para clasificar las imágenes presentes
def matriz_confusion(y_eval, y_pred_eval):
    matriz_conf = confusion_matrix(y_eval, y_pred_eval)
    
    # Visualizamos la matriz de confusión
    plt.figure(figsize=(6, 4))
    sns.heatmap(matriz_conf, annot=True, fmt="d", cmap="Blues", xticklabels=set(y_eval), yticklabels=set(y_eval))
    plt.xlabel("Predicción")
    plt.ylabel("Real")
    plt.title("Matriz de Confusión")
    plt.show()
    return matriz_conf
