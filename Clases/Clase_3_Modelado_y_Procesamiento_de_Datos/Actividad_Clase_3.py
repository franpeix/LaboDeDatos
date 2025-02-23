import numpy as np
import pandas as pn
empleado_01 = np.array([[20222333, 45, 2, 20000], [33456234, 40, 0, 25000], [45432345, 41, 1, 10000]])

#Actividad 1
def superanSalarioAtividad01(empleado, umbral):
    res = []
    for usuario in empleado:
        if (usuario[3] > umbral):
            res.append(usuario)
    return np.array(res)

print(superanSalarioAtividad01(empleado_01, 15000))


#Actividad 2
empleado_02 = np.array([[20222333, 45, 2, 20000], [33456234, 40, 0, 25000], [45432345, 41, 1, 10000], [43967304, 37, 0, 12000], [42236276, 36, 0, 18000]])

print(superanSalarioAtividad01(empleado_02, 15000))

#Actividad 3
empleado_03 = np.array([[20222333, 20000, 45, 2], [33456234, 25000, 40, 0], [45432345, 10000, 41, 1], [43967304, 12000, 37, 0], [42236276, 18000, 36, 0]])

def superanSalarioActividad03(empleado, umbral):
    res = []
    for usuario in empleado:
        if (usuario[1] > umbral):
            pos1 = usuario[2]
            pos2 = usuario[3]
            pos3 = usuario[1]
            usuario[3] = pos3
            usuario[1] = pos1
            usuario[2]= pos2
            res.append(usuario)
    return np.array(res)
    
print(superanSalarioActividad03(empleado_03, 15000))

#Actividad 4
empleado_04 = empleado_03.T
def superanSalarioActividad04(empleado, umbral):
    res = []
    empleado = empleado.T
    for usuario in empleado:
        if (usuario[1] > umbral):
            pos1 = usuario[2]
            pos2 = usuario[3]
            pos3 = usuario[1]
            usuario[3] = pos3
            usuario[1] = pos1
            usuario[2]= pos2
            res.append(usuario)
    return np.array(res)
print(superanSalarioActividad04(empleado_04, 15000))

#1)Como afecto a la programacion de la funcion cuando cambiaron levemente la matrz de empleado?
#     a) En el caso en que le agregaron mas filas
#     b)En el caso que le alteraron el orden de las columnas
    
# a)Al agregar filas, no hubo ningun problema con el codigo, es decir, se pudo ejecutar de manera efectiva sin necesidad de modificarlo.
# b)Aqui, hubo que modificar los criterios de comparacion de los ciclos dentro de nuestra condicion if, para que la comparacion de los umbrales sea realizada en la columna correspondiente.

# 2)Y cuando a empleado le cambiaron la forma de representar las matrices(de lista de filas a lista de columnas)?
# Para ello, se podria haber implementado la matriz inversa a la realizada (algo que con la bibilioteca numpy se puede realizar en una funcion de esta), y luego, dentro de la ejecucion de la funcion, pedirle al codigo que unicamente vuelva a realizar la transofrmacion de la matriz inversa, y asi poder hacer los mismos pasos realizado en la actividad anterior, sin modificar ninuna parte mas del codigo de la anterior actividad.

#     3)Cual es la ventaja, desde el punto de vista del usuario de la funcion, disponer de ella y no escribir directamente el codigo de la consulta dentro de su programa?
# Esto nos permite evaluar y remodelar de manera satisfactoria el codigo que estamos implementando, de tal forma que se vuelva mas dinamico el funcionamiento y la posible correcion de la misma.
    

