"""
Materia: Laboratorio de datos - FCEyN - UBA
Nombre del Grupo: Seguidores de Navathe
Autores  : Francisco Peix, Kamala Jimeno Leiton, Carolina Cuiña
Descripción: Análisis Exploratorio de los datos
"""

# %% Imports utilizados en esta sección

import duckdb as dd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import seaborn as sns

# %% Funciones propias definidas para esta sección

# %% Función: Normalizacion del dataframe fila por fila
#Esta función también será utilizada en las otras secciones, pero decidimos definirla en esta, pues corresponde a la primera parte del trabajo; mientras que los otros apartados utilizan esta función la cual ya se encontrará definida
def normalizar_mnistc(archivo):
    # Inicializamos una lista para almacenar las filas normalizadas
    imagenes_normalizadas = []
    
    # Iteramos sobre cada fila (imagen) de la fuente
    for index, row in archivo.iterrows():
        # Excluimos la columna 'labels', pues no la queremos normalizar a esta
        valores_sin_normalizar = row[:-1] #Nos quedamos con las 784 columnas (pixeles) que normalizaremos, excluyendo a la ultima columna, 'labels'
        label = row['labels']#Nos guardamos la label asignada a la fila recorrida
        
        #Aplicamos la fórmula de normalización
        valores_normalizados = (valores_sin_normalizar - np.min(valores_sin_normalizar)) / (np.max(valores_sin_normalizar) - np.min(valores_sin_normalizar))
        
        #Volvemos a agregar la columna 'labels' al final
        fila_normalizada = np.append(valores_normalizados, label)
        
        #Agregamos la fila normalizada a la lista para poder luego reconstruir el dataFrame
        imagenes_normalizadas.append(fila_normalizada)
    
    #Convertimos la lista de filas normalizadas a mnistc nuevamente, pero esta vez normalizado
    columnasMnistc = list(archivo.columns)
    return pd.DataFrame(imagenes_normalizadas, columns=columnasMnistc)



# %% EJERCICIO 1A - atributos relevantes y no relevantes para predecir el número de la imagen

#Función para mostrar la imagen con el encuadre de los píxeles más claros

def mostrar_imagen_con_encuadre(promedio):
    
    # Convertimos los promedios de cada atributo en una imagen de 28x28
    img = np.array(promedio).reshape((28, 28))
    
    # Encontramos las coordenadas de los píxeles más claros. Definimos que nuestro umbral para verificar esto es el valor de 0.3 en el dataset normalizado. Este umbral fue definido mediante la observacion de los valores que poseía cada dato
    claros = np.argwhere(img > 0.3)
    
    # Buscamos el rectángulo mínimo que contiene todos los píxeles claros
    x_min, y_min = claros.min(axis = 0)
    x_max, y_max = claros.max(axis = 0)
    
    # Mostrar la imagen con el encuadre de los píxeles más claros
    plt.imshow(img, cmap='gray')
    plt.title('Promedio de los Píxeles')
    plt.colorbar()
    
    #Encuadramiento utilizando los valores ya obtenidos
    #Conectamos a las 4 esquinas y luego cerramos la figura, para ello, se aclara lo siguiente:
    # Esquina Superior Izquierda (y_min, x_min)
    # Esquina Superior Derecha (y_max, x_min)
    # Esquina Inferior Derecha (y_max, x_max)
    # Esquina Inferior Izquierda (y_min, x_max)
    # Volvemos a la Esquina Superior Izquierda (y_min, x_min) para cerrar el contorno
    plt.plot([y_min, y_max, y_max, y_min, y_min], [x_min, x_min, x_max, x_max, x_min], color='red')
    plt.show()


#%% EJERCICIO 1B - parecidos entre distintos dígitos

# Utilizando los numeros promedio, los restamos para poder ver claramente las diferencias entre ellos    
def diferencia(prom1, prom2):
    # Calculamos la diferencia entre los dos promedios
    diferencia = prom1 - prom2
    
    # Aseguramos que los valores negativos sean 0
    diferencia[diferencia < 0] = 0
    
    # Convertimos a array y redimensionar a 28x28
    img_diff = np.array(diferencia).reshape((28, 28))
    
    # Mostramos la imagen de la diferencia
    plt.imshow(img_diff, cmap='gray')
    plt.colorbar()
    plt.title('Diferencia entre Promedios Normalizados')
    plt.show()


# %% EJERCICIO 1C - similitud entre imágenes de un mismo dígito

#Muestra de imagenes del mismo digito
def muestraDigitos(dataN, digito):
    dataNSinLabel = dataN.drop(['labels'], axis=1)
    fig, axes = plt.subplots(4, 5, figsize=(12, 5))
    axes = axes.ravel()
    for i in range(20):
        image = dataNSinLabel.iloc[i].values.reshape(28, 28)
        axes[i].imshow(image, cmap='gray')
        axes[i].set_title(f'Dígito {digito} - Ejemplo {i+1}')
        axes[i].axis('off')
        
    #Graficamos las imágenes obtenidas
    plt.tight_layout() #Para que los sublplots queden acomodados correctamente en el area de la figura
    plt.show()



#Gráfico que representa de desviación estándar del dígito determinado
def desv_estandar(dataN, digito):
    
    # Calculamos la desviación estándar de cada fila
    desviaciones_estandar = dataN.std(axis=1)
    
    # Creamos un DataFrame con las desviaciones estándar para graficar
    df_desviaciones = pd.DataFrame({'Desviación Estándar': desviaciones_estandar})
    
    # Graficamos las desviaciones estándar
    plt.figure(figsize=(10, 6))
    sns.histplot(df_desviaciones['Desviación Estándar'], bins=30, kde=True)
    plt.xlabel('Desviación Estándar')
    plt.ylabel('Frecuencia')
    plt.show()


#%% ANEXO: GRAFICO DE COMPARACIÓN DE CANIDAD DE CLASES PRESENTES
#Comparación de cantidades de apariciones de cada dígito dentro del dataset
def grafico_cantidad_apariciones(mnistc):
    diferenciasCantidad = dd.sql("""
                                 SELECT labels, COUNT(*) AS cantVeces
                                 FROM mnistc
                                 GROUP BY labels
                                 """).df()
    sns.barplot(data=diferenciasCantidad, x='labels', y='cantVeces')
    plt.axhline(7000, color='red', linestyle='--', linewidth=2)
    plt.title('Barplot con Línea de Corte en 7000')
    plt.ylabel('Cantidad de imágenes', fontsize = 'medium')
    plt.xlabel('Label', fontsize = 'medium')
    
    
    #Usamos el separador de miles en el eje y
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.show()
    
