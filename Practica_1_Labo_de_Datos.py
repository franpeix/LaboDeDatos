
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
        