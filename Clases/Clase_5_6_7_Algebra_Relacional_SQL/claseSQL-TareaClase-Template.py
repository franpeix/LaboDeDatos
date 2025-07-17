# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Clase  : Clase SQL. Script clase. 
Autor  : Pablo Turjanski
Fecha  : 2025-02-03
"""

# Importamos bibliotecas
import pandas as pd
import duckdb as dd


#%%===========================================================================
# Importamos los datasets que vamos a utilizar en este programa
#=============================================================================

carpeta = "~/Downloads/sql/"

# Ejercicios AR-PROJECT, SELECT, RENAME
empleado       = pd.read_csv(carpeta+"empleado.csv")
# Ejercicios AR-UNION, INTERSECTION, MINUS
alumnosBD      = pd.read_csv(carpeta+"alumnosBD.csv")
alumnosTLeng   = pd.read_csv(carpeta+"alumnosTLeng.csv")
# Ejercicios AR-CROSSJOIN
persona        = pd.read_csv(carpeta+"persona.csv")
nacionalidades = pd.read_csv(carpeta+"nacionalidades.csv")
# Ejercicios ¿Mismos Nombres?
se_inscribe_en=pd.read_csv(carpeta+"se_inscribe_en.csv")
materia       =pd.read_csv(carpeta+"materia.csv")
# Ejercicio JOIN múltiples tablas
vuelo      = pd.read_csv(carpeta+"vuelo.csv")    
aeropuerto = pd.read_csv(carpeta+"aeropuerto.csv")    
pasajero   = pd.read_csv(carpeta+"pasajero.csv")    
reserva    = pd.read_csv(carpeta+"reserva.csv")    
# Ejercicio JOIN tuplas espúreas
empleadoRol= pd.read_csv(carpeta+"empleadoRol.csv")    
rolProyecto= pd.read_csv(carpeta+"rolProyecto.csv")    
# Ejercicios funciones de agregación, LIKE, Elección, Subqueries 
# y variables de Python
examen     = pd.read_csv(carpeta+"examen.csv")
# Ejercicios de manejo de valores NULL
examen03 = pd.read_csv(carpeta+"examen03.csv")



#%%===========================================================================
# Ejemplo inicial
#=============================================================================

print(empleado)

consultaSQL = """
               SELECT DISTINCT DNI, Salario
               FROM empleado;
              """

dataframeResultado = dd.sql(consultaSQL).df() #Porque le indicamos que lo devuelva en un dataFrame

print(dataframeResultado)


#%%===========================================================================
# Ejercicios AR-PROJECT <-> SELECT
#=============================================================================
# a.- Listar DNI y Salario de empleados 
consultaSQL = """
                SELECT DISTINCT DNI, Salario
                FROM empleado;
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b.- Listar Sexo de empleados 
consultaSQL = """
                SELECT DISTINCT Sexo
                FROM empleado;
              """

dataframeResultado = dd.sql(consultaSQL).df()

print(dataframeResultado)

#%%-----------
#c.- Listar Sexo de empleados (sin DISTINCT)
consultaSQL = """
                SELECT Sexo
                FROM empleado;
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios AR-SELECT <-> WHERE
#=============================================================================
# a.- Listar de EMPLEADO sólo aquellos cuyo sexo es femenino
consultaSQL = """
                SELECT DISTINCT DNI, Nombre, Sexo, Salario
                FROM empleado
                WHERE Sexo = 'F';
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
#b.- Listar de EMPLEADO aquellos cuyo sexo es femenino y su salario es mayor a $15.000
consultaSQL = """
                SELECT DISTINCT DNI, Nombre, Sexo, Salario
                FROM empleado
                WHERE Sexo = 'F' AND Salario > 15000
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios AR-RENAME <-> AS
#=============================================================================
#a.- Listar DNI y Salario de EMPLEADO, y renombrarlos como id e Ingreso
consultaSQL = """
                SELECT DISTINCT DNI AS id, Salario AS Ingreso
                FROM empleado
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    INICIO -->           EJERCICIO Nro. 01                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IMPORTANTE: Recordar que se utilizaran los datos de vuelo, aeropuerto, pasajero y reserva

#%%===========================================================================
# EJERCICIOS PARA REALIZAR DE MANERA INDIVIDUAL --> EJERCICIO Nro. 01
#=============================================================================
# Ejercicio 01.1.- Retornar Codigo y Nombre de los aeropuertos de Londres
consultaSQL = """
                SELECT DISTINCT Codigo, Nombre
                FROM aeropuerto
                WHERE Ciudad = 'Londres'
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# Ejercicio 01.2.- ¿Qué retorna 
#                       SELECT DISTINCT Ciudad AS City 
#                       FROM aeropuerto 
#                       WHERE Codigo='ORY' OR Codigo='CDG'; ?
consultaSQL = """
                SELECT DISTINCT Ciudad AS City 
                FROM aeropuerto 
                WHERE Codigo='ORY' OR Codigo='CDG';
              """

dataframeResultado = dd.sql(consultaSQL).df()

#Retorna la columna Ciudad renombrada como City, cuyas filas seran aquellas que posean el Codigo con 'ORY' o 'CDG'


#%% -----------
# Ejercicio 01.3.- Obtener los números de vuelo que van desde CDG hacia LHR
consultaSQL = """
                SELECT DISTINCT Numero  
                FROM vuelo 
                WHERE Origen='CDG' AND Destino='LHR';
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# Ejercicio 01.4.- Obtener los números de vuelo que van desde CDG hacia LHR o viceversa
consultaSQL = """
                SELECT DISTINCT Numero  
                FROM vuelo 
                WHERE (Origen='CDG' AND Destino='LHR') 
                    OR 
                    (Origen='LHR' AND Destino='CDG') ;
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# Ejercicio 01.5.- Devolver las fechas de reservas cuyos precios son mayores a $200
consultaSQL = """
                SELECT DISTINCT Fecha  
                FROM reserva 
                WHERE Precio > 200;
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    FIN -->              EJERCICIO Nro. 01                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
#=============================================================================
# Ejercicios AR-UNION, INTERSECTION, MINUS <-> UNION, INTERSECTION, EXCEPT
#=============================================================================
# a1.- Listar a los alumnos que cursan BDs o TLENG

consultaSQL = """
                SELECT DISTINCT *
                FROM alumnosBD
            UNION
                SELECT DISTINCT *
                FROM alumnosTLeng
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% -----------
# a2.- Listar a los alumnos que cursan BDs o TLENG (usando UNION ALL)

consultaSQL = """
                SELECT DISTINCT *
                FROM alumnosBD
            UNION ALL
                SELECT DISTINCT *
                FROM alumnosTLeng
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# b.- Listar a los alumnos que cursan simultáneamente BDs y TLENG

consultaSQL = """
                SELECT DISTINCT *
                FROM alumnosBD
            INTERSECT
                SELECT DISTINCT *
                FROM alumnosTLeng
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% -----------
# c.- Listar a los alumnos que cursan BDs y no cursan TLENG 

consultaSQL = """
                SELECT DISTINCT *
                FROM alumnosBD
            EXCEPT
                SELECT DISTINCT *
                FROM alumnosTLeng
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    INICIO -->           EJERCICIO Nro. 02                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IMPORTANTE: Recordar que se utilizaran los datos de vuelo, aeropuerto, pasajero y reserva

#=============================================================================
#  EJERCICIOS PARA REALIZAR DE MANERA INDIVIDUAL --> EJERCICIO Nro. 02
#=============================================================================
# Ejercicio 02.1.- Devolver los números de vuelo que tienen reservas generadas (utilizar intersección)
consultaSQL = """
                SELECT DISTINCT Numero
                FROM vuelo
            INTERSECT
                SELECT DISTINCT NroVuelo
                FROM reserva
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 02.2.- Devolver los números de vuelo que aún no tienen reservas
consultaSQL = """
                SELECT DISTINCT Numero
                FROM vuelo
            EXCEPT
                SELECT DISTINCT NroVuelo
                FROM reserva
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 02.3.- Retornar los códigos de aeropuerto de los que parten o arriban los vuelos
consultaSQL = """
                SELECT DISTINCT Codigo
                FROM aeropuerto
            INTERSECT
            (
                SELECT DISTINCT Origen
                FROM vuelo
            UNION
                SELECT DISTINCT Destino
                FROM vuelo
            )
              """
              
dataframeResultado = dd.sql(consultaSQL).df()



#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    FIN -->              EJERCICIO Nro. 02                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#=============================================================================
# Ejercicios AR-... JOIN <-> ... JOIN
#=============================================================================
# a1.- Listar el producto cartesiano entre las tablas persona y nacionalidades

consultaSQL = """
                SELECT DISTINCT *
                FROM persona
                CROSS JOIN nacionalidades
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# a2.- Listar el producto cartesiano entre las tablas persona y nacionalidades (sin usar CROSS JOIN)

consultaSQL = """
                SELECT DISTINCT *
                FROM persona, nacionalidades
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% --------------------------------------------------------------------------------------------
# Carga los nuevos datos del dataframe persona para los ejercicios de AR-INNER y LEFT OUTER JOIN
# ----------------------------------------------------------------------------------------------
persona        = pd.read_csv(carpeta+"persona_ejemplosJoin.csv")
# ----------------------------------------------------------------------------------------------
# b1.- Vincular las tablas persona y nacionalidades a través de un INNER JOIN

consultaSQL = """
                SELECT DISTINCT *
                FROM persona
                INNER JOIN nacionalidades
                ON nacionalidad = IDN
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b2.- Vincular las tablas persona y nacionalidades (sin usar INNER JOIN)

consultaSQL = """
                SELECT DISTINCT *
                FROM persona, nacionalidades
                WHERE nacionalidad=IDN
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# c.- Vincular las tablas persona y nacionalidades a través de un LEFT OUTER JOIN

consultaSQL = """
                SELECT DISTINCT *
                FROM persona
                LEFT OUTER JOIN nacionalidades
                ON nacionalidad = IDN
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios SQL - ¿Mismos Nombres?
#=============================================================================
# a.- Vincular las tablas Se_inscribe_en y Materia. Mostrar sólo LU y Nombre de materia

#Para no escribir todo el nombre de la tabla, puedo renombrarlas por nombres mas chicos con AS

consultaSQL = """
               SELECT DISTINCT LU, Nombre
               FROM se_inscribe_en AS i
               INNER JOIN materia AS m
               ON i.Codigo_materia = m.Codigo_materia
              """

dataframeResultado = dd.sql(consultaSQL).df()

    
#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    INICIO -->           EJERCICIO Nro. 03                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# IMPORTANTE: Recordar que se utilizaran los datos de vuelo, aeropuerto, pasajero y reserva

#%%===========================================================================
# EJERCICIOS PARA REALIZAR DE MANERA INDIVIDUAL --> EJERCICIO Nro. 03
#=============================================================================
# Ejercicio 03.1.- Devolver el nombre de la ciudad de partida del vuelo número 165

consultaSQL = """
                SELECT DISTINCT Ciudad
                FROM aeropuerto
                INNER JOIN vuelo
                ON origen = codigo
                WHERE numero = 165
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 03.2.- Retornar el nombre de las personas que realizaron reservas a un valor menor a $200

consultaSQL = """
                SELECT DISTINCT Nombre 
                FROM pasajero
                INNER JOIN reserva
                ON reserva.DNI = pasajero.DNI
                WHERE precio < 200
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# Ejercicio 03.3.- Obtener Nombre, Fecha y Destino del Viaje de todos los pasajeros que vuelan desde Madrid

vuelosDeMadrid = dd.sql("""
                       SELECT DISTINCT *
                       FROM vuelo
                       WHERE Origen = 'MAD'

              """).df()

dniPersonasDesdeMadrid = dd.sql("""
                                SELECT DISTINCT *
                                FROM vuelosDeMadrid AS vam
                                INNER JOIN reserva AS r
                                ON vam.Numero = r.NroVuelo
              """).df()

consultaSQL = """
                SELECT DISTINCT Nombre, Fecha, Destino
                FROM dniPersonasDesdeMadrid AS dnipm
                INNER JOIN pasajero AS p
                ON dnipm.DNI = p.DNI
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%% # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # #                                                                     # #
# #    FIN -->              EJERCICIO Nro. 03                             # #
 # #                                                                     # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    
#%%===========================================================================
# Ejercicios SQL - Join de varias tablas en simultáneo
#=============================================================================
# a.- Vincular las tablas Reserva, Pasajero y Vuelo. Mostrar sólo Fecha de reserva, hora de salida del vuelo y nombre de pasajero.

#Hacer cross join (producto cartesiano)    
consultaSQL = """
                SELECT r.Fecha, v.Salida, p.Nombre
                FROM reserva AS r, vuelo AS v, pasajero AS p
                WHERE r.DNI=p.DNI AND r.NroVuelo=v.Numero
              """

dataframeResultado = dd.sql(consultaSQL).df()

    
#%%===========================================================================
# Ejercicios SQL - Tuplas espúreas
#=============================================================================
# a.- Vincular (JOIN)  EmpleadoRol y RolProyecto para obtener la tabla original EmpleadoRolProyecto
    
consultaSQL = """
                SELECT DISTINCT e.empleado, e.rol, p.proyecto
                FROM empleadoRol AS e
                INNER JOIN rolProyecto AS p
                ON e.rol = p.rol
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios SQL - Funciones de agregación
#=============================================================================
# a.- Usando sólo SELECT contar cuántos exámenes fueron rendidos (en total)
    
consultaSQL = """
                SELECT COUNT(*) AS cantidadExamenes
                FROM examen
              """

dataframeResultado = dd.sql(consultaSQL).df()

#El (*) del COUNT indica que agarre la dila entera, cuantas filas enteras distintas hay

#%%-----------
# b1.- Usando sólo SELECT contar cuántos exámenes fueron rendidos en cada Instancia
    
consultaSQL = """
                SELECT Instancia, COUNT(*) AS Asistieron
                FROM examen
                GROUP BY Instancia
              """

dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# b2.- Usando sólo SELECT contar cuántos exámenes fueron rendidos en cada Instancia (ordenado por instancia)
    
consultaSQL = """
                SELECT Instancia, COUNT(*) AS Asistieron
                FROM examen
                GROUP BY Instancia
                ORDER BY Instancia ASC
              """

dataframeResultado = dd.sql(consultaSQL).df()

#Por default es ASC, si quiero que sea descendente pongo DESC

#%%-----------
# b3.- Ídem ejercicio anterior, pero mostrar sólo las instancias a las que asistieron menos de 4 Estudiantes
    
consultaSQL = """
                SELECT Instancia, COUNT(*) AS Asistieron
                FROM examen
                GROUP BY Instancia
                HAVING Asistieron < 4
                ORDER BY Instancia
              """

dataframeResultado = dd.sql(consultaSQL).df()

#No puedo utilizar el WHERE porque este evalua por fila, no por columna
#El HAVING es para restingir lo que te realice el GROPU BY

#%%-----------
# c.- Mostrar el promedio de edad de los estudiantes en cada instancia de examen
    
consultaSQL = """
                SELECT Instancia, AVG(edad) AS PromedioEdad
                FROM examen
                GROUP BY Instancia
                ORDER BY Instancia
              """

dataframeResultado = dd.sql(consultaSQL).df()

#Tambien se puede usar MEAN()

#%%===========================================================================
# Ejercicios SQL - LIKE")
#=============================================================================
# a1.- Mostrar cuál fue el promedio de notas en cada instancia de examen, sólo para instancias de parcial.
    
consultaSQL = """
                SELECT Instancia, AVG(Nota) as PromedioNota
                FROM examen
                GROUP BY Instancia
                HAVING instancia='Parcial-01' OR
                       instancia='Parcial-02'
                ORDER BY Instancia
              """

dataframeResultado = dd.sql(consultaSQL).df()

#En este caso tambien se puede usar WHERE porque se evaluan las filas

#%%-----------
# a2.- Mostrar cuál fue el promedio de notas en cada instancia de examen, sólo para instancias de parcial. Esta vez usando LIKE.
    
consultaSQL = """
                SELECT Instancia, AVG(Nota) as PromedioNota
                FROM examen
                GROUP BY Instancia
                HAVING instancia LIKE 'Parc%'
                ORDER BY Instancia
              """

dataframeResultado = dd.sql(consultaSQL).df()

#Aqui tambien se puede usar el WHERE
#El % representa un comodin, se utiliza unicamente en Strings y unicamente se puede utilizar con LIKE


#%%===========================================================================
# Ejercicios SQL - Eligiendo
#=============================================================================
# a1.- Listar a cada alumno que rindió el Parcial-01 y decir si aprobó o no (se aprueba con nota >=4).
    
consultaSQL = """
                SELECT Nombre, Nota,
                    CASE WHEN Nota >= 4
                        THEN 'APROBÓ'
                        ELSE 'NO APROBÓ'
                    END AS Estado,
                    FROM examen
                    WHERE Instancia = 'Parcial-01'
                    ORDER BY Instancia
              """

dataframeResultado = dd.sql(consultaSQL).df()

#Los CASE van entre comas

#%%-----------
# a2.- Modificar la consulta anterior para que informe cuántos estudiantes aprobaron/reprobaron en cada instancia.
    
consultaSQL = """
                SELECT Instancia,
                    CASE WHEN Nota >= 4 
                        THEN 'APROBÓ'
                        ELSE 'NO APROBÓ'
                    END AS Estado,
                    COUNT (*) AS Cantidad
                    FROM examen
                    GROUP BY Instancia, Estado
                    ORDER BY Instancia
              """

dataframeResultado = dd.sql(consultaSQL).df()

#El COUNT va acompañado del GROUP BY, asi, defino por que criterio quiero que me cree la nueva columna con las cantidades
#Las cosas que estan en el SELECT tienen que estar en el GROUP BY
#Si no esta el GROUP BY, el COUNT te recorre todas la filas
#%%===========================================================================
# Ejercicios SQL - Subqueries
#=============================================================================
#a.- Listar los alumnos que en cada instancia obtuvieron una nota mayor al promedio de dicha instancia

promediosPorParcial = dd.sql("""
                                SELECT DISTINCT Instancia, AVG(Nota) AS Promedio
                                FROM examen
                                GROUP BY Instancia
              """).df()


promediosPorParcialConExamen = dd.sql("""
                                SELECT DISTINCT e.*, ppp.Promedio
                                FROM examen AS e
                                INNER JOIN promediosPorParcial AS ppp
                                ON e.Instancia = ppp.Instancia
              """).df()

consultaSQL = """
                SELECT Nombre, Instancia, Nota
                FROM promediosPorParcialConExamen
                WHERE Nota > Promedio
                ORDER BY Instancia, Nota DESC
              """


dataframeResultado = dd.sql(consultaSQL).df()

# e.* significa que de la tabla examen (examen AS e) me devuelve todas las columnas


###Otra forma
consultaSQL = """
                SELECT e1.Nombre, e1.Instancia, e1.Nota
                FROM examen AS e1
                WHERE e1.Nota > (
                    SELECT AVG(e2.Nota)
                    FROM examen as e2
                    WHERE e2.Instancia = e1.Instancia
                    )
                ORDER BY Instancia, Nota DESC
              """


#Es responsabilidad del programador asegurar que el subquerie devolvera una sola fila
#Simbolo de distinto : <>
#%%-----------
# b.- Listar los alumnos que en cada instancia obtuvieron la mayor nota de dicha instancia

consultaSQL = """
                SELECT e1.Nombre, e1.Instancia, e1.Nota
                FROM examen AS e1
                WHERE e1.Nota = (
                    SELECT MAX(e2.Nota)
                    FROM examen AS e2
                    WHERE e2.Instancia = e1.Instancia
                    )
                ORDER BY e1.Instancia, e1.Nota DESC
              """

dataframeResultado = dd.sql(consultaSQL).df()


#Cuando tenemos mas de un valor devuelto dentro del WHERE (nos devuelve varias filas) operador Multiple-Rows: IN, ANY, ALL, EXISTS
consultaSQL = """
                SELECT e1.Nombre, e1.Instancia, e1.Nota
                FROM examen AS e1
                WHERE e1.Nota >= ALL(
                    SELECT e2.Nota
                    FROM examen AS e2
                    WHERE e2.Instancia = e1.Instancia
                    )
                ORDER BY e1.Instancia, e1.Nota DESC
              """
              
#%%-----------
# c.- Listar el nombre, instancia y nota sólo de los estudiantes que no rindieron ningún Recuperatorio

consultaSQL = """
                SELECT e1.Nombre, e1.Instancia, e1.Nota
                FROM examen AS e1
                WHERE e1.Nombre NOT IN(
                    SELECT e2.Nombre
                    FROM examen AS e2
                    WHERE (e2.Instancia = 'Recuperatorio-01'
                    OR e2.Instancia = 'Recuperatorio-02')
                    )
                ORDER BY e1.Nombre
              """

dataframeResultado = dd.sql(consultaSQL).df()

consultaSQL = """
                SELECT e1.Nombre, e1.Instancia, e1.Nota
                FROM examen AS e1
                WHERE NOT EXISTS(
                    SELECT *
                    FROM examen AS e2
                    WHERE e2.Nombre = e1.Nombre
                    AND e2.Instancia LIKE 'Recuperatorio%'
                    )
                ORDER BY e1.Nombre ASC, e1.Instancia ASC
              """

#NOT EXISTS significa que me da True si el resultado es vacio, el NOT IN me da una lista
#%%===========================================================================
# Ejercicios SQL - Integrando variables de Python
#=============================================================================
# a.- Mostrar Nombre, Instancia y Nota de los alumnos cuya Nota supera el umbral indicado en la variable de Python umbralNota

umbralNota = 7

consultaSQL = f"""
                SELECT Nombre, Instancia, Nota
                FROM examen
                WHERE Nota > {umbralNota}
                ORDER BY Nombre ASC, Instancia ASC
              """

dataframeResultado = dd.sql(consultaSQL).df()

#Que reemplaze lo que esta entre llaves con el valor que esta en la variable

consultaSQL = """
                SELECT Nombre, Instancia, Nota
                FROM examen
                WHERE Nota > """ + str(umbralNota) +
                """ORDER BY Nombre ASC, Instancia ASC"""

#%%===========================================================================
# Ejercicios SQL - Manejo de NULLs
#=============================================================================
# a.- Listar todas las tuplas de Examen03 cuyas Notas son menores a 9

consultaSQL = """
                SELECT *
                FROM examen03 
                WHERE Nota < 9
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b.- Listar todas las tuplas de Examen03 cuyas Notas son mayores o iguales a 9

consultaSQL = """
                SELECT *
                FROM examen03 
                WHERE Nota >= 9
              """


dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# c.- Listar el UNION de todas las tuplas de Examen03 cuyas Notas son menores a 9 y las que son mayores o iguales a 9

consultaSQL = """
                SELECT *
                FROM examen03 
                WHERE Nota < 9
            UNION
                SELECT *
                FROM examen03 
                WHERE Nota >= 9
            """
            
dataframeResultado = dd.sql(consultaSQL).df()           

#El WHERE elimina toda condicion NULL o FALSE, se queda unicamente con los TRUE

#%%-----------
# d1.- Obtener el promedio de notas

consultaSQL = """
                SELECT AVG(Nota) AS NotaPromedio
                FROM examen03
              """


dataframeResultado = dd.sql(consultaSQL).df()


#%%-----------
# d2.- Obtener el promedio de notas (tomando a NULL==0)

consultaSQL = """
                SELECT AVG(
                    CASE WHEN Nota IS NULL
                    THEN 0
                    ELSE Nota
                    END) AS NotaPromedio
                FROM examen03
              """


dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
# Ejercicios SQL - Mayúsculas/Minúsculas
#=============================================================================
# a.- Consigna: Transformar todos los caracteres de las descripciones de los roles a mayúscula

consultaSQL = """
                SELECT empleado, UPPER(rol) AS rol
                FROM empleadoRol
              """

dataframeResultado = dd.sql(consultaSQL).df()

#%%-----------
# b.- Consigna: Transformar todos los caracteres de las descripciones de los roles a minúscula

consultaSQL = """
                SELECT empleado, LOWER(rol) AS rol
                FROM empleadoRol
              """

dataframeResultado = dd.sql(consultaSQL).df()




#%%===========================================================================
# Ejercicios SQL - Reemplazos
#=============================================================================
# a.- Consigna: En la descripción de los roles de los empleados reemplazar las ñ por ni

consultaSQL = """
                SELECT empleado, REPLACE(rol, 'ñ', 'ni') AS rol
                FROM empleadoRol
              """

dataframeResultado = dd.sql(consultaSQL).df()

#Si quiero hacer otro replace , seria: 
consultaSQL = """
                    SELECT empleado, REPLACE(
                                            REPLACE(rol, 'ñ', 'ni'),
                                            'i', 'A')
                                    AS rol
                    FROM empleadoRol
                    """

#(Sobre que campo, que reemplazar, por que reemplazar)

#%%===========================================================================
# Ejercicios SQL - Desafío
#=============================================================================
# a.- Mostrar para cada estudiante las siguientes columnas con sus datos: Nombre, Sexo, Edad, Nota-Parcial-01, Nota-Parcial-02, Recuperatorio-01 y , Recuperatorio-02

# ... Paso 1: Obtenemos los datos de los estudiantes

alumnos = dd.sql("""
                SELECT DISTINCT Nombre, Sexo, Edad
                FROM examen
              """).df()

notasParcial1 = dd.sql("""
                SELECT Nombre, Nota AS Parcial_01
                FROM examen
                WHERE Instancia = 'Parcial-01'
              """).df()
              
notasParcial2 = dd.sql("""
                SELECT Nombre, Nota AS Parcial_02
                FROM examen
                WHERE Instancia = 'Parcial-02'
              """).df()

notasRecu1 = dd.sql("""
                SELECT Nombre, Nota AS Recuperatorio_01
                FROM examen
                WHERE Instancia = 'Recuperatorio-01'
              """).df()

notasRecu2 = dd.sql("""
                SELECT Nombre, Nota AS Recuperatorio_02
                FROM examen
                WHERE Instancia = 'Recuperatorio-02'
              """).df()

alumnosParcial1 = dd.sql("""
                SELECT DISTINCT a.*, np1.Parcial_01
                FROM alumnos AS a
                LEFT OUTER JOIN notasParcial1 AS np1
                ON a.Nombre = np1.Nombre 
              """).df()

alumnosParciales = dd.sql("""
                SELECT DISTINCT ap1.*, np2.Parcial_02
                FROM alumnosParcial1 AS ap1
                LEFT OUTER JOIN notasParcial2 AS np2
                ON ap1.Nombre = np2.Nombre 
              """).df()
              
alumnosParcialesRecu1 = dd.sql("""
                SELECT DISTINCT ap.*, nr1.Recuperatorio_01
                FROM alumnosParciales AS ap
                LEFT OUTER JOIN notasRecu1 AS nr1
                ON ap.Nombre = nr1.Nombre 
              """).df()

consultaSQL = """
                SELECT DISTINCT apr1.*, nr2.Recuperatorio_02
                FROM alumnosParcialesRecu1 AS apr1
                LEFT OUTER JOIN notasRecu2 AS nr2
                ON apr1.Nombre = nr2.Nombre 
                ORDER BY apr1.Nombre
              """

desafio_01 = dd.sql(consultaSQL).df()

#Otra forma:
estudiantes = dd.sql("""
                SELECT DISTINCT Nombre, Sexo, Edad
                FROM examen
                ORDER BY Nombre
              """).df()

parcial_01 = dd.sql("""
                SELECT est.Nombre, est.Sexo, est.Edad, ex.Nota AS Parcial_01
                FROM estudiantes AS est
                LEFT OUTER JOIN examen AS ex
                ON est.Nombre = ex.Nombre
                WHERE ex.Instancia = 'Parcial-01'
              """).df()
              
parcial_02 = dd.sql("""
                SELECT pre.*, ex.Nota AS Parcial_02
                FROM parcial_01 AS pre
                LEFT OUTER JOIN examen AS ex
                ON pre.Nombre = ex.Nombre AND ex.Instancia = 'Parcial-02'
              """).df()

recu_01 = dd.sql("""
                SELECT pre.*, ex.Nota AS Recuperatorio_01
                FROM parcial_02 AS pre
                LEFT OUTER JOIN examen AS ex
                ON pre.Nombre = ex.Nombre AND ex.Instancia = 'Recuperatorio-01'
              """).df()

recu_02 = dd.sql("""
                SELECT pre.*, ex.Nota AS Recuperatorio_02
                FROM recu_01 AS pre
                LEFT OUTER JOIN examen AS ex
                ON pre.Nombre = ex.Nombre AND ex.Instancia = 'Recuperatorio-02'
                ORDER BY pre.Nombre
              """).df()

#La consulta será lo ultimo que pedimos

consultaSQL = """
                SELECT pre.*, ex.Nota AS Recuperatorio_02
                FROM recu_01 AS pre
                LEFT OUTER JOIN examen AS ex
                ON pre.Nombre = ex.Nombre AND ex.Instancia = 'Recuperatorio-02'
                ORDER BY pre.Nombre
              """

desafio_01 = dd.sql(consultaSQL).df()

#%% -----------
# b.- Agregar al ejercicio anterior la columna Estado, que informa si el alumno aprobó la cursada (APROBÓ/NO APROBÓ). Se aprueba con 4.

              
consultaSQL = """
                 SELECT DISTINCT *,
                     CASE WHEN ((Parcial_01 >= 4
                                     OR Recuperatorio_01 >= 4)
                                AND (Parcial_02 >= 4
                                     OR Recuperatorio_02 >= 4))
                     THEN 'APROBÓ'
                     ELSE 'NO APROBÓ'
                     END AS Estado
                FROM desafio_01
                ORDER BY Nombre
              """

desafio_02 = dd.sql(consultaSQL).df()



#%% -----------
# c.- Generar la tabla Examen a partir de la tabla obtenida en el desafío anterior.

parcial_01 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Parcial-01' AS Instancia, Parcial_01 AS Nota 
                FROM desafio_02
                WHERE Parcial_01 IS NOT NULL
              """).df()
              
parcial_02 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Parcial-02' AS Instancia, Parcial_02 AS Nota 
                FROM desafio_02
                WHERE Parcial_02 IS NOT NULL
              """).df()
              
recu_01 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Recuperatorio-01' AS Instancia, Recuperatorio_01 AS Nota 
                FROM desafio_02
                WHERE Recuperatorio_01 IS NOT NULL
              """).df()
              
recu_02 = dd.sql("""
                SELECT Nombre, Sexo, Edad, 'Recuperatorio-02' AS Instancia, Recuperatorio_02 AS Nota 
                FROM desafio_02
                WHERE Recuperatorio_02 IS NOT NULL
              """).df()

consultaSQL = """
                    SELECT DISTINCT *
                    FROM parcial_01
                UNION
                    SELECT DISTINCT *
                    FROM parcial_02
                UNION 
                    SELECT DISTINCT *
                    FROM recu_01
                UNION
                    SELECT DISTINCT *
                    FROM recu_02
                ORDER BY Instancia
              """

desafio_03 = dd.sql(consultaSQL).df()

