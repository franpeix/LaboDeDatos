# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Autores  : Francisco Peix, Kamala Jimeno Leiton, Carolina Cuiña
"""

# Importamos bibliotecas
import pandas as pd
import duckdb as dd
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


#%%===========================================================================
# Importamos los datasets que vamos a utilizar en este programa
#=============================================================================

carpeta = "~/Downloads/TP1_Labo/"

padronPoblacion = pd.read_excel(carpeta + "padron_poblacion.xlsx", skiprows= 12) 
padronEstEducativos = pd.read_excel(carpeta + "2022_padron_oficial_establecimientos_educativos.xlsx", skiprows= 5)
centrosCulturales = pd.read_csv(carpeta + "centros_culturales.csv") 



# %% CENSO

def procesar_censo(ruta_archivo, skiprows):
    # Leer el archivo Excel en un DataFrame, saltando las filas especificadas
    fuente_Censo = pd.read_excel(ruta_archivo, header=None, skiprows=skiprows)
    
    # Lista para almacenar los datos de todas las áreas
    datos_areas = []
    
    # Inicializar variables
    area_nombre = ''  # Nombre del área actual
    area_identificador = ''  # Identificador del área actual
    columns = ['Edad', 'Casos', '%', 'Acumulado %', 'Area', 'Id_area']  # Nombres de las columnas del DataFrame resultante
    
    # Recorrer fila por fila
    for index, row in fuente_Censo.iterrows():
        if row.dropna().empty:
            continue  # Omitir filas en blanco
            
        # Recorrer celda por celda en la fila actual
        for i, cell in row.items():
            # Verificar si la celda contiene la palabra 'area'
            if pd.notna(cell) and isinstance(cell, str) and 'area' in cell.lower():
                partes = cell.split() # Dividir la cadena en palabras
                area_identificador = partes[-1]  # Obtener la última palabra como identificador
                area_nombre = row[i + 1]  # Obtener el nombre del área
            # Verificar si la celda contiene la palabra 'resumen'
            elif pd.notna(cell) and isinstance(cell, str) and 'resumen' in cell.lower():
                area_identificador = '0'  # Identificador para 'Resumen'
                area_nombre = 'Resumen'  # Nombre para 'Resumen'
            # Si el área y el identificador están definidos
            elif area_nombre and area_identificador:
                if i + 3 < len(row):  # Verificar que existan suficientes columnas para los datos
                    edad = row[i]  # Obtener el valor de 'Edad'
                    casos = row[i + 1]  # Obtener el valor de 'Casos'
                    porcentaje = row[i + 2]  # Obtener el valor de '%'
                    acumulado = row[i + 3]  # Obtener el valor de 'Acumulado %'
                    
                    # Verificar que los valores no sean NaN antes de agregarlos
                    if pd.notna(edad) and pd.notna(casos) and pd.notna(porcentaje) and pd.notna(acumulado) and isinstance(edad, (int, float)) and isinstance(casos, (int, float)):
                        datos_areas.append([edad, casos, porcentaje, acumulado, area_nombre, area_identificador])  # Añadir los datos a la lista
    
    # Crear un DataFrame con los datos de todas las áreas
    dfCenso = pd.DataFrame(datos_areas, columns=columns)
    
    return dfCenso  # Devolver el DataFrame resultante

# Ruta del archivo Excel
ruta_archivo = '~/Downloads/TP1_Labo/padron_poblacion.xlsx'
skiprows = 13  # Ajusta este valor según sea necesario

# Procesar el archivo de censo y obtener el DataFrame consolidado de todas las áreas
censo = procesar_censo(ruta_archivo, skiprows)
censo = censo[['Edad', 'Casos', 'Area', 'Id_area']]
censo.columns = ['Edad', 'Casos', 'Area', 'ID_DEPTO']


censo.replace({'ID_DEPTO': {'94008': '94007'}}, inplace=True)
censo.replace({'ID_DEPTO': {'94011': '94010'}}, inplace=True)
censo.replace({'ID_DEPTO': {'94015': '94014'}}, inplace=True)

# %%CREACION DE LA TABLA: GRUPO_ETARIO 

g = {'ID': [1, 2, 3, 4, 5, 6], 'Descripción' : ['0 a 5', '6 a 11', '12 a 18', '19 a 26', '27 a 59', '60 a 110']}
GRUPO_ETARIO = pd.DataFrame(data = g)


# %% CREACION DE LA TABLA: HABITAN_EN
import pandas as pd

def comunas_censo(dataFrame):
    nuevas_filas = []
    for i, fila in dataFrame.iterrows():
        if 'comuna' in fila['Area'].lower():
            nuevas_filas.append({'Area':'Ciudad de Buenos Aires', 'ID_DEPTO':'02000', 'Edad': fila['Edad'], 'Casos': fila['Casos']})
        else:
            nuevas_filas.append({'Area':fila['Area'], 'ID_DEPTO':fila['ID_DEPTO'], 'Edad': fila['Edad'], 'Casos': fila['Casos']})
    df2 = pd.DataFrame(nuevas_filas)
    return df2


def agrupar_por_grupo_etario(df):

    habitan_En = df.copy()


    habitan_En['ID_Grupo_Etario'] = pd.cut(df['Edad'], bins= [-1, 5, 11, 18, 26, 59, 110] , labels=[1, 2, 3, 4, 5, 6] , right=True)
    habitan_En['ID_Grupo_Etario'] = habitan_En['ID_Grupo_Etario'].astype('Int64')
    habitan_En = habitan_En.drop(columns=['Edad'])
    df_agrupado = habitan_En.groupby(['ID_DEPTO', 'Area', 'ID_Grupo_Etario'], as_index=False)['Casos'].sum()

    return df_agrupado

HABITAN_EN = comunas_censo(censo)
HABITAN_EN = agrupar_por_grupo_etario(HABITAN_EN)
HABITAN_EN = HABITAN_EN[HABITAN_EN['Area'] != 'Resumen']

# %% EE CON VALORES BOOLEANOS EN NIVELES EDUCATIVOS

def filtrar_datos_y_crear_nuevo_df(ruta_archivo, skiprows):
    # Leer el archivo Excel, saltando las filas especificadas y utilizando header=[skiprows-1, skiprows] para manejar subcolumnas
    fuente_EE = pd.read_excel(ruta_archivo, header=[skiprows-1, skiprows])
    
    # Filtrar las filas donde la subcolumna 'Común' (columna N dentro del archivo) tenga el valor de '1'
    df_EEcomunes = fuente_EE[fuente_EE.iloc[:, 13] == 1].dropna(subset=[fuente_EE.columns[13]])
    
    # Seleccionar solo las columnas hasta la columna 'Común' (columna AA del archivo)
    df_acotado = df_EEcomunes.iloc[:, :27]  # Seleccionar hasta la columna 27 (índice base 0)

    # Crear el nuevo DataFrame con las columnas especificadas
    dfEstEducativos = pd.DataFrame()
    dfEstEducativos['Jurisdiccion'] = df_acotado.iloc[:,0]
    dfEstEducativos['Cueanexo'] = df_acotado.iloc[:, 1]
    dfEstEducativos['ID_DEPTO'] = df_acotado.iloc[:, 9]
    
    # Crear la columna 'Jardin' uniendo las columnas con índice 20 y 21
    dfEstEducativos['Jardin'] = ((df_acotado.iloc[:, 20] == 1) | (df_acotado.iloc[:, 21] == 1)).astype(str)
    
    # Crear la columna 'Primario' copiando la columna con índice 22
    dfEstEducativos['Primario'] = (df_acotado.iloc[:, 22] == 1).astype(str)
    
    # Crear la columna 'Secundario' uniendo las columnas con índices 23, 24, 25 y 26
    dfEstEducativos['Secundario'] = ((df_acotado.iloc[:, 23] == 1) | (df_acotado.iloc[:, 24] == 1) | 
                              (df_acotado.iloc[:, 25] == 1) | (df_acotado.iloc[:, 26] == 1)).astype(str)
    
    
    return dfEstEducativos

# Ruta del archivo Excel
ruta_archivo = '~/Downloads/TP1_Labo/2022_padron_oficial_establecimientos_educativos.xlsx'
skiprows = 6  # Fila donde comienzan los nombres de las columnas

# Filtrar los datos y crear el nuevo DataFrame resultante
dfEstEducativos = filtrar_datos_y_crear_nuevo_df(ruta_archivo, skiprows)


#Una vez obtenido el dataFrame, le agrego un 0 a los ID_DEPTO los cuales en censo poseen un area con un 0 adelante

def agregar_cero(dataframe):
    #Agrego 0 si es necesario en ID_DEPTO
    dataframe['ID_DEPTO'] = dataframe['ID_DEPTO'].astype(str)
    dataframe['ID_DEPTO'] = dataframe['ID_DEPTO'].apply(lambda x: '0' + x if len(x) == 7 else x)
    
    #Agrego 0 si es necesario en Cueanexo
    dataframe['Cueanexo'] = dataframe['Cueanexo'].astype(str)
    dataframe['Cueanexo'] = dataframe['Cueanexo'].apply(lambda x: '0' + x if len(x) == 8 else x)
    return dataframe

dfEstEducativos = agregar_cero(dfEstEducativos)
dfEstEducativos['ID_DEPTO'] =dfEstEducativos['ID_DEPTO'].str[:5] 


def caba_mismo_ID(dataFrame):    
    nuevas_filas = []

    for i, fila in dataFrame.iterrows():
        if fila['Jurisdiccion'] == 'Ciudad de Buenos Aires':
            nuevas_filas.append({'Jurisdiccion':fila['Jurisdiccion'], 'Cueanexo':fila['Cueanexo'], 'ID_DEPTO' : '02000', 'Jardin': fila['Jardin'], 'Primario': fila['Primario'], 'Secundario': fila['Secundario']})
        else:
            nuevas_filas.append({'Jurisdiccion':fila['Jurisdiccion'], 'Cueanexo':fila['Cueanexo'], 'ID_DEPTO' : fila['ID_DEPTO'], 'Jardin': fila['Jardin'], 'Primario': fila['Primario'], 'Secundario': fila['Secundario']})
    df2 = pd.DataFrame(nuevas_filas)
    return df2

dfEstEducativos_2 = caba_mismo_ID(dfEstEducativos)
#%% CREACION DE TABLA : ESTABLECIMIENTOS_EDUCATIVOS


ESTABLECIMIENTOS_EDUCATIVOS = dfEstEducativos_2[['Cueanexo' ,'ID_DEPTO']]

# %%CREACION DE TABLA: DEPARTAMENTO

DEPARTAMENTO = censo[['ID_DEPTO', 'Area']]
DEPARTAMENTO.columns = ['ID', 'Nombre']

def comunas_caba(dataFrame):
    nuevas_filas = []
    
    for i, fila in dataFrame.iterrows():
        if 'comuna' in fila['Nombre'].lower() or 'resumen' in fila['Nombre'].lower():
            nuevas_filas.append({'Nombre':'Ciudad de Buenos Aires', 'ID':'02000'})
        else:
            nuevas_filas.append({'Nombre':fila['Nombre'], 'ID':fila['ID']})

            
    df2 = pd.DataFrame(nuevas_filas)
    return df2
DEPARTAMENTO = comunas_caba(DEPARTAMENTO)



dfEstEducativos_2 = dfEstEducativos_2.set_index('ID_DEPTO')[['Jurisdiccion', 'Cueanexo','Jardin', 'Primario', 'Secundario']]  
DEPARTAMENTO = DEPARTAMENTO.set_index('ID').join(dfEstEducativos_2, how='left')  

DEPARTAMENTO = DEPARTAMENTO.reset_index()
dfEstEducativos_2 = dfEstEducativos_2.reset_index()

DEPARTAMENTO.rename(columns={'Jurisdiccion': 'Provincia'}, inplace=True)
DEPARTAMENTO.drop(columns=['Cueanexo','Jardin','Primario','Secundario'], inplace=True)


DEPARTAMENTO = DEPARTAMENTO.drop_duplicates()

DEPARTAMENTO = DEPARTAMENTO.fillna('Tierra del Fuego')

# %% CREACION DE TABLA: NIVEL_EDUCATIVO

d = {'ID':['1', '2', '3'], 'Descripcion': ['Jardin', 'Primaria', 'Secundaria']}

NIVEL_EDUCATIVO = pd.DataFrame(data = d)
NIVEL_EDUCATIVO.set_index('ID', inplace= True)


# %%CREACION DE TABLA: NIVEL_ESTABLECIMIENTO

def poner_nivel(df):
    # Lista para almacenar las filas del nuevo DataFrame
    nuevas_filas = []

    for i, fila in df.iterrows():
        if fila['Jardin'] == 'True':
            nuevas_filas.append({'Cueanexo':fila['Cueanexo'], 'ID_NIVEL': 1})
        if fila['Primario'] == 'True':
            nuevas_filas.append({'Cueanexo':fila['Cueanexo'], 'ID_NIVEL': 2})
        if fila['Secundario'] == 'True':
            nuevas_filas.append({'Cueanexo':fila['Cueanexo'], 'ID_NIVEL': 3})
    # Convertimos la lista de diccionarios en un DataFrame
    df2 = pd.DataFrame(nuevas_filas)
    return df2

NIVEL_ESTABLECIMIENTO= poner_nivel( dfEstEducativos_2)

    
# %%CENTROS CULTURALES

CENTROS_CULTURALES = centrosCulturales[['Nombre', 'Domicilio', 'ID_DEPTO', 'Mail ', 'Capacidad']]   
CENTROS_CULTURALES['ID_DEPTO'] = CENTROS_CULTURALES['ID_DEPTO'].astype(str)

def agregar_cero(dataframe):
    dataframe['ID_DEPTO'] = dataframe['ID_DEPTO'].apply(lambda x: '0' + x if len(x) == 4 else x)
    return dataframe



CENTROS_CULTURALES = agregar_cero(CENTROS_CULTURALES)
# selecciono esas columnas del censo 


def soloDominio(dataFrame):
    
    dataFrame = dataFrame.rename(columns={"Mail ": "Mail"}) #Quito el espacio que tenia la columna en su nombre
    
    for i, fila in dataFrame.iterrows():
        email = fila['Mail']   
        if pd.notna(email) and '@' in email:
            email = (email.split('@')[1].split('.')[0]).lower()
            dataFrame.loc[i, 'Mail'] = email #Actualizar el dataFrame
    
    return dataFrame

CENTROS_CULTURALES = soloDominio(CENTROS_CULTURALES)

#%%===========================================================================
# ANALISIS DE DATOS
#=============================================================================
# i)
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

resultado_1 = dd.sql("""
                     SELECT Provincia, Nombre AS Departamento, Jardines, Poblacion_Jardin, Primarias, Poblacion_Primaria, Secundarias, Poblacion_Secundaria
                     FROM CANT_Y_POB AS c
                     INNER JOIN DEPARTAMENTO AS d
                     ON d.ID = c.ID
                     ORDER BY Departamento
                     """).df()                                       

# %% ii)

capMayorA100 = dd.sql("""
               SELECT d.Provincia, d.Nombre, c.capacidad
               FROM DEPARTAMENTO AS d
               INNER JOIN CENTROS_CULTURALES AS c
               ON d.ID = c.ID_DEPTO
               WHERE c.capacidad > 100
              """).df()


consultaSQL = """
                SELECT  DISTINCT cm.Provincia, cm.Nombre AS Departamento, COUNT(*) AS 'Cantidad de CC con cap >100'
                FROM capMayorA100 AS cm
                GROUP BY cm.Provincia, cm.Nombre
                ORDER BY cm.Provincia ASC, COUNT(*) DESC
              """

resultado_2 = dd.sql(consultaSQL).df() #Porque le indicamos que lo devuelva en un dataFrame


# %% iii)

deptosEE = dd.sql("""
               SELECT d.ID, d.Provincia, d.Nombre, COUNT(e.*) AS Cant_EE
               FROM ESTABLECIMIENTOS_EDUCATIVOS AS e
               RIGHT OUTER JOIN DEPARTAMENTO AS d
               ON d.ID = e.ID_DEPTO
               GROUP BY d.Provincia, d.Nombre, d.ID
              """).df()


unionCC = dd.sql("""
               SELECT d.*, COUNT(c.*) AS Cant_CC
               FROM CENTROS_CULTURALES AS c
               RIGHT OUTER JOIN deptosEE AS d
               ON d.ID = c.ID_DEPTO
               GROUP BY d.Provincia, d.Nombre, d.Cant_EE, d.ID
              """).df()

resultado_3 = dd.sql("""
                SELECT u.Provincia, u.Nombre, u.Cant_EE, u.Cant_CC, SUM(h.casos) AS Poblacion_Total
                FROM unionCC AS u
                LEFT OUTER JOIN HABITAN_EN AS h
                ON u.ID = h.ID_DEPTO
                GROUP BY u.Provincia, u.Nombre, u.Cant_EE, u.Cant_CC
                ORDER BY u.Cant_EE DESC, u.Cant_CC DESC, u.Provincia ASC, u.Nombre ASC
              """).df()
              

# %% iv)

CCDominio = dd.sql("""
               SELECT ID_DEPTO, Mail, COUNT(*) AS CantDom
               FROM CENTROS_CULTURALES
               WHERE Mail LIKE '____%'  
               GROUP BY ID_DEPTO, Mail
               ORDER BY ID_DEPTO, Mail
              """).df()

# Con 'WHERE Mail LIKE '____%''  descarto aquellos que no son dominios             
              
consultaSQL = """
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
              """


resultado_4 = dd.sql(consultaSQL).df() #Porque le indicamos que lo devuelva en un dataFrame              


#%%
graf1 = dd.sql("""
               SELECT Provincia, SUM(Cant_CC) AS Cantidad
               FROM resultado_3
               WHERE Provincia != 'Ciudad de Buenos Aires'
               GROUP BY Provincia
               ORDER BY cantidad DESC
              
              """).df()             
#%%
#Grafico 1 
fig, ax = plt.subplots(figsize=(13,5))
graf1.set_index("Provincia")["Cantidad"].plot(kind="bar", ax=ax)
ax.set_xlabel('Provincia', fontsize = 14)
ax.set_ylabel('Cantidad')
ax.bar_label(ax.containers[0], fontsize=12)
ax.tick_params(axis='x', direction='in', length=10, labelsize=14)

#%%
#grafico que acompaña el primer grafico
aux_graf1 = dd.sql(
                """
                SELECT Provincia, SUM(Poblacion_total) AS Poblacion
                FROM resultado_3
                WHERE Provincia != 'Ciudad de Buenos Aires'
                GROUP BY Provincia
                ORDER BY poblacion DESC
                """).df()

fig, ax = plt.subplots(figsize=(13,5))
aux_graf1.set_index("Provincia")["Poblacion"].plot(kind="bar", ax=ax)

ax.set_xlabel('Provincias', fontsize = 14)
ax.set_ylabel('Poblacion_provincia')


# Grafico 2

aux_graf2 = dd.sql("""
                     SELECT Departamento, Jardines, Poblacion_Jardin, Primarias, Poblacion_Primaria, Secundarias, Poblacion_Secundaria
                     FROM resultado_1
                     """).df()   

plt.figure(figsize=(12, 7))

sns.scatterplot(x=aux_graf2['Poblacion_Jardin'], y=aux_graf2['Jardines'], 
                color='#1f77b4', label='Inicial', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=aux_graf2['Poblacion_Primaria'], y=aux_graf2['Primarias'], 
                color='#2ca02c', label='Primaria', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=aux_graf2['Poblacion_Secundaria'], y=aux_graf2['Secundarias'], 
                color='#d62728', label='Secundaria', s=50, edgecolor='black', alpha=0.5)

def add_trendline(x, y, color, label):
    # reshape de los datos para que sklearn pueda trabajar con ellos
    x_reshaped = x.values.reshape(-1, 1)
    y_reshaped = y.values

    # Crear el modelo de regresión sin intercepto (forzando que pase por el origen)
    model = LinearRegression(fit_intercept=False)
    model.fit(x_reshaped, y_reshaped)

    # Predecir los valores y crear la línea de tendencia
    y_pred = model.predict(x_reshaped)

    # Graficar la línea de tendencia
    plt.plot(x, y_pred, color=color, label=label)

add_trendline(aux_graf2['Poblacion_Jardin'], aux_graf2['Jardines'], 'k', 'Tendencia Inicial')
add_trendline(aux_graf2['Poblacion_Primaria'], aux_graf2['Primarias'], 'g', 'Tendencia Primaria')
add_trendline(aux_graf2['Poblacion_Secundaria'], aux_graf2['Secundarias'], 'r', 'Tendencia Secundaria')


# Personalización de etiquetas y título
plt.xlabel("Población del Departamento", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de Establecimientos Educativos (EE)", fontsize=14, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.6)

# Agregar la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)


plt.xlim(0, 10000)  
plt.ylim(0, 200) 



# %% 
# grafico 3
medianas = dd.sql("""
    SELECT Provincia, MEDIAN(Cant_EE) as mediana
    FROM resultado_3
    WHERE Provincia != 'Ciudad de Buenos Aires'
    GROUP BY Provincia
    ORDER BY mediana DESC
    """).df()


aux_graf3 = dd.sql("""
                     SELECT Provincia, Cant_EE
                     FROM resultado_3
                     WHERE Provincia != 'Ciudad de Buenos Aires'
                     """).df()  
                     
plt.figure(figsize=(10, 6))
sns.boxplot(x='Provincia', y='Cant_EE', data=aux_graf3, order=medianas['Provincia'],
            boxprops=dict( facecolor='white',linewidth = 1),
            medianprops=dict(color="green", linewidth=2))

# Agregar título y etiquetas a los ejes
plt.xlabel('Provincia', fontsize=12)
plt.ylabel('Cantidad', fontsize=12)
plt.xticks(rotation=90, fontsize=10)
plt.grid(True, axis='y')

plt.show()
#%%
# grafico 4
# hacer por depto y dividir por poblacion


##SQL
aux_graf4 = dd.sql("""
                   SELECT  Provincia, Nombre AS Departamento, (Cant_EE/ Poblacion_Total)*1000 AS ProporcionEE_cada_mil, (Cant_CC/ Poblacion_Total)*1000 AS ProporcionCC_cada_mil
                   FROM resultado_3
                   GROUP BY Nombre, Cant_EE, Cant_CC, Poblacion_Total, Provincia
                   ORDER BY ProporcionEE_cada_mil DESC, ProporcionCC_cada_mil DESC
                   """).df()

plt.figure(figsize=(12, 7))

# Scatterplot para cada nivel educativo con mejor visibilidad
sns.scatterplot(x=aux_graf4['ProporcionEE_cada_mil'], y=aux_graf4['ProporcionCC_cada_mil'], color='#1f77b4', s=50, edgecolor='black', alpha=0.7)



# Personalización de etiquetas y título
plt.xlabel("Cantidad de EE cada mil habitantes", fontsize=14)
plt.ylabel("Cantidad de CC cada mil habitantes", fontsize=14)

# Personalizar la cuadrícula
plt.grid(True, linestyle='--', alpha=0.7)

plt.xlim(0, 4)  
plt.ylim(0, 0.2)

#%%
#ANEXO

medianas = dd.sql("""
    SELECT Provincia, MEDIAN(Cant_EE) as mediana
    FROM resultado_3
    GROUP BY Provincia
    ORDER BY mediana DESC
    """).df()


aux_graf3 = dd.sql("""
                     SELECT Provincia, Cant_EE
                     FROM resultado_3
                     """).df()  
                     
plt.figure(figsize=(10, 6))
sns.boxplot(x='Provincia', y='Cant_EE', data=aux_graf3, order=medianas['Provincia'],
            boxprops=dict( facecolor='white',linewidth = 1),
            medianprops=dict(color="green", linewidth=2))

# Agregar título y etiquetas a los ejes
plt.xlabel('Provincia', fontsize=12)
plt.ylabel('Cantidad', fontsize=12)
plt.xticks(rotation=90, fontsize=10)
plt.grid(True, axis='y')

plt.show()

plt.figure(figsize=(12, 7))

# Scatterplot para cada nivel educativo con mejor visibilidad
sns.scatterplot(x=aux_graf4['ProporcionEE_cada_mil'], y=aux_graf4['ProporcionCC_cada_mil'], color='#1f77b4', s=50, edgecolor='black', alpha=0.7)



# Personalización de etiquetas y título
plt.xlabel("Cantidad de EE cada mil habitantes", fontsize=14)
plt.ylabel("Cantidad de CC cada mil habitantes", fontsize=14)

# Personalizar la cuadrícula
plt.grid(True, linestyle='--', alpha=0.7)
#%%
plt.figure(figsize=(12, 7))

# Scatterplot para cada nivel educativo con mejor visibilidad
sns.scatterplot(x=aux_graf2['Poblacion_Jardin'], y=aux_graf2['Jardines'], 
                color='#1f77b4', label='Inicial', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=aux_graf2['Poblacion_Primaria'], y=aux_graf2['Primarias'], 
                color='#2ca02c', label='Primaria', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=aux_graf2['Poblacion_Secundaria'], y=aux_graf2['Secundarias'], 
                color='#d62728', label='Secundaria', s=50, edgecolor='black', alpha=0.5)

# Agregar líneas de tendencia para cada nivel educativo
add_trendline(aux_graf2['Poblacion_Jardin'], aux_graf2['Jardines'], 'k', 'Tendencia Inicial')
add_trendline(aux_graf2['Poblacion_Primaria'], aux_graf2['Primarias'], 'g', 'Tendencia Primaria')
add_trendline(aux_graf2['Poblacion_Secundaria'], aux_graf2['Secundarias'], 'r', 'Tendencia Secundaria')

# Personalización de etiquetas y título
plt.xlabel("Población del Departamento", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de Establecimientos Educativos (EE)", fontsize=14, fontweight='bold')

# Activar la cuadrícula con estilo suave
plt.grid(True, linestyle='--', alpha=0.6)

# Agregar la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)

#%% 
# grafico scatter para responder la pregunta general

aux_graf_gral = dd.sql("""
                   SELECT  Nombre, Cant_EE, Cant_CC
                   FROM resultado_3
                   """).df()

sns.scatterplot(x=aux_graf_gral['Cant_EE'], y=aux_graf_gral['Cant_CC'], 
                color='#1f77b4', s=50, edgecolor='black', alpha=0.5)

plt.xlabel("cantidad de EE", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de CC", fontsize=14, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.6)

#%%


plt.figure(figsize=(12, 7))

# Scatterplot para cada nivel educativo con mejor visibilidad
sns.scatterplot(x=aux_graf4['ProporcionEE_cada_mil'], y=aux_graf4['ProporcionCC_cada_mil'], color='#1f77b4', s=50, edgecolor='black', alpha=0.7)



# Personalización de etiquetas y título
plt.xlabel("Cantidad de EE cada mil habitantes", fontsize=14)
plt.ylabel("Cantidad de CC cada mil habitantes", fontsize=14)

# Personalizar la cuadrícula
plt.grid(True, linestyle='--', alpha=0.7)



anexo_3= dd.sql("""
                     SELECT Provincia, Cant_EE
                     FROM resultado_3
                     GROUP BY Provincia, Cant_EE
                     """).df()  
                     
fig, ax = plt.subplots()

anexo_3.boxplot(by=['Provincia'], column= ['Cant_EE'],
             ax=ax, grid=False, showmeans=True)

#Agrega titulo, etiquetas a los ejes
fig.suptitle('')
ax.set_title('Cantidad EE por Jurisdiccion')
ax.set_xlabel('Provincia')
ax.set_ylabel('Cantidad')
ax.tick_params(axis='x', direction='in', rotation = 90, length=4, labelsize=8)



plt.figure(figsize=(12, 7))

# Scatterplot para cada nivel educativo con mejor visibilidad
sns.scatterplot(x=aux_graf4['ProporcionEE_cada_mil'], y=aux_graf4['ProporcionCC_cada_mil'], color='#1f77b4', s=50, edgecolor='black', alpha=0.7)



# Personalización de etiquetas y título
plt.xlabel("Cantidad de EE cada mil habitantes", fontsize=14)
plt.ylabel("Cantidad de CC cada mil habitantes", fontsize=14)
plt.title("Cantidad de CC cada mil habitantes en relacion a la cantidad de EE cada mil habitantes sin acotar", fontsize=16, fontweight='bold')

# Personalizar la cuadrícula
plt.grid(True, linestyle='--', alpha=0.7)

plt.figure(figsize=(12, 7))

# Scatterplot para cada nivel educativo con mejor visibilidad
sns.scatterplot(x=aux_graf2['Poblacion_Jardin'], y=aux_graf2['Jardines'], 
                color='#1f77b4', label='Inicial', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=aux_graf2['Poblacion_Primaria'], y=aux_graf2['Primarias'], 
                color='#2ca02c', label='Primaria', s=50, edgecolor='black', alpha=0.5)

sns.scatterplot(x=aux_graf2['Poblacion_Secundaria'], y=aux_graf2['Secundarias'], 
                color='#d62728', label='Secundaria', s=50, edgecolor='black', alpha=0.5)

# Personalización de etiquetas y título
plt.xlabel("Población del Departamento", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de Establecimientos Educativos (EE)", fontsize=14, fontweight='bold')
plt.title("Cantidad de EE en función de la Población por Nivel Educativo sin acotar", fontsize=16, fontweight='bold')

# Ajuste de escala para mejor visualización si hay mucha variabilidad
#plt.xscale('log')  # Eliminar si no se necesita escala logarítmica

# Activar la cuadrícula con estilo suave
plt.grid(True, linestyle='--', alpha=0.6)

# Agregar la leyenda con mejor visibilidad
plt.legend(title="Nivel Educativo", fontsize=12, title_fontsize=13)


