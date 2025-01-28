
import random
prueba = random.random()
print (prueba)
random.seed(50)

nombre_archivo = 'datame.txt'
f = open(nombre_archivo, 'rt')
data = f.read()
f.close()


print(data)

f = open('datame.txt', 'rt') #Forma mas facil

path = '/home/Estudiante/Escritorio/' #Orden absoluto, le copio todo el path
f = open(path + 'datame.txt', 'rt')

patth_rel = "../Estudiante/Escritorio/" #Orden relativo, con .. subo una rama y para bajar le pongo el nombre del directorio

with open('/home/Estudiante/Escritorio/datame.txt', 'rt') as file:
    data = file.read()
    
data_nuevo = 'inicio de texto ' + data
data_nuevo = data_nuevo + 'cierre del texto'

datame = open("nuevonombre.txt", "w") #write mode
datame.write(data_nuevo)
datame.close()

open('nuevonombre.txt', 'rt')


# #Iterar sobre las lineas del archivo
# with open(nombre_archivo, 'rt') as file:
#     for line in file:
#         #procesar la linea
    
    

#Archivos CSV
nombre_archivo = '/home/Estudiante/Escritorio/cronograma_sugerido.csv'
with open(nombre_archivo, 'rt') as file:
    res = []
    encabezado = next(file) #agarra la primera parte de la iteracion, pasa a la siguiente linea. Además, tambien devuelve la lista que recorrió, es decir, la variable encabezado posee toda la primera linea de la lista, incluyendo las comas.
    for line in file:
        datos_linea = line.split(',')
        print(datos_linea[1])
        res.append(datos_linea[1])
print (res)



# f = open(nombre_archivo)
# filas = csv.reader(f)
# for fila in filas:
#     instrucciones
# f.close()

# f = open(nombre_archivo)
# filas = csv.reader(f)    
# encabezado = next(filas)



#Ejercicios de la Clase
import random
def generarla_tirar():
    res = []
    i:int = 0
    for i in range (0, 5, 1):
        res.append(random.randint(1,6))
    return res

print (generarla_tirar())

def lineas_estudiantes():
    nombre_archivo = '/home/Estudiante/Escritorio/datame.txt'
    with open(nombre_archivo, 'rt') as file:
        for line in file:
            oracion = line.split(' ')
            if 'estudiantes' in oracion:
                print(line)
                
print(lineas_estudiantes())

def cuantas_materias(n):
    with open('/home/Estudiante/Escritorio/cronograma_sugerido.csv', 'rt') as file:
        contador = 0
        next(file)
        for line in file:
            datos_linea = line.split(',')
            if int(datos_linea[0]) == n:
                contador += 1
    return contador
    
print(cuantas_materias(5))

"""
def materias_cuatrimestre(nombre_archivo, n):
    with open(nombre_archivo, 'rt') as file:
        for line in file:
"""         
 
import numpy as np
a = np.array([1,2,3,4,5,6]) #matriz de 1 dimension
b = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]]) #matriz de 2 dimensiones           
np.zeros() #matriz de ceros del tamaño indicado 
np.zeros((2,3))

np.linspace(0, 10, num=5) #me da 5 valores, de el cero al diez
np.concatenate((a,b)) #concatena a con b

array_ejemplo = np.array([[[0, 1, 2, 3],
[4, 5, 6, 7]],
[[3, 8, 10, -1],
[0, 1, 1, 0]],
[[3 ,3 ,3, 3],
[5, 5, 5, 5]]])
array_ejemplo.ndim # cantidad de dimensiones - 3
array_ejemplo.shape # cantidad de elementos en cada eje
(3,2,4)
    
array_ejemplo.size # total de entradas 3*2*4
array_ejemplo.reshape((12,2)) # modifico la forma
array_ejemplo.reshape((4,6))
array_ejemplo.reshape((3,-1)) # 3 por lo que corresponda


#Ejercicio
import numpy as np
def  pisar_elemento(M,e):
    dimensiones = M.shape
    i = 0
    for i in range (0, dimensiones[0],1):
        j = 0
        for j in range(0, dimensiones[1],1):
            if (M[i][j] == e):
                M[i][j] = -1
    return M

M = np.array([[0, 1, 2, 3], [4, 5, 6, 7]])
e = 2        
print(pisar_elemento(M, e)) 

#Pandas

#Data Frame
#Al principio si seteo un dataframe se me crea una columna mas que me indica cada numero de cada persona
import pandas as pd 
