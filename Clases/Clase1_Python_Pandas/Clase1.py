
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
    dados = []
    juego = ""
    for i in range (0, 5, 1):
        dados.append(random.randint(1,6))

    for numero in dados:
        if (cant_apariciones(numero, dados) == 5):
            juego = "Generala"
            
        elif(cant_apariciones(numero, dados) == 4):
            juego = "Poker"

        elif(todos_distintos(dados)):
            if ([3,4,5] in dados == False):
                juego = "Escalera"

        elif(cant_numeros(dados) == 2):
            juego = "Full"
          
    print(dados)
    return juego
             
def cant_apariciones(n, dados):
    res = 0
    for i in range(0, len(dados), 1):
        if (dados[i] == n):
                res += 1
    return res

def todos_distintos(dados):
    res: bool = True
    for i in range (0, len(dados)-1, 1):
        for j in range(i+1,  len(dados), 1):
            if (dados[i] == dados[j]):
                res = False
    return res

def cant_numeros(dados) -> int :
    dadosDistintos = []
    for dado in dados:
        if (dado in dadosDistintos == False):
            dadosDistintos.append(dado)
    return len(dadosDistintos)
           
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


def materias_cuatrimestre(nombre_archivo, n):
    res = []
    with open(nombre_archivo, 'rt') as file:
        encabezado = next(file)
        encabezadoList = encabezado.split(',')
        for line in file:
            datos_linea = line.split(',')
            if int(datos_linea[0]) == n:
                info = {}
                info[encabezadoList[0]] = datos_linea[0]
                info[encabezadoList[1]] = datos_linea[1]
                info[encabezadoList[2]] = datos_linea[2]
                res.append(info)
        return res
                 
print(materias_cuatrimestre('/Users\\franp\\Downloads\\cronograma_sugerido.csv', 3))            

# def registros(nombre_archivo):
#  lista = []
#  with open('/Users\\franp\\Downloads\\cronograma_sugerido.csv', 'rt') as f:
#      filas = csv.reader(f)
#      encabezado = next(filas)
#      for fila in filas:
#          registro = dict(zip(encabezado,fila)) # armo el diccionario de cada fila
#          lista.append(registro) # lo agrego a la lista
#      return lista
 
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
(3,2,4) #(cantidad de [[]], cantidad de [] por [[]], cantidad de elementos en [])
    
array_ejemplo.size # total de entradas 3*2*4
array_ejemplo.reshape((12,2)) # modifico la forma
array_ejemplo.reshape((4,6))
array_ejemplo.reshape((3,-1)) # 3 por lo que corresponda


#Ejercicio
import numpy as np
def  pisar_elemento(M,e):
    dimensiones = M.shape
    tamanio = M.size
    cambioValores = np.reshape(M, tamanio)

    for i in range (0, len(cambioValores),1):
        if (cambioValores[i] == e):
                cambioValores[i] = -1
    res = np.reshape(cambioValores, dimensiones)
    return res

M = np.array([[0, 1, 2, 3], [4, 5, 6, 7]])
e = 2        
print(pisar_elemento(M, e)) 

            #Pandas
import pandas as pd 

            #Data Frame
#Al principio si seteo un dataframe se me crea una columna mas que me indica cada numero de cada persona

#Crear un Data Frame con un Diccionario
df = pd.DataFrame(data = d) # creamos un df a partir de un diccionario
df.set_index('lu', inplace = True) # seteamos una columna como index

#Crear un Data Frame con un Array
Si tenemos datos numéricos en un array M:
M = np.array([[11, 1, -5, 3],[10, 5, 6, 7],[3, 8, 10, -1]])
df2 = pd.DataFrame(data = d) # creamos un df a partir de un array
df2 = pd.DataFrame(M, columns = ['a', 'b', 'c', 'd'], index = ['v1', 'v2', 'v3'])

#Cargar un Data Frame desde un archivo
fname = ‘directorio/cronograma_sugerido.csv’
df = pd.read_csv(fname)

#Ejemplo usando dataframes
import pandas as pd
archivo = '/Users\\franp\\Downloads\\arbolado-en-espacios-verdes.csv'
df = pd.read_csv(archivo, index_col = 2)

df.head()
df.tail()
df.info()
df.dtypes
df.columns
df.index
df.describe()
df[columnas]
df[columna]
df.iloc[i]
df.iloc[2:6]
df.loc[index_6]
df.loc[index_5, col2]
df.sample()
df.sample(n = 3)


df[df['tipo_folla'] == 'Jacarandás']
df[df['tipo_folla'] == 'Palmera']
