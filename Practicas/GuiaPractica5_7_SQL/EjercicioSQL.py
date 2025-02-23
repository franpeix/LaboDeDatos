# -*- coding: utf-8 -*-
"""
Materia: Laboratorio de datos - FCEyN - UBA
Clase  : Clase SQL. Script clase. 
Autor  : Francisco Peix
Fecha  : 2025-02-03
"""

# Importamos bibliotecas
import pandas as pd
import duckdb as dd


#%%===========================================================================
# Importamos los datasets que vamos a utilizar en este programa
#=============================================================================

carpeta = "~/Downloads/GuiaPracticaSQL/"

grupoetario       = pd.read_csv(carpeta+"grupoetario.csv")
provincia      = pd.read_csv(carpeta+"provincia.csv")
tipoevento   = pd.read_csv(carpeta+"tipoevento.csv")
casos        = pd.read_csv(carpeta+"casos.csv")
departamento = pd.read_csv(carpeta+"departamento.csv")
#%%===========================================================================
#A. Consultas sobre una tabla
# %%
# a. Listar sólo los nombres de todos los departamentos que hay en la tabla
# departamento (dejando los registros repetidos).

consultaSQL = """
               SELECT descripcion 
               FROM departamento;
              """

dataframeResultado = dd.sql(consultaSQL).df() #Porque le indicamos que lo devuelva en un dataFrame


# %%
# b. Listar sólo los nombres de todos los departamentos que hay en la tabla
# departamento (eliminando los registros repetidos).

consultaSQL = """
               SELECT DISTINCT descripcion
               FROM departamento;
              """

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# c. Listar sólo los códigos de departamento y sus nombres, de todos los
# departamentos que hay en la tabla departamento

consultaSQL = """
               SELECT id, descripcion
               FROM departamento;
              """

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# d. Listar todas las columnas de la tabla departamento.

consultaSQL = """
               SELECT *
               FROM departamento;
              """

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# e. Listar los códigos de departamento y nombres de todos los departamentos
# que hay en la tabla departamento. Utilizar los siguientes alias para las
# columnas: codigo_depto y nombre_depto, respectivamente.

consultaSQL = """
               SELECT  id AS codigo_depto, descripcion AS nombre_depto
               FROM departamento;
              """

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# f. Listar los registros de la tabla departamento cuyo código de provincia es
# igual a 54

consultaSQL = """
               SELECT DISTINCT id
               FROM departamento
               WHERE id_provincia = 54;
              """

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# g. Listar los registros de la tabla departamento cuyo código de provincia es
# igual a 22, 78 u 86.

consultaSQL = """
               SELECT  *
               FROM departamento
               WHERE (
                   id_provincia = 22
                   OR id_provincia = 78
                   OR id_provincia = 86
                   )
              """

dataframeResultado = dd.sql(consultaSQL).df() 


# %%
# h. Listar los registros de la tabla departamento cuyos códigos de provincia se
# encuentren entre el 50 y el 59 (ambos valores inclusive).

consultaSQL = """
               SELECT  *
               FROM departamento
               WHERE (
                   id_provincia >= 50
                   AND id_provincia <= 59
                   )
              """

dataframeResultado = dd.sql(consultaSQL).df() 

#%%===========================================================================
#B. Consultas multitabla (INNER JOIN)
# %%
# a. Devolver una lista con los código y nombres de departamentos, asociados al
# nombre de la provincia al que pertenecen.

consultaSQL = """
               SELECT DISTINCT d.id AS codigo, d.descripcion AS nombre_dpto, p.descripcion  AS nombre_prov
               FROM departamento AS d
               INNER JOIN provincia AS p
               ON d.id_provincia = p.id
              """

dataframeResultado = dd.sql(consultaSQL).df() 



# %%
# b. Devolver los casos registrados en la provincia de “Chaco”.

infoChaco = dd.sql("""
               SELECT DISTINCT *
               FROM provincia
               WHERE descripcion = 'Chaco'
              """).df()
              
deptoChaco = dd.sql("""
               SELECT DISTINCT d.id, d.descripcion, d.id_provincia
               FROM departamento AS d
               INNER JOIN infoChaco AS ic
               ON d.id_provincia = ic.id
              """).df()
              
consultaSQL = """
               SELECT DISTINCT c.id, c.id_tipoevento, c.anio, c.semana_epidemiologica, c.id_depto, c.id_grupoetario, c.cantidad  
               FROM casos AS c
               INNER JOIN deptoChaco AS dc
               ON c.id_depto = dc.id
              """

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# c. Devolver aquellos casos de la provincia de “Buenos Aires” cuyo campo
# cantidad supere los 10 casos.

infoBsAs = dd.sql("""
               SELECT DISTINCT *
               FROM provincia
               WHERE descripcion = 'Buenos Aires'
              """).df()
              
deptoBsAs = dd.sql("""
               SELECT DISTINCT d.id, d.descripcion, d.id_provincia
               FROM departamento AS d
               INNER JOIN infoBsAs AS iBA
               ON d.id_provincia = iBA.id
              """).df()
              
consultaSQL = """
               SELECT DISTINCT c.id, c.id_tipoevento, c.anio, c.semana_epidemiologica, c.id_depto, c.id_grupoetario, c.cantidad  
               FROM casos AS c
               INNER JOIN deptoChaco AS dc
               ON c.id_depto = dc.id AND c.cantidad > 10
              """

dataframeResultado = dd.sql(consultaSQL).df() 

#%%===========================================================================
# C. Consultas multitabla (OUTER JOIN)
# %%
# a. Devolver un listado con los nombres de los departamentos que no tienen
# ningún caso asociado.

consultaSQL = """
               SELECT DISTINCT d.descripcion AS nombre_dpto
               FROM departamento AS d
               LEFT OUTER JOIN casos AS c
               ON d.id = c.id_depto
               WHERE c.id_depto IS NULL;
              """              

dataframeResultado = dd.sql(consultaSQL).df() 


# %%
# b. Devolver un listado con los tipos de evento que no tienen ningún caso
# asociado.

consultaSQL = """
               SELECT DISTINCT te.descripcion AS nombre_evento
               FROM tipoevento AS te
               LEFT OUTER JOIN casos AS c
               ON te.id = c.id_tipoevento
               WHERE c.id_depto IS NULL;
              """              

dataframeResultado = dd.sql(consultaSQL).df() 

#%%===========================================================================
# D. Consultas resumen
# %%
# a. Calcular la cantidad total de casos que hay en la tabla casos.

consultaSQL = """
               SELECT SUM(cantidad) AS cantCasosTotales
               FROM casos
              """              

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# b. Calcular la cantidad total de casos que hay en la tabla casos para cada año y
# cada tipo de caso. Presentar la información de la siguiente manera:
# descripción del tipo de caso, año y cantidad. Ordenarlo por tipo de caso
# (ascendente) y año (ascendente).

casosConEvento = dd.sql("""
               SELECT t.descripcion AS tipoCaso, c.anio, c.id, c.semana_epidemiologica, id_depto, id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN tipoevento AS t
               ON c.id_tipoevento = t.id
              """).df()
consultaSQL = """
               SELECT tipoCaso, anio, SUM(cantidad) as cantTotalCasos
               FROM casosConEvento
               GROUP BY tipoCaso, anio
               ORDER BY tipoCaso, anio ASC
              """              

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# c. Misma consulta que el ítem anterior, pero sólo para el año 2019.

casosConEvento = dd.sql("""
               SELECT t.descripcion AS tipoCaso, c.anio, c.id, c.semana_epidemiologica, id_depto, id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN tipoevento AS t
               ON c.id_tipoevento = t.id
              """).df()
consultaSQL = """
               SELECT tipoCaso, anio, SUM(cantidad) as cantTotalCasos
               FROM casosConEvento
               WHERE anio = 2019
               GROUP BY tipoCaso, anio
               ORDER BY tipoCaso, anio ASC
              """              

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# d. Calcular la cantidad total de departamentos que hay por provincia. Presentar
# la información ordenada por código de provincia.

consultaSQL = """
               SELECT id_provincia, COUNT(*) AS cantDeptos
               FROM departamento
               GROUP BY id_provincia
               ORDER BY id_provincia
              """              

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# e. Listar los departamentos con menos cantidad de casos en el año 2019.

deptosConCasos = dd.sql("""
               SELECT DISTINCT d.descripcion AS depto, c.anio, c.id, c.id_tipoevento, c.semana_epidemiologica, c.id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN departamento AS d
               ON c.id_depto = d.id
              """).df()


consultaSQL = """
               SELECT depto, SUM(cantidad) AS cantCasos
               FROM deptosConCasos
               WHERE anio = 2019
               GROUP BY depto, cantidad
               ORDER BY cantCasos ASC
              """              

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# f. Listar los departamentos con más cantidad de casos en el año 2020.

deptosConCasos = dd.sql("""
               SELECT DISTINCT d.descripcion AS depto, c.anio, c.id, c.id_tipoevento, c.semana_epidemiologica, c.id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN departamento AS d
               ON c.id_depto = d.id
              """).df()


consultaSQL = """
               SELECT depto, SUM(cantidad) AS cantCasos
               FROM deptosConCasos
               WHERE anio = 2020
               GROUP BY depto, cantidad
               ORDER BY cantCasos DESC
              """              

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# g. Listar el promedio de cantidad de casos por provincia y año.

deptosConCasos = dd.sql("""
               SELECT DISTINCT d.descripcion AS depto, c.anio, c.id, c.id_tipoevento, c.semana_epidemiologica, c.id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN departamento AS d
               ON c.id_depto = d.id
              """).df()
              
provinciaCasos = dd.sql("""
               SELECT DISTINCT d.id_provincia AS provincia, dc.anio, dc.id, dc.id_tipoevento, dc.semana_epidemiologica, dc.id_grupoetario, dc.cantidad
               FROM deptosConCasos AS dc
               INNER JOIN departamento AS d
               ON dc.depto = d.descripcion
              """).df()
              

consultaSQL = """
               SELECT provincia, anio, AVG(cantidad) AS promedioCasos
               FROM provinciaCasos
               GROUP BY provincia, anio
               ORDER BY provincia, anio
              """ 

dataframeResultado = dd.sql(consultaSQL).df()              

# %%
# h. Listar, para cada provincia y año, cuáles fueron los departamentos que más
# cantidad de casos tuvieron.

deptosConCasos = dd.sql("""
               SELECT DISTINCT d.descripcion AS depto, c.anio, c.id, c.id_tipoevento, c.semana_epidemiologica, c.id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN departamento AS d
               ON c.id_depto = d.id
              """).df()
              
provinciaCasos = dd.sql("""
               SELECT DISTINCT d.id_provincia AS provincia, dc.anio, dc.id, dc.id_tipoevento, dc.semana_epidemiologica, dc.id_grupoetario, dc.cantidad
               FROM deptosConCasos AS dc
               INNER JOIN departamento AS d
               ON dc.depto = d.descripcion
              """).df()              

consultaSQL = """
               SELECT provincia, anio, SUM(cantidad) AS cantCasos
               FROM provinciaCasos
               GROUP BY provincia, anio
               ORDER BY cantCasos DESC
              """ 

dataframeResultado = dd.sql(consultaSQL).df()   

# %%
# i. Mostrar la cantidad de casos total, máxima, mínima y promedio que tuvo la
# provincia de Buenos Aires en el año 2019.

deptosConCasos = dd.sql("""
               SELECT DISTINCT d.descripcion AS depto, c.anio, c.id, c.id_tipoevento, c.semana_epidemiologica, c.id_grupoetario, c.cantidad
               FROM casos AS c
               JOIN departamento AS d
               ON c.id_depto = d.id
              """).df()
              
provinciaCasos = dd.sql("""
               SELECT DISTINCT d.id_provincia, dc.anio, dc.id, dc.id_tipoevento, dc.semana_epidemiologica, dc.id_grupoetario, dc.cantidad
               FROM deptosConCasos AS dc
               JOIN departamento AS d
               ON dc.depto = d.descripcion
              """).df()              

consultaSQL = dd.sql("""
               SELECT pc.anio, pc.id_provincia, p.descripcion AS nombre_provincia, MAX(cantidad) AS maxCant, MIN(cantidad) AS minCant, AVG(cantidad) AS promCant
               FROM provinciaCasos AS pc
               INNER JOIN provincia AS p
               ON pc.id_provincia = p.id
               GROUP BY id_provincia, nombre_provincia, anio
              """).df()
              
consultaSQL = """
               SELECT *
               FROM datosProvincias
               WHERE anio = 2019
                   AND nombre_provincia = 'Buenos Aires'
              """               

dataframeResultado = dd.sql(consultaSQL).df()   

# %%
# j. Misma consulta que el ítem anterior, pero sólo para aquellos casos en que la
# cantidad total es mayor a 1000 casos.

deptosConCasos = dd.sql("""
               SELECT DISTINCT d.descripcion AS depto, c.anio, c.id, c.id_tipoevento, c.semana_epidemiologica, c.id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN departamento AS d
               ON c.id_depto = d.id
              """).df()
              
provinciaCasos = dd.sql("""
               SELECT DISTINCT d.id_provincia, dc.anio, dc.id, dc.id_tipoevento, dc.semana_epidemiologica, dc.id_grupoetario, dc.cantidad
               FROM deptosConCasos AS dc
               INNER JOIN departamento AS d
               ON dc.depto = d.descripcion
              """).df()              

datosProvincias = dd.sql("""
               SELECT pc.anio, pc.id_provincia, p.descripcion AS nombre_provincia, MAX(cantidad) AS maxCant, MIN(cantidad) AS minCant, AVG(cantidad) AS promCant, SUM(cantidad) AS canTotal
               FROM provinciaCasos AS pc
               INNER JOIN provincia AS p
               ON pc.id_provincia = p.id
               GROUP BY id_provincia, nombre_provincia, anio
              """).df()
              
consultaSQL = """
               SELECT *
               FROM datosProvincias
               WHERE canTotal > 1000
              """               

dataframeResultado = dd.sql(consultaSQL).df()   

# %%
# k. Listar los nombres de departamento (y nombre de provincia) que tienen
# mediciones tanto para el año 2019 como para el año 2020. Para cada uno de
# ellos devolver la cantidad de casos promedio. Ordenar por nombre de
# provincia (ascendente) y luego por nombre de departamento (ascendente).

deptosProvincia = dd.sql("""
               SELECT DISTINCT d.descripcion AS depto, p.descripcion AS provincia, d.id AS id_depto
               FROM departamento AS d
               INNER JOIN provincia AS p
               ON d.id_provincia = p.id 
              """).df()



              
deptosProvinciaCasos = dd.sql("""
               SELECT DISTINCT dp.depto, dp.id_depto, dp.provincia, c.anio, c.id, c.id_tipoevento, c.semana_epidemiologica, c.id_grupoetario, c.cantidad
               FROM casos AS c
               INNER JOIN deptosProvincia AS dp
               ON c.id_depto = dp.id_depto
              """).df()              

              
consultaSQL = """
               SELECT DISTINCT dpc.depto, dpc.provincia, AVG(c.cantidad) AS cantCasosProm
               FROM deptosProvinciaCasos AS dpc
               INNER JOIN casos AS c
               ON dpc.id_depto = c.id_depto
               WHERE dpc.anio = 2019 
                   AND c.anio = 2020
               GROUP BY dpc.depto, dpc.provincia
               ORDER BY dpc.provincia ASC, dpc.depto ASC
              """               

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
# l. Devolver una tabla que tenga los siguientes campos: descripción de tipo de
# evento, id_depto, nombre de departamento, id_provincia, nombre de
# provincia, total de casos 2019, total de casos 2020.

deptosProvincia = dd.sql("""
               SELECT DISTINCT d.id AS id_depto, d.descripcion AS depto, p.id AS id_provincia, p.descripcion AS provincia
               FROM departamento AS d
               INNER JOIN provincia AS p
               ON d.id_provincia = p.id 
              """).df()
              
casosConEvento = dd.sql("""
               SELECT DISTINCT te.descripcion AS tipoEvento, c.anio, c.id_depto, c.cantidad, 
               FROM casos AS c
               INNER JOIN tipoevento AS te
               ON c.id_tipoevento = te.id
              """).df()              

              
infoBuscada = dd.sql("""
               SELECT DISTINCT ce.tipoEvento, dp.id_depto, dp.depto, dp.id_provincia,  dp.provincia, ce.anio, SUM(ce.cantidad) AS totalCasos
               FROM deptosProvincia AS dp
               INNER JOIN casosConEvento AS ce
               ON dp.id_depto = ce.id_depto
               GROUP BY dp.depto, dp.provincia, ce.anio, ce.tipoEvento, dp.id_depto, dp.id_provincia
               ORDER BY dp.depto, ce.anio
              """).df()      

info2019 = dd.sql("""
               SELECT DISTINCT *
               FROM infoBuscada
               WHERE anio = 2019
              """).df()     
              
info2020 = dd.sql("""
               SELECT DISTINCT *
               FROM infoBuscada
               WHERE anio = 2020
              """).df()
              
consultaSQL = """
               SELECT DISTINCT i19.tipoEvento, i19.id_depto, i19.depto, i19.id_provincia,  dp.provincia, ce.anio, SUM(ce.cantidad)
               FROM deptosProvinciaCasos AS dpc
               WHERE dpc.anio = 2019 
                   OR dpc.anio = 2020
               GROUP BY depto, provincia
               ORDER BY provincia, depto
              """                             

dataframeResultado = dd.sql(consultaSQL).df() 

#%%===========================================================================
#E. Subconsultas (ALL, ANY)
# %%
#a. Devolver el departamento que tuvo la mayor cantidad de casos sin hacer uso de MAX, ORDER BY ni LIMIT.

cantCasosDepto = dd.sql("""
               SELECT DISTINCT id_depto, SUM(cantidad) AS cantCasos
               FROM casos
               GROUP BY id_depto
               ORDER BY id_depto
               """).df()
consultaSQL = """
               SELECT DISTINCT cd1.id_depto, cd1.cantCasos
               FROM cantCasosDepto AS cd1
                   WHERE cd1.cantCasos >= ALL(
                       SELECT cd2.cantCasos
                       FROM cantCasosDepto AS cd2
                       )
              """                             

dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#b. Devolver los tipo de evento que tienen casos asociados. (Utilizando ALL o ANY).

consultaSQL = """
               SELECT DISTINCT te.descripcion
               FROM tipoevento AS te
                   WHERE te.id = ANY(
                       SELECT id_tipoEvento
                       FROM casos
                       )
                   """
        
dataframeResultado = dd.sql(consultaSQL).df()         

#%%===========================================================================
#F. Subconsultas (IN, NOT IN)
# %%
#a. Devolver los tipo de evento que tienen casos asociados (Utilizando IN, NOT IN).

consultaSQL = """
               SELECT DISTINCT te.descripcion
               FROM tipoevento AS te
                   WHERE te.id IN(
                       SELECT id_tipoEvento
                       FROM casos
                       )
                   """
        
dataframeResultado = dd.sql(consultaSQL).df()

# %%
#b. Devolver los tipo de evento que NO tienen casos asociados (Utilizando IN, NOT IN).

consultaSQL = """
               SELECT DISTINCT te.descripcion
               FROM tipoevento AS te
                   WHERE te.id NOT IN(
                       SELECT id_tipoEvento
                       FROM casos
                       )
                   """
        
dataframeResultado = dd.sql(consultaSQL).df()


#%%===========================================================================
#G. Subconsultas (EXISTS, NOT EXISTS)
# %%
#a. Devolver los tipo de evento que tienen casos asociados (Utilizando EXISTS, NOT EXISTS).

consultaSQL = """
               SELECT DISTINCT te.descripcion
               FROM tipoevento AS te
                   WHERE EXISTS(
                       SELECT id_tipoEvento
                       FROM casos
                       WHERE te.id = casos.id_tipoevento
                       )
                   """
        
dataframeResultado = dd.sql(consultaSQL).df()

# %%
#b. Devolver los tipo de evento que NO tienen casos asociados (Utilizando IN, NOT IN).

consultaSQL = """
               SELECT DISTINCT te.descripcion
               FROM tipoevento AS te
                   WHERE NOT EXISTS(
                       SELECT id_tipoEvento
                       FROM casos
                       WHERE te.id = casos.id_tipoevento
                       )
                   """
        
dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
#H. Subconsultas correlacionadas
# %%
#a. Listar las provincias que tienen una cantidad total de casos mayor al promedio de casos del país. Hacer el listado agrupado por año.


casosProvincia = dd.sql("""
               SELECT DISTINCT casos.anio, SUM(casos.cantidad) AS cantCasos, departamento.id_provincia
               FROM casos
               INNER JOIN departamento
               ON casos.id_depto = departamento.id
               GROUP BY departamento.id_provincia, casos.anio
               """).df()

consultaSQL = """
                SELECT cp1.id_provincia AS Provincia, cp1.anio, cp1.cantCasos
                FROM casosProvincia AS cp1
                WHERE cp1.cantCasos > (
                    SELECT AVG(cp2.cantCasos)
                    FROM casosProvincia AS cp2
                    WHERE cp2.anio = cp1.anio
                    )
                ORDER BY cp1.id_provincia, cp1.anio
              """


promediosPorAnio = dd.sql("""
               SELECT DISTINCT anio, AVG(cantidad) AS promCasos 
               FROM casos
               GROUP BY anio
               """).df()
               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#b. Por cada año, listar las provincias que tuvieron una cantidad total de casos mayor a la cantidad total de casos que la provincia de Corrientes.

casosIdProvincia = dd.sql("""
               SELECT DISTINCT casos.anio, SUM(casos.cantidad) AS cantCasos, departamento.id_provincia
               FROM casos
               INNER JOIN departamento
               ON casos.id_depto = departamento.id
               GROUP BY departamento.id_provincia, casos.anio
               ORDER BY departamento.id_provincia
               """).df()

casosProvincia = dd.sql("""
               SELECT DISTINCT c.*, p.descripcion AS provincia
               FROM casosIdProvincia AS c
               INNER JOIN provincia AS p
               ON c.id_provincia = p.id
               GROUP BY c.id_provincia, p.descripcion, c.anio, c.cantCasos 
               """).df()

consultaSQL = """
                SELECT cp1.id_provincia AS Provincia, cp1.anio, cp1.cantCasos
                FROM casosProvincia AS cp1
                WHERE cp1.cantCasos > (
                    SELECT cp2.cantCasos
                    FROM casosProvincia AS cp2
                    WHERE cp2.provincia = 'Corrientes'
                    )
                ORDER BY cp1.id_provincia, cp1.anio
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

#%%===========================================================================
#I. Más consultas sobre una tabla
# %%
#a. Listar los códigos de departamento y sus nombres, ordenados por estos últimos (sus nombres) de manera descendentes (de la Z a la A). En caso de empate, desempatar por código de departamento de manera ascendente.

consultaSQL = """
                SELECT id AS codigo_depto, descripcion AS nombre_depto
                FROM departamento
                ORDER BY nombre_depto DESC, codigo_depto ASC
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#b. Listar los registros de la tabla provincia cuyos nombres comiencen con la letra M.

consultaSQL = """
                SELECT DISTINCT *
                FROM provincia
                WHERE descripcion LIKE 'M%'
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#c. Listar los registros de la tabla provincia cuyos nombres comiencen con la letra S y su quinta letra sea una letra A.

consultaSQL = """
                SELECT DISTINCT *
                FROM provincia
                WHERE descripcion LIKE 'S___a%'
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#d. Listar los registros de la tabla provincia cuyos nombres terminan con la letra A.

consultaSQL = """
                SELECT DISTINCT *
                FROM provincia
                WHERE descripcion LIKE '%a'
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#e. Listar los registros de la tabla provincia cuyos nombres tengan exactamente 5 letras.

consultaSQL = """
                SELECT DISTINCT *
                FROM provincia
                WHERE descripcion LIKE '_____'
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#f. Listar los registros de la tabla provincia cuyos nombres tengan ”do” en alguna parte de su nombre.

consultaSQL = """
                SELECT DISTINCT *
                FROM provincia
                WHERE (descripcion LIKE 'do%' 
                       OR descripcion LIKE '%do%' 
                       OR descripcion LIKE '%do' 
                       )
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#g. Listar los registros de la tabla provincia cuyos nombres tengan ”do” en alguna parte de su nombre y su código sea menor a 30.

consultaSQL = """
                SELECT DISTINCT *
                FROM provincia
                WHERE ((descripcion LIKE 'do%' 
                       OR descripcion LIKE '%do%' 
                       OR descripcion LIKE '%do' 
                       ) AND (id < 30))
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#h. Listar los registros de la tabla departamento cuyos nombres tengan ”san” en alguna parte de su nombre. Listar sólo id y descripcion. Utilizar los siguientes alias para las columnas: codigo_depto y nombre_depto, respectivamente. El resultado debe estar ordenado por sus nombres de manera descendentes (de la Z a la A).

consultaSQL = """
                SELECT DISTINCT id AS codigo_depto, descripcion AS nombre_depto
                FROM departamento
                WHERE (descripcion LIKE 'San%' 
                       OR descripcion LIKE '%San%' 
                       OR descripcion LIKE '%San' 
                       )
                ORDER BY nombre_depto DESC
              """

               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#i. Devolver aquellos casos de las provincias cuyo nombre terminen con la letra a y el campo cantidad supere 10. Mostrar: nombre de provincia, nombre de departamento, año, semana epidemiológica, descripción de grupo etario y cantidad. Ordenar el resultado por la cantidad (descendente), luego por el nombre de la provincia (ascendente), nombre del departamento (ascendente), año (ascendente) y la descripción del grupo etario (ascendente).

deptosProvincia = dd.sql("""
                SELECT DISTINCT p.descripcion AS nombre_provincia, d.id AS codigo_depto, d.descripcion AS nombre_depto 
                FROM departamento AS d
                INNER JOIN provincia AS p
                ON d.id_provincia = p.id
                WHERE p.descripcion LIKE '%a'
              """).df()
              
casosGrupoEtario =  dd.sql("""
                SELECT DISTINCT c.anio, c.semana_epidemiologica, c.id_depto, c.cantidad, ge.descripcion AS descGrupoEtario 
                FROM casos AS c
                INNER JOIN grupoetario AS ge
                ON c.id_grupoetario = ge.id
              """).df()             


consultaSQL = """
                SELECT DISTINCT dp.nombre_provincia, dp.nombre_depto, cge.anio, cge.semana_epidemiologica, cge.descGrupoEtario, cge.cantidad
                FROM casosGrupoEtario AS cge
                INNER JOIN deptosProvincia AS dp
                ON cge.id_depto = dp.codigo_depto
                WHERE cge.cantidad > 10
                ORDER BY cge.cantidad DESC, dp.nombre_provincia ASC, dp.nombre_depto ASC, cge.anio ASC, cge.descGrupoEtario ASC
              """
               
dataframeResultado = dd.sql(consultaSQL).df() 

# %%
#j. Ídem anterior, pero devolver sólo aquellas tuplas que tienen el máximo en el campo cantidad.

deptosProvincia = dd.sql("""
                SELECT DISTINCT p.descripcion AS nombre_provincia, d.id AS codigo_depto, d.descripcion AS nombre_depto 
                FROM departamento AS d
                INNER JOIN provincia AS p
                ON d.id_provincia = p.id
                WHERE p.descripcion LIKE '%a'
              """).df()
              
casosGrupoEtario =  dd.sql("""
                SELECT DISTINCT c.anio, c.semana_epidemiologica, c.id_depto, c.cantidad, ge.descripcion AS descGrupoEtario 
                FROM casos AS c
                INNER JOIN grupoetario AS ge
                ON c.id_grupoetario = ge.id
              """).df()             


info_obtenida = dd.sql("""
                SELECT DISTINCT dp.nombre_provincia, dp.nombre_depto, cge.anio, cge.semana_epidemiologica, cge.descGrupoEtario, cge.cantidad
                FROM casosGrupoEtario AS cge
                INNER JOIN deptosProvincia AS dp
                ON cge.id_depto = dp.codigo_depto
                ORDER BY cge.cantidad DESC, dp.nombre_provincia ASC, dp.nombre_depto ASC, cge.anio ASC, cge.descGrupoEtario ASC
              """).df()
              
consultaSQL = """
                SELECT DISTINCT i1.*
                FROM info_obtenida AS i1
                WHERE i1.cantidad = (
                     SELECT MAX(io2.cantidad)
                     FROM info_obtenida AS io2
                     )
              """              
               
dataframeResultado = dd.sql(consultaSQL).df()

#%%===========================================================================
#J. Reemplazos
# %%
#a. Listar los id y descripción de los departamentos. Estos últimos sin tildes y en orden alfabético.

consultaSQL = """
                SELECT id, 
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(
                                        REPLACE(
                                            REPLACE(
                                                REPLACE(
                                                    REPLACE(
                                                        REPLACE(descripcion, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'), 'Á', 'A'), 'É', 'E'), 'Í', 'I'), 'Ó', 'O'), 'Ú', 'U') AS descSinTildes
                FROM departamento
                ORDER BY descripcion
              """              
               
dataframeResultado = dd.sql(consultaSQL).df()

# %%
#b. Listar los nombres de provincia en mayúscula, sin tildes y en orden alfabético

consultaSQL = """
                SELECT UPPER(
                            REPLACE(
                                REPLACE(
                                    REPLACE(
                                        REPLACE(
                                            REPLACE(
                                                REPLACE(
                                                    REPLACE(
                                                        REPLACE(
                                                            REPLACE(
                                                                REPLACE(descripcion, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u'), 'Á', 'A'), 'É', 'E'), 'Í', 'I'), 'Ó', 'O'), 'Ú', 'U')) AS provSinTildeMayus
                FROM departamento
                ORDER BY descripcion
              """              
               
dataframeResultado = dd.sql(consultaSQL).df()


