#Descripcion

"""
Materia: Laboratorio de datos - FCEyN - UBA
Nombre del Grupo: Seguidores de Navathe
Autores  : Francisco Peix, Kamala Jimeno Leiton, Carolina Cuiña
Descripción: Código utilizado para trabajar con las fuentes de datos brindadas
Objetivo: 
"""

# %% Imports


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

# %%Carga de datos

carpeta = '~/Descargas/'

mnistc = pd.read_csv(carpeta + 'mnist_c_fog_tp.csv', index_col=0)

#La cantidad de datos corresponde con 70000 filas y 785 columnas, pero, al haber una columna la cual hace referencia a el numero que se esta representando en la determinada fila ('labels'), se presentan 

#Cada columna posee como nombre a el numero respectivo a la posicion en la que se encuentra (asumiendo que primer columna posee el valor 0) con excepcion de la ultima, cuyo nombre es 'labels' 

# %% Funciones propias definidas

# %% Codigo fuera de funciones


mnistc_sin_labels= mnistc.drop(['labels'], axis=1)
#X = mnistc_sin_labels.columns

###########
# Plot imagen

img = np.array(mnistc_sin_labels.iloc[12]).reshape((28,28))
plt.imshow(img, cmap='gray')
plt.show()
############



