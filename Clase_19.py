#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:02:55 2025

@author: Estudiante
"""

#Statquest
# %%


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
# %%Aprendizaje no supervisado: se busca etender los datos sin saber que es lo que se espera de ellos, tal vez no tengo una pregunta especifica, pero quiero saber como se relacionan las variables entre si.
#Vamos a ver Clustering-agrupamiento: metodos para encontrar subgrupos homogeneos dentro del conjunto entero de los datos.
#La idea es encontrar grupos de instancias a partir de informacion en los datos que describan objetos y sus relaciones.
#Las instancas de un cluster (grupo) tienen que ser similares entre si; y diferentes a las de los otros clusters. Maximisamos las diferencias extra-grupo y minimizamos las diferencias inter-grupo.
#Cada cluster tiene al menos un datos y cada dato tiene unicamente un claster asignado.
#K-means: metodo iterativo, necesita un numero de clusters determinado (hiperparametro del modelo). Se empieza eligiendo alearoriamente determinadas ubicaciones en mis datos, que se van a llamar 'centroides'. Cada dato va a pertenecer a uno de los clusters asignados a cada centroide. Una vez hecho esto, se actualiza y se calcula el centroide dentro de cada grupo, agarra los puntos de cada centoide, calcula el promedio y ese va a ser el nuevo centroide.
#Es decir, despues de asignar los primeros centroides y sus cluster (agrupar), los centroides se recalculan teniendo en cuenta los puntos que estan asignados en cada cluster, esto es, el promedio de los puntos que se encuentran dentro del cluster (el promedio de cada eje, cada atributo, que me devolvera una coordenada), por ejemplo tengo un cluster rojo, calculo el promedio de los rojos y ese va a ser mi nuevo centroide.
#Luego, hay que volver a asignar los clusters a los nuevos centroides, pues al cambiar los centroides los puntos tal vez no se encuentren tan cerca como antes.
#A cada muestra, le calculo la distancia de este a cada cluster. Sumo la distancia al cuadrado de todos los puntos a su determinado centroide del cluster. En cada paso del K-means (tanto en la asignacion como en cada iteracion), voy a estar bajando esta metrica
#Para determinar el mejor k, usamos la misma metrica que con KNN: graficamos WCSS para un rango k y usamos el metodo del codo; pero en este caso para cada k se hace un promedio, pues como son asignados los centroides al azar no sabemos bien, cada grafico variaria.
#Este metodo tiene problemas con los datos atipicos (outliers). Otro problema que tiene  es cuando los datos no tienen forma esferica; o tienen tamaños o densidades muy distintas.
#Ventajas: es rapido, sencillo de implementar y puede ser util en general
#Desventajas: outliers, formas raras, tamaños de clusters, sensibilidad a los valores iniciales de los centroides, depende de un k.

#DBSCAN
#Basado en densidad, tiene dos hiperparametros, que tambien son dificiles de elegir. Va a tratar de buscar un punto nucleo y ahi va a iniciar el primer cluster, va a imcluir dentro de este cluster a todos lo puntos que esten dentro de la discancia determinada. Luego, con los puntos restantes si quedan, hace de nuevo el paso de buscar el punto nucleo para iniciar el segundo cluster, y asi...
#Va a llegar un momento en el que ya esten los clusters asignados; si todavia hay puntos sin asignar, se los consideran outliers
#Para cada observacion miramos el numero de puntos a una distancia maxima o menos (Eps)
#Los nucleos se van esparciendo segun la distancia hasta que ya no se pueda incluir a ningun punto mas dentro de el cluster
#Ventajas: no asume ningun numero de clusters, clusters con formas arbitrarias, robusto detectando outliers.
#Desventajas: diferencias de densidades, dificil determinar los parametros (minPts y eps); y no es bueno para datasets muy grandes o en muchas dimensiones.


#Clustering jerarquico:
    #Ventajas:
        #No asume ningun numero de clusters (se pueden obtener cortando el dendograma en el nivel deseado
        # Genera un dendograma: util para interpretar
        # Pueden corresponder a taxonomias (ej reino animal)
                                            
    #Desventajas:
        # Sensible a ruido y outliers
        # Computacionalmente caro en tiempo y espacio
        # No siempre la estructura jerarquica es la mas adecuada. El clustering jerarquico, va a estar recortando un corte en dos, va a ser una subdivision de el corte anterior, no modifica el corte anterior que tenia. Esto le da cierta rigidez en los clusters que antes tenia
        # Optimiza localmente, no de manera global
#Dendograma
#Se genera una especie de arbol, donde abajo tengo tantas hojas como puntos del dataset
#La altra representa la escala a la que se unen los clusters. La altura importa
#Una vez hecho el Dendograma, se puede cortar la altura y asi generar el clustering, mientras mas abajo del arbol, mayor cantidad de clusters


#Criterios de cercania
#La distancia entre dos puntos es la cercania entre ellas.
#Distancia entre clusters: 1)Minima
#2)Mayor
#3) Promedio de todos contra todos
#4)Utilizo los centroides


#Estos metodos estan teniendo en cuenta la distancia, dependen de la escala de los datos y estan pendiente de la distancia a la que estos se encuentran. Hay que tener en cuenta que con distintas escalas me va a afectar como estan mis atributos. Una cosa que hicimos era normalizar a el dataframe en uno nuevo para poder graficar mejor los datos
# %%


import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
#from statsmodels.datasets import get_rdataset
#from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import datasets
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram , cut_tree

from sklearn.preprocessing import StandardScaler

#%%
np.random.seed (0);
X = np.random.standard_normal ((50 ,2));
X[:25 ,0] += 3; #a los ultimos 25 puntos, en la coordenada 0 los corro 3 valores
X[:25 ,1] -= 4; #a los ultimos 25 puntos, en la coordenada 1 los corro 4 valores
#X[25:50, 1] += 10; #a los 25 puntos que estan en el medio, en la coordenada 1 sumo 10
X[50:, 0] += 6;  #a los que vienen despues del 50 (los ultimos 25), en la primera coordenada sumales 6 (son los mismos datos que al principio)
X[50:, 1] += 6 #a los gglomerativeClusteringque vienen despues del 50 (los ultimos 25), en la primera coordenada sumales 6 (son los mismos datos que al principio)


#%% Reescalar los datos, normalizarlos
scaler = StandardScaler()
scaler.fit(X)
Xn= scaler.transform(X)


fig , ax = plt.subplots (1, 1, figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1])


kmeans = KMeans(n_clusters = 2, random_state = 2, n_init = 20) #n_init : ya esta pensado para promediar tantas veces, lo hace 20 veces y se queda con el mejor, 2 clusters 20 veces, lo hace 20 veces y se queda con el mejor.
kmeans.fit(X)
kmeans.labels_
#%%
kmeans = KMeans(n_clusters = 2, random_state = 2, n_init = 20) #n_init : ya esta pensado para promediar tantas veces, lo hace 20 veces y se queda con el mejor, 2 clusters 20 veces, lo hace 20 veces y se queda con el mejor.
kmeans.fit(X)
kmeans.labels_
#%%

fig , ax = plt.subplots (1, 1, figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=kmeans.labels_)
ax.set_title("K-Means Clustering Results with K=2");

#%%
kmeans = KMeans(n_clusters =3, random_state =3, n_init =20)
kmeans.fit(X)
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=kmeans.labels_)
ax.set_title("K-Means Clustering Results with K=3");


#%%
kmeans1 = KMeans(n_clusters =3, random_state =3, n_init =1)
kmeans1.fit(X) 
kmeans20 = KMeans(n_clusters =3, random_state =3, n_init =20)
kmeans20.fit(X);

kmeans1.inertia_ , kmeans20.inertia_ #La medida WCSS a la que llega cada cluster 

#%%
dbclust = DBSCAN(eps=0.5, min_samples=3) #eps es la distancia en la cual se van moviendo el area donde se asignan a los puntos los clusters . min_samples es la cantidad minima de puntos para que lo considere como un cluster

dbclust.fit(X)
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=dbclust.labels_)
ax.set_title("DBSCAN Results");
#%% Cambio el eps
dbclust = DBSCAN(eps=1, min_samples=3) #eps es la distancia en la cual se van moviendo el area donde se asignan a los puntos los clusters . min_samples es la cantidad minima de puntos para que lo considere como un cluster

dbclust.fit(X)
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=dbclust.labels_)
ax.set_title("DBSCAN Results");

# %%




#%% Hierarical clustering, clustering gerarquico
HClust = AgglomerativeClustering
hc_comp = HClust( distance_threshold =0, n_clusters=None , linkage='complete') #el linkage determina el criterio de cercania de los clusters. Cuando la cantidad de clusters dice None , significa que me hace todo el camino
hc_comp.fit(X)
#%%
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=hc_comp.labels_) #El color que determina las etiquetas asignadas
ax.set_title("Agglomerative Clustering Results");
#%%
HClust = AgglomerativeClustering
hc_comp = HClust( distance_threshold =None, n_clusters=3 , linkage='complete')
hc_comp.fit(X)
#%%
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=hc_comp.labels_)
ax.set_title("Agglomerative Clustering Results");
#%%
HClust = AgglomerativeClustering
hc_comp = HClust( distance_threshold = None, n_clusters=2 , linkage='complete')
hc_comp.fit(X)
#%%
fig , ax = plt.subplots(figsize =(8 ,8))
ax.scatter(X[:,0], X[:,1], c=hc_comp.labels_)
ax.set_title("Agglomerative Clustering Results");
#%%
hc_avg = HClust(distance_threshold =0, n_clusters=None , linkage='average'); 
hc_avg.fit(X)
hc_sing = HClust(distance_threshold =0, n_clusters=None , linkage='single');
hc_sing.fit(X);

#%%
D = np.zeros ((X.shape [0], X.shape [0]));
for i in range(X.shape [0]):
    x_ = np.multiply.outer(np.ones(X.shape [0]) , X[i])
    D[i] = np.sqrt(np.sum((X - x_)**2, 1));
hc_sing_pre = HClust( distance_threshold =0, n_clusters=None , metric='precomputed', linkage='single')
hc_sing_pre.fit(D)

#%%
def compute_linkage(model):
    # Create linkage matrix 
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    return linkage_matrix
    

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

#%%

hc_comp = HClust( distance_threshold =0, n_clusters=None , linkage='complete')
hc_comp.fit(X)

linkage_comp = compute_linkage(hc_comp)
dendrogram(linkage_comp)

plt.figure(figsize = (15,15))
plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
#plot_dendrogram(hc_comp, truncate_mode="level", p=3)
dendrogram(linkage_comp, color_threshold =4, above_threshold_color ='black');

#plot_dendrogram(hc_comp)
plt.show()

#%%
cargs = {'color_threshold':-np.inf , 'above_threshold_color':'black'}
linkage_comp = compute_linkage(hc_comp)
fig , ax = plt.subplots(1, 1, figsize =(12, 8))
dendrogram(linkage_comp , ax=ax , ** cargs);

#%%
fig , ax = plt.subplots (1, 1, figsize =(8, 8))
dendrogram(linkage_comp , ax=ax , color_threshold =4, above_threshold_color ='black');

#%%
cut_tree(linkage_comp , n_clusters =4).T

#%%
cut_tree(linkage_comp , height = 3)

#%%
scaler = StandardScaler ()
X_scale = scaler.fit_transform(X)
hc_comp_scale = HClust( distance_threshold =0,
n_clusters=None ,
linkage='complete').fit(X_scale)
linkage_comp_scale = compute_linkage(hc_comp_scale)
fig , ax = plt.subplots (1, 1, figsize =(8, 8))
dendrogram(linkage_comp_scale , ax=ax , ** cargs)
ax.set_title("Hierarchical Clustering with Scaled Features");

#%%
######## OTROS DATOS SINTETICOS
#%%
seed = 75
n_samples = 500
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=0.05, random_state=seed)

noisy_circles = datasets.make_circles(n_samples=n_samples, factor=0.5, noise=0.05, random_state=seed)

blobs = datasets.make_blobs(n_samples=n_samples, random_state=seed)

varied = datasets.make_blobs(n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5], random_state=seed) #Para cambiarles a distintos grupitos la densidad
#%%
for dataset in [noisy_moons, noisy_circles, blobs, varied]:
    X, y = dataset
    plt.figure()
    plt.scatter(X[:, 0], X[:, 1], s=10)
    

    plt.xticks(())
    plt.yticks(())
    plt.show()

#%%
X, y = noisy_circles
plt.figure()
plt.scatter(X[:, 0], X[:, 1], s=10)


plt.xticks(())
plt.yticks(())
plt.show()


# %%
