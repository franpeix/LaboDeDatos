# 1) Denir una función leer_parque(nombre_archivo, parque) que abra el
# archivo indicado y devuelva una lista de diccionarios con la información del
# parque especicado. La lista debe tener un diccionario por cada árbol del parque
# elegido. Dicho diccionario debe tener los datos correspondientes a un árbol
# (recordar que cada la del csv corresponde a un árbol).
# Probar la función en el parque ‘GENERAL PAZ’ y debería dar una lista con 690
# árboles.

# import csv
# def leer_parque(nombre_archivo, parque):
#     res = []
#     with open(nombre_archivo, 'rt') as file:
#         filas = csv.reader(file)
#         encabezado = next(filas)
#         for fila in file:
#             datos_linea = fila.split(',')
#             if (datos_linea[10] == parque):
#                 # registro = dict(zip(encabezado,fila) # armo el diccionario de la fila
#                 registro= {}
#                 for i in range(0,len(encabezado)-1,1):
#                     registro[encabezado[i]] = datos_linea[i]
#                 res.append(registro)
#         return res

import csv    
def leer_parque(nombre_archivo, parque):
     lista = []
     with open(nombre_archivo, 'rt') as f:
         filas = csv.reader(f)
         encabezado = next(filas)
         for fila in filas:
             registro = dict(zip(encabezado,fila)) # armo el diccionario de cada fila
             if registro['espacio_ve'] == parque:
                 lista.append(registro) # lo agrego a la lista
     return lista
    
    
print(leer_parque('/Users\\franp\\Downloads\\arbolado-en-espacios-verdes.csv', 'GENERAL PAZ'))
print(len(leer_parque('/Users\\franp\\Downloads\\arbolado-en-espacios-verdes.csv', 'GENERAL PAZ')))                


import csv
def leer_parque(nombre_archivo, parque):
    lista_arboles = []
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            if fila['espacio_ve'] == parque:
                lista_arboles.append(fila)
    return lista_arboles

nombre_archivo = '/Users\\franp\\Downloads\\arbolado-en-espacios-verdes.csv'
parque_especificado = 'ANDES, LOS'
print(leer_parque(nombre_archivo, parque_especificado))
arboles_en_parque = leer_parque(nombre_archivo, parque_especificado) 
for arbol in arboles_en_parque:
    print(arbol)
    
# 2)  Escribir una función especies(lista_arboles) que tome una lista de árboles
# como la generada en el ejercicio anterior y devuelva el conjunto de especies (la
# columna 'nombre_com' del archivo) que figuran en la lista. 
def especies(lista_arboles):
    res = []
    for dic in lista_arboles:
        if ((dic['nombre_com'] in res) == False):
            res.append(dic['nombre_com'])
    return res
lista_arboles = leer_parque(nombre_archivo, parque_especificado)
print(lista_arboles)
print(especies(lista_arboles))


# 3) Escribir una función contar_ejemplares(lista_arboles) que, dada una
# lista como la generada con leer_parque(...), devuelva un diccionario en el
# que las especies sean las claves y tengan como valores asociados la cantidad de
# ejemplares en esa especie en la lista dada.
# Debería verse que en el parque General Paz hay 20 Jacarandás, en el Parque Los
# Andes hay 3 Tilos y en Parque Centenario hay 1 Laurel.
def contar_ejemplares(lista_arboles):
    res = {}
    for dic in lista_arboles:
        if (dic['nombre_com'] in res):
            res[dic['nombre_com']] += 1
        else:
            res[dic['nombre_com']] = 1
    return res

print(contar_ejemplares(lista_arboles))

# 4)Escribir una función obtener_alturas(lista_arboles, especie) que,
# dada una lista como la generada con leer_parque(...) y una especie de
# árbol (un valor de la columna 'nombre_com' del archivo), devuelva una lista con
# las alturas (columna 'altura_tot') de los ejemplares de esa especie en la lista.
def obtener_alturas(lista_arboles, especie):
    alturas:list(float) = []
    for dic in lista_arboles:
        if (dic['nombre_com'] == especie):
            alturas.append(dic['altura_tot'])
    return alturas

#Usar la función para calcular la altura promedio y altura máxima de los
#'Jacarandá' en los tres parques mencionados

def altura_prom_y_max(lista_alturas):
    suma_alturas: float = 0
    altMax: float = 0
    for altura in lista_alturas:
        suma_alturas += float(altura)
        if float(altura) > float(altMax):
            altMax = altura
    altProm = suma_alturas / len(lista_alturas)
    print(altProm)
    return altMax

especie = 'Jacarandá'    
print(obtener_alturas(lista_arboles, especie))
print(altura_prom_y_max(obtener_alturas(lista_arboles, especie)))
    
# 5)Escribir una función obtener_inclinaciones(lista_arboles, especie)
# que, dada una lista como la generada con leer_parque(...) y una especie
# de árbol, devuelva una lista con las inclinaciones (columna 'inclinacio') de
# los ejemplares de esa especie.
def obtener_inclinaciones(lista_arboles, especie):
    alturas = []
    for dic in lista_arboles:
        if (dic['nombre_com'] == especie):
            alturas.append(int(dic['inclinacio']))
    return alturas


print(obtener_inclinaciones(lista_arboles, especie))

# 6)Combinando la función especies() con obtener_inclinaciones() escribir
# una función especimen_mas_inclinado(lista_arboles) que, dada una
# lista de árboles devuelva la especie que tiene el ejemplar más inclinado y su
# inclinación.
def inclinacionMax(lista_inclinaciones):
    incMax = 0
    for inclinacion in lista_inclinaciones:
        if float(inclinacion) > incMax:
            incMax = inclinacion
    return incMax

def especimen_mas_inclinado(listArboles):
    res = (' ', 0)
    for esp in listArboles:
        inclinacionesEsp = obtener_inclinaciones(lista_arboles, esp)
        if (inclinacionMax(inclinacionesEsp) > res[1]):
            res = (esp, inclinacionMax(inclinacionesEsp))
    return res

listArboles = especies(lista_arboles)
print(especimen_mas_inclinado(listArboles))


# 7)Volver a combinar las funciones anteriores para escribir la función
# especie_promedio_mas_inclinada(lista_arboles) que, dada una lista
# de árboles devuelva la especie que en promedio tiene la mayor inclinación y el
# promedio calculado
def inclinacionProm(lista_inclinaciones):
    totInclinaciones = 0
    for inclinacion in lista_inclinaciones:
        totInclinaciones += inclinacion
    return float(totInclinaciones / len(lista_inclinaciones))


def especie_promedio_mas_inclinada(listArboles):
    res = (' ', 0)
    for esp in listArboles:
        inclinacionesEsp = obtener_inclinaciones(lista_arboles, esp)
        if (inclinacionProm(inclinacionesEsp) > res[1]):
            res = (esp, inclinacionProm(inclinacionesEsp))
    return res

print(especie_promedio_mas_inclinada(listArboles))

# Vamos a trabajar ahora también con el archivo de árboles en veredas. Queremos
# estudiar si hay diferencias entre los ejemplares de una misma especie según si crecen
# en un un parque o en la vereda. Para eso tendremos que juntar datos de dos bases de
# datos diferentes.

# Armar un DataFrame data_arboles_veredas que tenga solamente las siguiente
# columnas: 'nombre_cientifico', 'ancho_acera', 'diametro_altura_pecho',
# 'altura_arbol'

import pandas as pd
import numpy as np

fname = '/Users\\franp\\Downloads\\arbolado-publico-lineal-2017-2018.csv'
dfVer = pd.read_csv(fname)
dfPar = pd.read_csv(nombre_archivo)
 


# Sugerimos trabajar al menos con las siguientes especies seleccionadas:
# especies_seleccionadas = ['Tilia x moltkei', 'Jacaranda mimosifolia', 'Tipuana tipu']

especies_seleccionadas = ['Tilia x moltkei', 'Jacaranda mimosifolia', 'Tipuana tipu']

# Advertencia: El GCBA usa distintos nombres para especie, altura y diámetro según el
# dataset, por ejemplo 'altura_tot' en uno y 'altura_arbol' en otro. Los nombres cientícos
# varían de un dataset al otro. Por ejemplo 'Tipuana Tipu' se transforma en 'Tipuana tipu'.

# Proponemos los siguientes pasos para comparar los diámetros a la altura del pecho de
# las tipas en ambos tipos de entornos.

# 8)Para cada dataset, armar otro seleccionando solamente las las correspondientes
# a las tipas (llamalos df_tipas_parques y df_tipas_veredas, respectivamente) y las
# columnas correspondientes al diámetro a la altura del pecho y alturas. Usar como
# copias (usando .copy()) para poder trabajar en estos nuevos dataframes sin
# modicar los dataframes grandes originales. Renombrar las columnas necesarias
# para que se llamen igual en ambos dataframes.

df_tipas_parques = dfPar.copy()
df_tipas_veredas = dfVer.copy()

df_tipas_veredas = df_tipas_veredas.drop(['long', 'lat', 'nro_registro', 'tipo_activ', 'comuna', 'manzana', 'calle_nombre', 'calle_altura', 'calle_chapa', 'direccion_normalizada', 'ubicacion', 'estado_plantera', 'nivel_plantera', 'ubicacion_plantera'], axis = 1) # tiro las columnas

df_tipas_parques = df_tipas_parques.drop(['long', 'lat', 'id_arbol', 'inclinacio', 'id_especie', 'nombre_com', 'tipo_folla', 'espacio_ve', 'ubicacion', 'nombre_fam', 'nombre_gen', 'origen', 'coord_x', 'coord_y'], axis = 1)

df_tipas_parques = df_tipas_parques.rename(columns={"altura_tot": "altura_arbol", "nombre_cie": "nombre_cientifico", "diametro": "diametro_altura_pecho"}) #cambiar los nombres de las columnas

# 9) Agregar a cada dataframe (df_tipas_parques y df_tipas_veredas) una columna
# llamada 'ambiente' que en un caso valga siempre 'parque' y en el otro caso
# 'vereda'.

# Agregar columna 'ambiente' al dataframe de parques
df_tipas_parques['ambiente'] = 'parque'

# Agregar columna 'ambiente' al dataframe de veredas
df_tipas_veredas['ambiente'] = 'vereda'

# 10) Concatenar los dataframes
df_info_junta = pd.concat([df_tipas_parques, df_tipas_veredas])

# 11) Explorar y analizar sobre la cuestión planteada:
# ¿Hay diferencias entre los ejemplares de una misma especie según si crecen en
# un un parque o en la vereda?
df_info_junta = df_info_junta.replace({'nombre_cientifico': {'Tipuana Tipu': 'Tipuana tipu','Jacarandá mimosifolia': 'Jacaranda mimosifolia', 'Tilia viridis subsp. x moltkei': 'Tilia x moltkei'}}) # modifico todas las apariciones de las plantas
df_info_junta[df_info_junta['nombre_cientifico'] == 'Tipuana tipu']
df_info_junta[df_info_junta['nombre_cientifico'] == 'Jacaranda mimosifolia']
df_info_junta[df_info_junta['nombre_cientifico'] == 'Tilia x moltkei']


