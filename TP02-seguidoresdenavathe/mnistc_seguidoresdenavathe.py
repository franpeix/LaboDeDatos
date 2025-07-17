#Descripción

"""
Materia: Laboratorio de datos - FCEyN - UBA
Nombre del Grupo: Seguidores de Navathe
Autores  : Francisco Peix, Kamala Jimeno Leiton, Carolina Cuiña
Descripción: Archivo principal (main)
Objetivo: Entrenamiento de modelos mediante la fuente de datos proporcionada
Aclaración: en este archivo no se encuentran los algoritmos que poseen ciertas funciones. Para tener más información sobre la implemetación de las funciones llamadas desde este archivo, se solicita que se traslade a los archivos correspondientes
"""

# %% Imports utilizados para poder ejecutar este archivo

#Importamos los archivos locales
from analisisExploratorio import (normalizar_mnistc, mostrar_imagen_con_encuadre, diferencia, muestraDigitos, desv_estandar, grafico_cantidad_apariciones)
from clasificacionBinaria import (construir_dataframe_0_1, armar_conjuntos_train_test, ajuste_modelo_knn, comparacion_modelos_knn)
from clasificacionMulticlase import (armar_conjuntos_dev_held_out, ajuste_modelo_arbol_decision, comparacion_seleccion_arboles_kfold, entrenamiento_modelo_elegido, matriz_confusion)

#Importamos las librerías
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%Carga de datos

print('Cargando la fuente de datos original... \n')

#Definimos la carpeta donde se encuentra el archivo
carpeta = Path.home() / 'Downloads' #En nuestro caso Downloads

# Definimos la ruta completa al archivo CSV
archivo_csv = carpeta / 'mnist_c_fog_tp.csv'

# Cargamos el archivo
mnistc = pd.read_csv(archivo_csv, index_col=0) #Establecemos la primer columna del dataset como índice

# %%

print('La ejecución del codigo puede demorar un tiempo, le solicitamos que tenga paciencia... \n')

def main():
    mnistc_normalizado = normalizar_mnistc(mnistc)

# %% APARTADO 1: ANÁLISIS EXPLORATORIO
    print('APARTADO 1: ANÁLISIS EXPLORATORIO \n')
    print('A continuación se presentan los gráficos utilizados para el ejercicio 1: \n')
#------------------------------------------------
    #ANEXO: GRÁFICO DE COMPARACIÓN DE CANIDAD DE CLASES PRESENTES
    grafico_cantidad_apariciones(mnistc)
#------------------------------------------------
    # EJERCICIO 1A
    #TODOS LOS NUMEROS
    promediosTodasColumnas = mnistc_normalizado.drop('labels', axis=1).mean()
    mostrar_imagen_con_encuadre(promediosTodasColumnas)
    
    #NUMERO 0
    data0 = mnistc_normalizado[mnistc_normalizado['labels'] == 0]
    promedios0 = data0.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios0)
    
    #NUMERO 1
    data1 = mnistc_normalizado[mnistc_normalizado['labels'] == 1]
    promedios1 = data1.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios1)
    
    #NUMERO 2
    data2 = mnistc_normalizado[mnistc_normalizado['labels'] == 2]
    promedios2 = data2.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios2)

    #NUMERO 3
    data3 = mnistc_normalizado[mnistc_normalizado['labels'] == 3]
    promedios3 = data3.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios3)

    #NUMERO 4
    data4 = mnistc_normalizado[mnistc_normalizado['labels'] == 4]
    promedios4 = data4.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios4)

    #NUMERO 5
    data5 = mnistc_normalizado[mnistc_normalizado['labels'] == 5]
    promedios5 = data5.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios5)

    #NUMERO 6
    data6 = mnistc_normalizado[mnistc_normalizado['labels'] == 6]
    promedios6 = data6.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios6)

    #NUMERO 7
    data7 = mnistc_normalizado[mnistc_normalizado['labels'] == 7]
    promedios7 = data7.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios7)

    #NUMERO 8
    data8 = mnistc_normalizado[mnistc_normalizado['labels'] == 8]
    promedios8 = data8.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios8)

    #NUMERO 9
    data9 = mnistc_normalizado[mnistc_normalizado['labels'] == 9]
    promedios9 = data9.drop('labels', axis= 1).mean()
    mostrar_imagen_con_encuadre(promedios9)
#------------------------------------------------
    # EJERCICIO 1B
    # Utilizando los numeros promedio, los restamos para poder ver claramente las diferencias entre ellos
    diferencia(promedios3, promedios1) #Refleja la imagen del promedio de imágenes con label 3 restada con la del promedio de imágenes con label 1
    diferencia(promedios8, promedios3)#Refleja la imagen del promedio de imágenes con label 3 restada con la del promedio de imágenes con label 1
#------------------------------------------------
    # EJERCICIO 1C
    #Muestra de algunos ceros
    muestraDigitos(data0, 0)
    desv_estandar(data0, 0)
    
    #Muestra de algunos cincos
    muestraDigitos(data5, 5)
    desv_estandar(data5, 5)
#------------------------------------------------
# %% APARTADO 2: CLASIFICACÓN BINARIA
    print('APARTADO 2: CLASIFICACÓN BINARIA \n')
    print('A continuación se presentan los resultados y gráficos utilizados para el ejercicio 2: \n')
#------------------------------------------------
    #EJERCICIO 2A
    df_solo_0_y_1 = construir_dataframe_0_1(mnistc_normalizado)
#------------------------------------------------
    #EJERCICIO 2B
    X_train, X_test, Y_train, Y_test = armar_conjuntos_train_test(df_solo_0_y_1, [promedios0, promedios1])
#------------------------------------------------
    #EJERCICIO 2C
    #Elegimos distintas combinaciones de píxeles claves para distinguir cada número
    print('EJERCICIO 2C: probamos con distintas combinaciones de píxeles para distinguir cada número \n')
    
    #Diccionario con distintos conjuntos de atributos (píxeles):
    columnas = {'centro vertical': [434, 406, 462], 
                'centro horizontal' : [412,413,414],
                'esta en el 0 y falta en el 1': [262, 407, 468],
                '5 atributos':[183, 350, 628, 153, 653],
                '10 atributos': [127,184,269,323,328,384,428,434,597,634]}
    
    print(f'Los conjuntos elejidos son: \n {columnas} \n')
    #Prueba de los distintos conjuntos
    ajuste_modelo_knn(columnas, X_train, X_test, Y_train, Y_test)
#------------------------------------------------
    #EJERCICIO 2D
    print('EJERCICIO 2D - Comparación de modelos de KNN utilizando distintos atributos y distintos valores de k \n')
    # Evaluación de modelos con diferentes conjuntos de atributos
    comparacion_modelos_knn(columnas, X_train, X_test, Y_train, Y_test)
#------------------------------------------------
# %% APARTADO 3: CLASIFICACIÓN MULTICASE
    print('APARTADO 3: CLASIFICACÓN MULTICASE \n')
    print('A continuación se presentan los resultados y gráficos utilizados para el ejercicio 3: \n')
#------------------------------------------------
    #EJERCICIO 3A
    promedios_numeros = [promedios0, promedios1, promedios2, promedios3, promedios4, promedios5, promedios6, promedios7, promedios8, promedios9]
    X_dev, X_eval, y_dev, y_eval = armar_conjuntos_dev_held_out(mnistc_normalizado, promedios_numeros, mnistc.labels)
#------------------------------------------------
    #EJERCICIO 3B
    ajuste_modelo_arbol_decision(X_dev, y_dev)
    
    print('\nComo se observa, a mayor profundidad, mayor exactitud posee el árbol. \n')
#------------------------------------------------
    #EJERCICIO 3C
    mejor_h = comparacion_seleccion_arboles_kfold(X_dev, y_dev)
#------------------------------------------------ 
    #EJERCICIO 3D
    print('EJERCICIO 3D- Entrenamiento del modelo elegido \n')
    print('Luego de haber realizado el K-foling con distintos valores de hiperparámetros (profundidad) en el ejercicio 3C, seleccionamos el que obtuvo mayor performance y entrenamos, con el conjunto de desarrollo, al modelo con este hiperparámetro. \n')
    score_arbol_elegido_dev, score_arbol_elegido_eval, y_pred_eval = entrenamiento_modelo_elegido(X_dev, y_dev, mejor_h, X_eval, y_eval)
    
    print('Por último, aquí se muestra la matriz de confusión obtenida con dicho modelo: \n')
    #EJERCICIO 3D: EXTRA
    matriz_confusion(y_eval, y_pred_eval)
#------------------------------------------------
    print('Espero que le haya gustado nuestro trabajo realizado.')
# %%

if __name__ == "__main__":
    main()


