# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Autores  : Francisco Peix, Kamala Jimeno Leiton, Carolina Cuiña
Descripción: Código utilizado para trabajar con las fuentes de datos brindadas
Objetivo: Procesar y analizar los datos presentas; y con ellos diagnosticar si existe cierta relación entre la cantidad de CC y EE en los departamentos del país
"""

# Importamos bibliotecas
import pandas as pd
import duckdb as dd
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression


#%%===========================================================================
# Importamos los datasets que vamos a utilizar en esta investigación
#=============================================================================

carpeta = "~/Downloads/TP-labo\\TP01-seguidoresdenavathe/TablasOriginales/"

padronPoblacion = pd.read_excel(carpeta + "padron_poblacion.xlsx", skiprows= 12) 
padronEstEducativos = pd.read_excel(carpeta + "2022_padron_oficial_establecimientos_educativos.xlsx", skiprows= 5)
centrosCulturales = pd.read_csv(carpeta + "centros_culturales.csv") 



#%%===========================================================================
# PROCESAMIENTO DE DATOS: A continuación, se muestran todos los pasos que seguimos apara poder trabajar con las fuentes brindadads de manera eficiente, y así poder realizar el analisis de los datos que estas poseían. En esta seccion no solo se trabaja con ellas, sino que también se produce la creacion de las Tablas del Modelo Entidad-Relacion
#=============================================================================

# %% CREACION DE DATAFRAME: censo

def procesar_censo(ruta_archivo, skiprows):
    # Lee el archivo Excel de un DataFrame, saltando las filas especificadas
    fuente_Censo = pd.read_excel(ruta_archivo, header=None, skiprows=skiprows)
    
    # Lista para almacenar los datos de todas las áreas
    datos_areas = []
    
    # Inicializamos variables
    area_nombre = ''  # Nombre del área que se esta recorriendo
    area_identificador = ''  # Identificador del área que se esta recorriendo
    columns = ['Edad', 'Casos', '%', 'Acumulado %', 'Area', 'Id_area']  # Nombres de las columnas del DataFrame nuevo resultante
    
    # Recorremos fila por fila
    for index, fila in fuente_Censo.iterrows():
        if fila.dropna().empty:
            continue  # Omitimos filas en blanco
            
        # Recorremos celda por celda en la fila actual
        for i, celda in fila.items():
            # Verificamos si la celda contiene la palabra 'area'
            if pd.notna(celda) and isinstance(celda, str) and 'area' in celda.lower():
                partes = celda.split() # Dividimos la cadena en palabras
                area_identificador = partes[-1]  # Obtenemos la última palabra como identificador
                area_nombre = fila[i + 1]  # Obtenemos el nombre del área
                
            # Verificamos si la celda contiene la palabra 'resumen' y terminamos el ciclo
            elif pd.notna(celda) and isinstance(celda, str) and 'resumen' in celda.lower():
                return pd.DataFrame(datos_areas, columns=columns) # devolvemos un dataframe con los datos de todas las areas

            # Si el área y el identificador están definidos
            elif area_nombre and area_identificador: 
                if i + 3 < len(fila):  # Verificamos que existan suficientes columnas para los datos
                    edad = fila[i]  # Obtenemos el valor de 'Edad'
                    casos = fila[i + 1]  # Obtenemos el valor de 'Casos'
                    porcentaje = fila[i + 2]  # Obtenemos el valor de '%'
                    acumulado = fila[i + 3]  # Obtenemos el valor de 'Acumulado %'
                    
                    # Verificamos que los valores no sean NaN antes de agregarlos
                    if pd.notna(edad) and pd.notna(casos) and pd.notna(porcentaje) and pd.notna(acumulado) and isinstance(edad, (int, float)) and isinstance(casos, (int, float)):
                        datos_areas.append([edad, casos, porcentaje, acumulado, area_nombre, area_identificador])  # Añadir los datos a la lista


skiprows = 13  # Ajusta este valor según sea necesario

# Procesamos el archivo de censo y obtener el DataFrame consolidado de todas las áreas
censo = procesar_censo(carpeta + 'padron_poblacion.xlsx', skiprows)
censo = censo[['Edad', 'Casos', 'Area', 'Id_area']]
censo.columns = ['Edad', 'Casos', 'Area', 'ID_DEPTO'] #Ajustamos los nombres de las columnas


#Como hay ciertos ID_DEPTOS los cuales poseen un valor no apropiado, decidimos cambiarlos dentro del dataframe
censo.replace({'ID_DEPTO': {'94008': '94007'}}, inplace=True)
censo.replace({'ID_DEPTO': {'94011': '94010'}}, inplace=True)
censo.replace({'ID_DEPTO': {'94015': '94014'}}, inplace=True)

# %%CREACION DE LA TABLA: GRUPO_ETARIO 

g = {'ID': [1, 2, 3, 4, 5, 6], 'Descripción' : ['0 a 5', '6 a 11', '12 a 18', '19 a 26', '27 a 59', '60 a 110']} #Diccionario con la informacion del DataFrame
GRUPO_ETARIO = pd.DataFrame(data = g) #Creamos el DataFrame


# %% CREACION DE LA TABLA: HABITAN_EN

def comunas_censo(dataFrame):
    nuevas_filas = []  # Lista para almacenar los datos de todas las filas
    for i, fila in dataFrame.iterrows():
        if 'comuna' in fila['Area'].lower(): #Si es una comuna, le indica que su area es Ciudad de Buenos Aires y que su ID_DEPTO ES 02000
            nuevas_filas.append({'Area':'Ciudad de Buenos Aires', 'ID_DEPTO':'02000', 'Edad': fila['Edad'], 'Casos': fila['Casos']})
        else: #Si no ocurre esto, le pone los mismos datos que tiene
            nuevas_filas.append({'Area':fila['Area'], 'ID_DEPTO':fila['ID_DEPTO'], 'Edad': fila['Edad'], 'Casos': fila['Casos']})
    censoNuevo = pd.DataFrame(nuevas_filas)
    return censoNuevo


def agrupar_por_grupo_etario(df):

    habitan_En = df.copy()

    #Establecemos los limites de edad para cada grupo mediante la funcion cut, donde la lista bins posee los valores con los cuales comienza y termina cada uno.
    habitan_En['ID_Grupo_Etario'] = pd.cut(df['Edad'], bins= [-1, 5, 11, 18, 26, 59, 110] , labels=[1, 2, 3, 4, 5, 6] , right=True)
    
    #cambiamos a tipo int para evitar errores en la función groupby
    habitan_En['ID_Grupo_Etario'] = habitan_En['ID_Grupo_Etario'].astype('Int64') 
    
    habitan_En = habitan_En.drop(columns=['Edad']) #Eliminamos la columna Edad
    
    df_agrupado = habitan_En.groupby(['ID_DEPTO', 'Area', 'ID_Grupo_Etario'], as_index=False)['Casos'].sum()

    return df_agrupado

HABITAN_EN = comunas_censo(censo)
HABITAN_EN = agrupar_por_grupo_etario(HABITAN_EN)

# %% CREACION DE DATAFRAME: EE CON VALORES BOOLEANOS EN NIVELES EDUCATIVOS

def filtrar_datos_y_crear_nuevo_df(ruta_archivo, skiprows):
    # Lee el archivo Excel, saltando las filas especificadas y utilizando header=[skiprows-1, skiprows] para manejar subcolumnas
    fuente_EE = pd.read_excel(ruta_archivo, header=[skiprows-1, skiprows])
    
    # Filtramos las filas donde la subcolumna 'Común' (columna N dentro del archivo) tenga el valor de '1'
    df_EEsoloComunes = fuente_EE[fuente_EE.iloc[:, 13] == 1].dropna(subset=[fuente_EE.columns[13]])
    
    # Seleccionamos solo las columnas hasta la columna 'Común' (columna AA del archivo)
    df_EEcomunesAcotado = df_EEsoloComunes.iloc[:, :27]  # Seleccionamos hasta la columna 27 (índice base 0)

    # Creamos el nuevo DataFrame con las columnas especificadas
    EstEducativos = pd.DataFrame()
    EstEducativos['Jurisdiccion'] = df_EEcomunesAcotado.iloc[:,0]
    EstEducativos['Cueanexo'] = df_EEcomunesAcotado.iloc[:, 1]
    EstEducativos['ID_DEPTO'] = df_EEcomunesAcotado.iloc[:, 9]
    
    # Creamos la columna 'Jardin' uniendo las columnas con índice 20 y 21
    EstEducativos['Jardin'] = ((df_EEcomunesAcotado.iloc[:, 20] == 1) | (df_EEcomunesAcotado.iloc[:, 21] == 1)).astype(str)
    
    # Creamos la columna 'Primario' copiando la columna con índice 22
    EstEducativos['Primario'] = (df_EEcomunesAcotado.iloc[:, 22] == 1).astype(str)
    
    # Creamos la columna 'Secundario' uniendo las columnas con índices 23, 24, 25 y 26
    EstEducativos['Secundario'] = ((df_EEcomunesAcotado.iloc[:, 23] == 1) | (df_EEcomunesAcotado.iloc[:, 24] == 1) | 
                              (df_EEcomunesAcotado.iloc[:, 25] == 1) | (df_EEcomunesAcotado.iloc[:, 26] == 1)).astype(str)
    
    
    return EstEducativos

skiprows = 6  # Fila donde comienzan los nombres de las columnas

# Filtramos los datos y creamos el nuevo DataFrame resultante
EstEducativos = filtrar_datos_y_crear_nuevo_df(carpeta + '2022_padron_oficial_establecimientos_educativos.xlsx', skiprows)


#Una vez obtenido el dataFrame, le agrego un 0 a los ID_DEPTO los cuales en censo poseen un area con un 0 adelante

def agregar_cero(dataframe, i):
    #Agrego 0 si es necesario en ID_DEPTO
    dataframe['ID_DEPTO'] = dataframe['ID_DEPTO'].astype(str)
    dataframe['ID_DEPTO'] = dataframe['ID_DEPTO'].apply(lambda x: '0' + x if len(x) == i else x)
    return dataframe

EstEducativos = agregar_cero(EstEducativos, 7)

#nos quedamos con los primeros 5 dígitos de ID_DEPTO, ya que estos son los que coinciden con las demás tablas
EstEducativos['ID_DEPTO'] =EstEducativos['ID_DEPTO'].str[:5] 


#Definimos que todos los EE ubicados en la CABA posean el mismo ID_DEPTO
def caba_mismo_ID(dataFrame):    
    
    nuevas_filas = []

    for i, fila in dataFrame.iterrows():
        if fila['Jurisdiccion'] == 'Ciudad de Buenos Aires':
            nuevas_filas.append({'Jurisdiccion':fila['Jurisdiccion'], 'Cueanexo':fila['Cueanexo'], 'ID_DEPTO' : '02000', 'Jardin': fila['Jardin'], 'Primario': fila['Primario'], 'Secundario': fila['Secundario']})
        else:
            nuevas_filas.append({'Jurisdiccion':fila['Jurisdiccion'], 'Cueanexo':fila['Cueanexo'], 'ID_DEPTO' : fila['ID_DEPTO'], 'Jardin': fila['Jardin'], 'Primario': fila['Primario'], 'Secundario': fila['Secundario']})
    dfModificado = pd.DataFrame(nuevas_filas)
    return dfModificado

dfEstEducativos_2 = caba_mismo_ID(EstEducativos)

#%% CREACION DE TABLA : ESTABLECIMIENTOS_EDUCATIVOS

ESTABLECIMIENTOS_EDUCATIVOS = dfEstEducativos_2[['Cueanexo' ,'ID_DEPTO']]

# %%CREACION DE TABLA: DEPARTAMENTO

#Nos quedamos con las columnas de censo seleccionadas
DEPARTAMENTO = censo[['ID_DEPTO', 'Area']]
#Cambiamos el nombre a las columnas
DEPARTAMENTO.columns = ['ID', 'Nombre']

#Para cada departamento que sea una comuna de la CABA, le asignamos el mismo nombre y el mismo ID 
def comunas_caba(dataFrame):
    nuevas_filas = []
    
    for i, fila in dataFrame.iterrows():
        if 'comuna' in fila['Nombre'].lower():
            nuevas_filas.append({'Nombre':'Ciudad de Buenos Aires', 'ID':'02000'})
            
        else:
            nuevas_filas.append({'Nombre':fila['Nombre'], 'ID':fila['ID']})
            
    dfModificado = pd.DataFrame(nuevas_filas)
    return dfModificado

DEPARTAMENTO = comunas_caba(DEPARTAMENTO)


#Establecemos como indice a la columna ID_DEPTO para luego poder hacer un JOIN entre DEPARTAMENTO y dfEstEducativos_2 mediante ID y ID_DEPTO, respectivamente
dfEstEducativos_2 = dfEstEducativos_2.set_index('ID_DEPTO')[['Jurisdiccion', 'Cueanexo','Jardin', 'Primario', 'Secundario']]  
DEPARTAMENTO = DEPARTAMENTO.set_index('ID').join(dfEstEducativos_2, how='left')  

#Reseteamos los indices
DEPARTAMENTO = DEPARTAMENTO.reset_index()
dfEstEducativos_2 = dfEstEducativos_2.reset_index()

#Renombramos las columnas de DEPARTAMENTO, y elminamos aquellas que no nos seran utiles
DEPARTAMENTO.rename(columns={'Jurisdiccion': 'Provincia'}, inplace=True)
DEPARTAMENTO.drop(columns=['Cueanexo','Jardin','Primario','Secundario'], inplace=True)

#Eliminamos duplicados
DEPARTAMENTO = DEPARTAMENTO.drop_duplicates()

#Aquellas filas que tengan valores nulos, las rellenamos con Tierra del Fuego. Esto se debe a que en los unicos casos donde se ven la presencia de estos tipos de valores se necesitan completar con este mismo.
DEPARTAMENTO = DEPARTAMENTO.fillna('Tierra del Fuego')

# %% CREACION DE TABLA: NIVEL_EDUCATIVO

d = {'ID':['1', '2', '3'], 'Descripcion': ['Jardin', 'Primaria', 'Secundaria']} #Creamos el diccionario con la informacion asociada a el DataFrame

NIVEL_EDUCATIVO = pd.DataFrame(data = d) #armamos del dataframe
NIVEL_EDUCATIVO.set_index('ID', inplace= True) #Marcamos como indice la columna ID

# %%CREACION DE TABLA: NIVEL_ESTABLECIMIENTO

def poner_nivel(dataFrame):
    # Lista para almacenar las filas del nuevo DataFrame
    nuevas_filas = []
    
    #Segun si los resultados booleanos indican si tiene o no cada establecimiento su respectivo nivel educativo, le asigna el ID_NIVEL correspondiente a este si es que lo posee
    for i, fila in dataFrame.iterrows():
        if fila['Jardin'] == 'True':
            nuevas_filas.append({'Cueanexo':fila['Cueanexo'], 'ID_NIVEL': 1})
        if fila['Primario'] == 'True':
            nuevas_filas.append({'Cueanexo':fila['Cueanexo'], 'ID_NIVEL': 2})
        if fila['Secundario'] == 'True':
            nuevas_filas.append({'Cueanexo':fila['Cueanexo'], 'ID_NIVEL': 3})
    # Convertimos la lista de diccionarios en un DataFrame
    dfConNivel = pd.DataFrame(nuevas_filas)
    return dfConNivel

NIVEL_ESTABLECIMIENTO= poner_nivel( dfEstEducativos_2)
  
# %% CREACION DE TABLA: CENTROS CULTURALES

#Creamos el dataFrame seleccionando las columnas que necesitaremos de la fuente de datos dada.
CENTROS_CULTURALES = centrosCulturales.copy()
CENTROS_CULTURALES = CENTROS_CULTURALES[['Nombre', 'Domicilio', 'ID_DEPTO', 'Mail ', 'Capacidad']]   
CENTROS_CULTURALES['ID_DEPTO'] = CENTROS_CULTURALES['ID_DEPTO'].astype(str)

#agregamos ceros reutilizando la función previamente definida
CENTROS_CULTURALES = agregar_cero(CENTROS_CULTURALES, 4)

#Para poder facilitar lo buscado, unicamente nos quedaremos con los dominios de mail de cada fila (de cada centro cultural)
def soloDominio(dataFrame):
    
    dataFrame = dataFrame.rename(columns={"Mail ": "Mail"}) #Quitamos el espacio que tenia la columna en su nombre
    
    for i, fila in dataFrame.iterrows():
        email = fila['Mail']   
        if pd.notna(email) and '@' in email:
            email = (email.split('@')[1].split('.')[0]).lower()
            dataFrame.loc[i, 'Mail'] = email #Actualizamos el dataFrame
    
    return dataFrame

CENTROS_CULTURALES = soloDominio(CENTROS_CULTURALES)

#%%===========================================================================
# ANALISIS DE DATOS: A continuación, se muestran todos los pasos que seguimos apara poder realizar el analisis de datos con las tablas ya armadas previamente en la anterior seccion. Para este apartado, realizamos nuevas tablas con información que podría servirnos de utilidad y también implementamos ciertos graficos los cuales nos facilitarían poder detectar lo buscado en el objetivo general.
#=============================================================================
# %% Reportes: CONSULTAS SQL
# %%
# i) Para cada departamento informar la provincia, cantidad de EE de cada nivel educativo, considerando solamente la modalidad común, y cantidad de habitantes por edad según los niveles educativos. El orden del reporte debe ser alfabético por provincia y dentro de las provincias, descendente por cantidad de escuelas primarias.

CANTIDADES = dd.sql("""
                    SELECT ID_DEPTO AS ID,
                    SUM(CASE WHEN ID_NIVEL = 1 THEN 1 ELSE 0 END) AS Jardines,
                    SUM(CASE WHEN ID_NIVEL = 2 THEN 1 ELSE 0 END) AS Primarias,
                    SUM(CASE WHEN ID_NIVEL = 3 THEN 1 ELSE 0 END) AS Secundarias
                    FROM NIVEL_ESTABLECIMIENTO AS n
                    INNER JOIN ESTABLECIMIENTOS_EDUCATIVOS AS e
                    ON e.Cueanexo = n.Cueanexo 
                    GROUP BY ID_DEPTO
                    ORDER BY ID_DEPTO
                    """).df()

POBLACION_JARDIN = dd.sql("""
                  SELECT ID_DEPTO, Casos AS Poblacion_Jardin
                  FROM HABITAN_EN
                  WHERE ID_Grupo_Etario = 1
                  """).df()
                  
POBLACION_PRIMARIA = dd.sql("""
                 SELECT h.ID_DEPTO, Poblacion_Jardin, Casos AS Poblacion_Primaria
                 FROM HABITAN_EN AS h
                 INNER JOIN POBLACION_JARDIN AS p
                 ON h.ID_DEPTO = p.ID_DEPTO
                 WHERE ID_Grupo_Etario = 2
                 """).df()
                 
POBLACION_SECUNDARIA = dd.sql("""
                 SELECT h.ID_DEPTO, Poblacion_Jardin, Poblacion_Primaria, Casos AS Poblacion_Secundaria
                 FROM HABITAN_EN AS h
                 INNER JOIN POBLACION_PRIMARIA AS p
                 ON h.ID_DEPTO = p.ID_DEPTO
                 WHERE ID_Grupo_Etario = 3
                 """).df()
                 
CANT_Y_POB = dd.sql("""
                    SELECT ID, Jardines, Poblacion_Jardin, Primarias, Poblacion_Primaria, Secundarias, Poblacion_Secundaria
                    FROM CANTIDADES
                    INNER JOIN POBLACION_SECUNDARIA
                    ON ID = ID_DEPTO
                    """).df()

RESULTADO_1 = dd.sql("""
                     SELECT Provincia, Nombre AS Departamento, Jardines, Poblacion_Jardin, Primarias, Poblacion_Primaria, Secundarias, Poblacion_Secundaria
                     FROM CANT_Y_POB AS c
                     INNER JOIN DEPARTAMENTO AS d
                     ON d.ID = c.ID
                     ORDER BY Departamento
                     """).df()                                       

# %% ii) Para cada departamento informar la provincia y la cantidad de CC con capacidad mayor a 100 personas. El orden del reporte debe ser alfabético por provincia y dentro de las provincias, descendente por cantidad de CC de dicha capacidad.


capMayorA100 = dd.sql("""
               SELECT d.Provincia, d.Nombre, c.capacidad
               FROM DEPARTAMENTO AS d
               INNER JOIN CENTROS_CULTURALES AS c
               ON d.ID = c.ID_DEPTO
               WHERE c.capacidad > 100
              """).df()


RESULTADO_2 = dd.sql("""
                SELECT  DISTINCT cm.Provincia, cm.Nombre AS Departamento, COUNT(*) AS 'Cantidad de CC con cap >100'
                FROM capMayorA100 AS cm
                GROUP BY cm.Provincia, cm.Nombre
                ORDER BY cm.Provincia ASC, COUNT(*) DESC
              """).df()


# %% iii) Para cada departamento, indicar provincia, cantidad de CC, cantidad de EE (de modalidad común) y población total. Ordenar por cantidad EE descendente, cantidad CC descendente, nombre de provincia ascendente y nombre de departamento ascendente. No omitir casos sin CC o EE.


deptosConEE = dd.sql("""
               SELECT d.ID, d.Provincia, d.Nombre, COUNT(e.*) AS Cant_EE
               FROM ESTABLECIMIENTOS_EDUCATIVOS AS e
               INNER JOIN DEPARTAMENTO AS d
               ON d.ID = e.ID_DEPTO
               GROUP BY d.Provincia, d.Nombre, d.ID
              """).df()


deptosConYSinEE = dd.sql("""
               SELECT d.ID, d.Provincia, d.Nombre, CASE WHEN dce.Cant_EE IS NULL 
                             THEN 0 
                             ELSE dce.Cant_EE
                             END AS Cant_EE , 
               FROM DEPARTAMENTO AS d
               LEFT OUTER JOIN deptosConEE AS dce
               ON d.ID = dce.ID
              """).df()

deptosConCC = dd.sql("""
               SELECT d.ID, d.Provincia, d.Nombre, COUNT(c.*) AS Cant_CC
               FROM CENTROS_CULTURALES AS c
               INNER JOIN DEPARTAMENTO AS d
               ON d.ID = c.ID_DEPTO
               GROUP BY d.Provincia, d.Nombre, d.ID
              """).df()


todoJunto = dd.sql("""
               SELECT dcse.*, CASE WHEN dcc.Cant_CC IS NULL 
                             THEN 0 
                             ELSE dcc.Cant_CC
                             END AS Cant_CC
               FROM deptosConYSinEE AS dcse
               LEFT OUTER JOIN deptosConCC AS dcc
               ON dcse.ID = dcc.ID
              """).df()
              

RESULTADO_3 = dd.sql("""
                SELECT tj.Provincia, tj.Nombre, tj.Cant_EE, tj.Cant_CC, SUM(h.casos) AS Poblacion_Total
                FROM todoJunto AS tj
                LEFT OUTER JOIN HABITAN_EN AS h
                ON tj.ID = h.ID_DEPTO
                GROUP BY tj.Provincia, tj.Nombre, tj.Cant_EE, tj.Cant_CC
                ORDER BY tj.Cant_EE DESC, tj.Cant_CC DESC, tj.Provincia ASC, tj.Nombre ASC
              """).df()
              

# %% iv) Para cada departamento, indicar provincia y qué dominios de mail se usan más para los CC.

CCDominio = dd.sql("""
               SELECT ID_DEPTO, Mail, COUNT(*) AS CantDom
               FROM CENTROS_CULTURALES
               WHERE Mail LIKE '____%'  
               GROUP BY ID_DEPTO, Mail
               ORDER BY ID_DEPTO, Mail
              """).df()

# Con 'WHERE Mail LIKE '____%''  descarto aquellos que no son dominio. Esta decision esta aclarada en el Informe, dentro del apartado "Decisiones Tomadas"           
              
RESULTADO_4 = dd.sql("""
                SELECT d.Provincia, d.Nombre AS Departamento, cd1.Mail AS 'Dominio más
frecuente en CC'
                FROM DEPARTAMENTO AS d
                INNER JOIN CCDominio AS cd1
                ON d.ID = cd1.ID_DEPTO
                WHERE cd1.CantDom = (
                    SELECT MAX(cd2.CantDom)
                    FROM CCDominio AS cd2
                    WHERE cd2.ID_DEPTO = cd1.ID_DEPTO
                    ) 
                GROUP BY d.Provincia, d.Nombre, cd1.Mail, cd1.CantDom
                ORDER BY d.Provincia ASC, d.Nombre ASC
              """).df()
           


#%% Herramientas de Visualización: GRÁFICOS
# %% Gráfico 1:  Cantidad de CC por provincia. Mostrarlos ordenados de manera decreciente por dicha cantidad.

infoGraf1 = dd.sql("""
               SELECT Provincia, SUM(Cant_CC) AS Cantidad
               FROM RESULTADO_3
               WHERE Provincia != 'Ciudad de Buenos Aires'
               GROUP BY Provincia
               ORDER BY cantidad DESC
              
              """).df()             

#Presemtamos la informacón mediante un gráfico de barras
fig, ax = plt.subplots(figsize=(13,5))
infoGraf1.set_index("Provincia")["Cantidad"].plot(kind="bar", ax=ax)

# Aqui personalizamos el título y las etiquetas
ax.set_xlabel('Provincia', fontsize = 14)
ax.set_ylabel('Cantidad')
ax.bar_label(ax.containers[0], fontsize=12)
ax.tick_params(axis='x', direction='in', length=10, labelsize=14)

#%% Auxiliar: grafico que acompaña al Gráfico 1
#Aqui armamos otro grafico de barras que muestra la población de cada provincia

aux_graf1 = dd.sql(
                """
                SELECT Provincia, SUM(Poblacion_total) AS Poblacion
                FROM RESULTADO_3
                WHERE Provincia != 'Ciudad de Buenos Aires'
                GROUP BY Provincia
                ORDER BY poblacion DESC
                """).df()
#Presemtamos la informacón mediante un gráfico de barras
fig, ax = plt.subplots(figsize=(13,5))
aux_graf1.set_index("Provincia")["Poblacion"].plot(kind="bar", ax=ax)

# Aqui personalizamos el título y las etiquetas
ax.set_xlabel('Provincias', fontsize = 14)
ax.set_ylabel('Poblacion_provincia')

#%% Gráfico 2: Graficar la cantidad de EE de los departamentos en función de la población, separando por nivel educativo y su correspondiente grupo etario (identificándolos por colores). Se pueden basar en la primera consulta SQL para realizar este gráfico.


infoGraf2 = dd.sql("""
                     SELECT Departamento, Jardines, Poblacion_Jardin, Primarias, Poblacion_Primaria, Secundarias, Poblacion_Secundaria
                     FROM RESULTADO_1
                     """).df()   

plt.figure(figsize=(12, 7))
#Armamos un scatterplot para cada nivel educativo
sns.scatterplot(x=infoGraf2['Poblacion_Jardin'], y=infoGraf2['Jardines'], 
                color='#1f77b4', label='Inicial', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=infoGraf2['Poblacion_Primaria'], y=infoGraf2['Primarias'], 
                color='#2ca02c', label='Primaria', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=infoGraf2['Poblacion_Secundaria'], y=infoGraf2['Secundarias'], 
                color='#d62728', label='Secundaria', s=50, edgecolor='black', alpha=0.5)


#Añadimos líneas de tendencia, para poder tener una visualizacion más clara

def linea_tendencia(x, y, color, label):
    # reshape de los datos para que sklearn pueda trabajar con ellos
    X = x.values.reshape(-1, 1)
    Y = y.values

    # Creamos el modelo de regresión sin intercepto (forzando que pase por el origen)
    modelo = LinearRegression(fit_intercept=False)
    modelo.fit(X, Y)

    # Predecir los valores y crear la línea de tendencia
    y_pred = modelo.predict(X)

    # Graficar la línea de tendencia
    plt.plot(x, y_pred, color=color, label=label)

linea_tendencia(infoGraf2['Poblacion_Jardin'], infoGraf2['Jardines'], 'k', 'Tendencia Inicial')
linea_tendencia(infoGraf2['Poblacion_Primaria'], infoGraf2['Primarias'], 'g', 'Tendencia Primaria')
linea_tendencia(infoGraf2['Poblacion_Secundaria'], infoGraf2['Secundarias'], 'r', 'Tendencia Secundaria')


# Personalización de etiquetas y título
plt.xlabel("Población del Departamento", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de Establecimientos Educativos (EE)", fontsize=14, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.6)

# Agregamos la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)

#%% Gráfico 2 acotado (igual al original pero agregando limites en el eje X,Y)

#Creamos un scatterplot para cada nivel educativo.
plt.figure(figsize=(12, 7))

sns.scatterplot(x=infoGraf2['Poblacion_Jardin'], y=infoGraf2['Jardines'], 
                color='#1f77b4', label='Inicial', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=infoGraf2['Poblacion_Primaria'], y=infoGraf2['Primarias'], 
                color='#2ca02c', label='Primaria', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=infoGraf2['Poblacion_Secundaria'], y=infoGraf2['Secundarias'], 
                color='#d62728', label='Secundaria', s=50, edgecolor='black', alpha=0.5)

#Nuevamente, para este gráfico también añadimos las líneas de tendencia utilizando la función definida anteriormente
linea_tendencia(infoGraf2['Poblacion_Jardin'], infoGraf2['Jardines'], 'k', 'Tendencia Inicial')
linea_tendencia(infoGraf2['Poblacion_Primaria'], infoGraf2['Primarias'], 'g', 'Tendencia Primaria')
linea_tendencia(infoGraf2['Poblacion_Secundaria'], infoGraf2['Secundarias'], 'r', 'Tendencia Secundaria')


# Personalización de etiquetas y título
plt.xlabel("Población del Departamento", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de Establecimientos Educativos (EE)", fontsize=14, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.6)

# Agregamos la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)

# Usamos limites para acotar
plt.xlim(0, 10000)  
plt.ylim(0, 200) 

#%% Gráfico 2 acotado y separado por niveles

# Scatterplot del nivel 1
plt.figure(figsize=(12, 7))

sns.scatterplot(x=infoGraf2['Poblacion_Jardin'], y=infoGraf2['Jardines'], 
                color='#1f77b4', label='Inicial', s=50, edgecolor='black', alpha=0.5)

# Personalización de etiquetas y título
plt.xlabel("Población del Departamento", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de Establecimientos Educativos (EE)", fontsize=14, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.6)

# Agregamos la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)

# Usamos limites para acotar
plt.xlim(0, 10000)  
plt.ylim(0, 200) 

# Scatterplot del nivel 2
plt.figure(figsize=(12, 7))

sns.scatterplot(x=infoGraf2['Poblacion_Primaria'], y=infoGraf2['Primarias'], 
                color='#2ca02c', label='Primaria', s=50, edgecolor='black', alpha=0.5)

# Personalización de etiquetas y título
plt.xlabel("Población del Departamento", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de Establecimientos Educativos (EE)", fontsize=14, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.6)

# Agregamos la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)

# Usamos limites para acotar
plt.xlim(0, 10000)  
plt.ylim(0, 200) 

# Scatterplot del nivel 3
plt.figure(figsize=(12, 7))

sns.scatterplot(x=infoGraf2['Poblacion_Secundaria'], y=infoGraf2['Secundarias'], 
                color='#d62728', label='Secundaria', s=50, edgecolor='black', alpha=0.5)

plt.grid(True, linestyle='--', alpha=0.6)

# Agregamos la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)

# Usamos limites para acotar
plt.xlim(0, 10000)  
plt.ylim(0, 200) 

# %% Gráfico 3: Realizar un boxplot por cada provincia, de la cantidad de EE por cada departamento de la provincia. Mostrar todos los boxplots en una misma figura, ordenados por la mediana de cada provincia.

#Calculamos las medianas de EE por cada Provincia

medianas = dd.sql("""
    SELECT Provincia, MEDIAN(Cant_EE) as mediana
    FROM RESULTADO_3
    WHERE Provincia != 'Ciudad de Buenos Aires'
    GROUP BY Provincia
    ORDER BY mediana DESC
    """).df()

infoGraf3 = dd.sql("""
                     SELECT Provincia, Cant_EE
                     FROM RESULTADO_3
                     WHERE Provincia != 'Ciudad de Buenos Aires'
                     """).df()  
                     
#Armamos los boxplots, ordenados por la mediana                     
plt.figure(figsize=(10, 6))
sns.boxplot(x='Provincia', y='Cant_EE', data=infoGraf3, order=medianas['Provincia'],
            boxprops=dict( facecolor='white',linewidth = 1),
            medianprops=dict(color="green", linewidth=2))

# Agregar título y etiquetas a los ejes
plt.xlabel('Provincia', fontsize=12)
plt.ylabel('Cantidad', fontsize=12)
plt.xticks(rotation=90, fontsize=10)

# Personalizar la cuadrícula
plt.grid(True, axis='y')

plt.show()

#%% Grafico 3 teniendo en cuenta a la Ciudad de Buenos Aires

#Calculamos las medianas

medianas = dd.sql("""
    SELECT Provincia, MEDIAN(Cant_EE) as mediana
    FROM RESULTADO_3
    GROUP BY Provincia
    ORDER BY mediana DESC
    """).df()


infoGraf3 = dd.sql("""
                     SELECT Provincia, Cant_EE
                     FROM RESULTADO_3
                     """).df()  
                     
plt.figure(figsize=(10, 6))
sns.boxplot(x='Provincia', y='Cant_EE', data=infoGraf3, order=medianas['Provincia'],
            boxprops=dict( facecolor='white',linewidth = 1),
            medianprops=dict(color="green", linewidth=2))

# Agregamos título y etiquetas a los ejes
plt.xlabel('Provincia', fontsize=12)
plt.ylabel('Cantidad', fontsize=12)
plt.xticks(rotation=90, fontsize=10)
plt.grid(True, axis='y')

plt.show()

#%% Gráfico 4: Relación entre la cantidad de CC cada mil habitantes y de EE cada mil habitantes.

# Consulta SQL auxiliar para separar la información que precisamos
infoGraf4 = dd.sql("""
                   SELECT  Provincia, Nombre AS Departamento, (Cant_EE/ Poblacion_Total)*1000 AS ProporcionEE_cada_mil, (Cant_CC/ Poblacion_Total)*1000 AS ProporcionCC_cada_mil
                   FROM RESULTADO_3
                   GROUP BY Nombre, Cant_EE, Cant_CC, Poblacion_Total, Provincia
                   ORDER BY ProporcionEE_cada_mil DESC, ProporcionCC_cada_mil DESC
                   """).df()

# Armamos el scatterplot

plt.figure(figsize=(12, 7))

sns.scatterplot(x=infoGraf4['ProporcionEE_cada_mil'], 
                y=infoGraf4['ProporcionCC_cada_mil'],
                color='#1f77b4', s=50, edgecolor='black', alpha=0.7)



# Personalización de etiquetas y título
plt.xlabel("Cantidad de EE cada mil habitantes", fontsize=14)
plt.ylabel("Cantidad de CC cada mil habitantes", fontsize=14)

# Personalizar la cuadrícula
plt.grid(True, linestyle='--', alpha=0.7)

#%% Grafico 4 acotado (igual al original pero agregando limites en el eje X,Y)
plt.figure(figsize=(12, 7))

# Scatterplot para cada nivel educativo con mejor visibilidad
sns.scatterplot(x=infoGraf4['ProporcionEE_cada_mil'], y=infoGraf4['ProporcionCC_cada_mil'], color='#1f77b4', s=50, edgecolor='black', alpha=0.7)



# Personalización de etiquetas y título
plt.xlabel("Cantidad de EE cada mil habitantes", fontsize=14)
plt.ylabel("Cantidad de CC cada mil habitantes", fontsize=14)

# Personalizar la cuadrícula
plt.grid(True, linestyle='--', alpha=0.7)
#Usamos para acotar
plt.xlim(0, 4)  
plt.ylim(0, 0.2)
#%%
#ANEXO
#%%===========================================================================
# ANEXO: Gráficos auxiliares utilizados para poder detectar con mayor precisión lo analizado por cada item del apartado Visualización. Además, realizamos un gráfico extra, el cual nos ayuda a poder responder a la pregunta general
#=============================================================================
#%% Gráfico scatterplot para responder la pregunta general

aux_graf_gral = dd.sql("""
                   SELECT  Nombre, Cant_EE, Cant_CC
                   FROM RESULTADO_3
                   """).df()

sns.scatterplot(x=aux_graf_gral['Cant_EE'], y=aux_graf_gral['Cant_CC'], 
                color='#1f77b4', s=50, edgecolor='black', alpha=0.5)

# Personalización de etiquetas y título
plt.xlabel("cantidad de EE", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de CC", fontsize=14, fontweight='bold')

# Personalizar la cuadrícula
plt.grid(True, linestyle='--', alpha=0.6)