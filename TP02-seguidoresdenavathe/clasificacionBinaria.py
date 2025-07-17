"""
Materia: Laboratorio de datos - FCEyN - UBA
Nombre del Grupo: Seguidores de Navathe
Autores  : Francisco Peix, Kamala Jimeno Leiton, Carolina Cuiña
Descripción: Clasificación Binaria
"""

# %% Imports utilizados en esta sección

import numpy as np
import pandas as pd
import duckdb as dd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# %% Funciones propias definidas para esta sección

#%% EJERCICIO 2A - construcción de dataframe con subconjuntos de imágenes de 0 y 1
# Armamos el nuevo dataframe solo con los 0 y 1, para esto, utilizamos el dataframe de mnistc ya normalizado previamente en la anterior sección

def construir_dataframe_0_1(mnistc_normalizado):
    df_solo_0_y_1 = mnistc_normalizado[mnistc_normalizado['labels'].isin([0, 1])]
    
    #Chequeamos con un gráfico de barras si es que está balanceado
    diferenciasCantidad = dd.sql("""
                                 SELECT labels, COUNT(*) AS cantVeces
                                 FROM df_solo_0_y_1
                                 GROUP BY labels
                                 """).df()
    sns.barplot(data=diferenciasCantidad, x='labels', y='cantVeces')
    plt.axhline(7000, color='red', linestyle='--', linewidth=2)
    plt.ylabel('Cantidad de imágenes', fontsize = 'medium')
    plt.xlabel('Label', fontsize = 'medium')
    
    #Usamos el separador de miles en el eje y
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.show()
    return df_solo_0_y_1


#%% EJERCICIO 2B - armado de los conjuntos de TRAIN y TEST
def pixeles_claros(promedios):
    # Lista para almacenar las columnas (píxeles) más claras
    pixeles_claros_lista = []
    
    # Definimos el umbral de claridad en 0.3 (el dataframe se encuentra normalizado)
    umbral_claridad = 0.3
    
    # Recorremos los DataFrames de promedios de cada número
    for promedio in promedios:
        
        # Trabajamos directamente con los valores del dataframe del promedio del digito determinado
        valores_promedio = promedio.values # Obtenemos la fila única del dataframe recorrido (promedio)
        
        # Identificamos las columnas (índices de los píxeles) que superan el umbral
        pixeles_claros = np.where(valores_promedio > umbral_claridad)[0]
        
        # Añadimos los píxeles claros a la lista
        pixeles_claros_lista.append(pixeles_claros)
        
    # Aplanamos la lista y eliminamos los posibles atributos (pixeles) duplicados
    return list(set(np.concatenate(pixeles_claros_lista)))


#Armamos conjuntos de train y test del dataframe
def armar_conjuntos_train_test(df_solo_0_y_1, promedios_0_y_1):
    
    X = df_solo_0_y_1.copy()
    X.columns = range(1,786)
    X = X[pixeles_claros(promedios_0_y_1)]
    Y = df_solo_0_y_1['labels']
    return train_test_split(X, Y, test_size=0.2, random_state=42) #Dejamos un 20% para test, y un 80% para train

#%% EJERCICIO 2C - ajuste de modelo KNN

# Función para buscar la accuracy más alta mediante un gráfico
def ajuste_modelo_knn(columnas, X_train, X_test, Y_train, Y_test):
     
    resultados = []
    for columna in columnas:
       train = X_train[columnas[columna]]
       test = X_test[columnas[columna]]

       modelo = KNeighborsClassifier(n_neighbors=5)
       modelo.fit(train, Y_train.values.ravel())
           
       Y_pred_train = modelo.predict(train)
       Y_pred_test = modelo.predict(test)
           
       score_train = accuracy_score(Y_train, Y_pred_train)
       score_test = accuracy_score(Y_test, Y_pred_test)
           
           
       #Agregamos los valores a la lista de resultados
       resultados.append({ 'Atributos': columna, 'Train Accuracy': score_train, 'Test Accuracy': score_test })

    dataResultados = pd.DataFrame(resultados)
    print(dataResultados)  
    return

#%% EJERCICIO 2D - Comparación de modelos de KNN utilizando distintos atributos y distintos valores de k

# Función para evaluar modelos con distintos valores de k
def comparacion_modelos_knn(columnas, X_train, X_test, Y_train, Y_test):
    # Inicializamos la lista para almacenar los resultados
    resultados = []
    print('A continuación, se presentan las comparaciones de los modelos con distintos valores de k')
    for columna in columnas:
        train = X_train[columnas[columna]]
        test = X_test[columnas[columna]]
        
        scores_train = []
        scores_test = []
        
        for k in range(2, 11):
            modelo = KNeighborsClassifier(n_neighbors=k)
            modelo.fit(train, Y_train.values.ravel())
            
            Y_pred_train = modelo.predict(train)
            Y_pred_test = modelo.predict(test)
            
            score_train = accuracy_score(Y_train, Y_pred_train)
            score_test = accuracy_score(Y_test, Y_pred_test)
            
            scores_train.append(score_train)
            scores_test.append(score_test)
            
            #Agregamos los valores a la lista de resultados
            resultados.append({
                'Atributos': columna,
                'k': k,
                'Train Accuracy': score_train,
                'Test Accuracy': score_test
            })
             
    # Convertimos los resultados en un dataframe para facilitar la comparación entre modelos
    dataResultados = pd.DataFrame(resultados)
    
    # Graficamos los resultados de las accuracy de cada modelo, para poder compararlas
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=dataResultados, x='k', y='Train Accuracy', hue='Atributos', marker='o', linestyle='-')
    sns.lineplot(data=dataResultados, x='k', y='Test Accuracy', hue='Atributos', marker='o', linestyle='--')
    plt.xlabel('Cantidad de vecinos')
    plt.ylabel('Accuracy Score')
    plt.grid()
    plt.show()
    return resultados
