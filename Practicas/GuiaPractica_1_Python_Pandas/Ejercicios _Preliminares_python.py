##Ejercicios Preliminares python


#1) Una mañana ponés un billete en la vereda al lado del obelisco porteño. A partir
# de ahí, cada día vas y duplicás la cantidad de billetes, apilándolos prolijamente.
# ¿Cuánto tiempo pasa antes de que la pila de billetes sea más alta que el
# obelisco?
# Datos: espesor del billete: 0.11 mm, altura obelisco: 67.5 m.
def pilaMayorAObelisco(espesor_billete, altura_obelisco):
    dias: int = 1
    altura_pila = espesor_billete
    while altura_pila < altura_obelisco:
        altura_pila * 2
        dias += 1
    return dias
print(pilaMayorAObelisco(0.11, 67500))    

# 2)Usá una iteración sobre el string cadena para agregar la sílaba 'pa', 'pe', 'pi', 'po', o
# 'pu' según corresponda luego de cada vocal.
# Ejemplo:
# cadena = 'Casa'
# cadena_geringosa = ''
# for c in cadena:
#   COMPLETAR
# print(cadena_geringosa)
# # Geperipingoposopo
# Luego hacelo con un while en vez del for.
def modificarPalabra(palabra):
    palabraNueva = ''
    for letra in palabra:
        if (letra == 'A'):
            palabraNueva += 'ApA'
        elif (letra == 'E'):
            palabraNueva += 'EpE'
        elif (letra == 'I'):
            palabraNueva += 'IpI'
        elif (letra == 'O'):
            palabraNueva += 'OpO'
        elif (letra == 'U'):
            palabraNueva += 'UpU'
        elif (letra == 'a'):
            palabraNueva += 'apa'
        elif (letra == 'e'):
            palabraNueva += 'epe'
        elif (letra == 'i'):
            palabraNueva += 'ipi'
        elif (letra == 'o'):
            palabraNueva += 'opo'
        elif (letra == 'u'):
            palabraNueva += 'upu'
        else:
            palabraNueva += letra
    return palabraNueva
print (modificarPalabra('geringosa'))

def modificarPalabra2(palabra):
    palabraNueva = ''
    letra = palabra[0]
    while letra != ' ':
        if (letra == 'A'):
            palabraNueva += 'ApA'
        elif (letra == 'E'):
            palabraNueva += 'EpE'
        elif (letra == 'I'):
            palabraNueva += 'IpI'
        elif (letra == 'O'):
            palabraNueva += 'OpO'
        elif (letra == 'U'):
            palabraNueva += 'UpU'
        elif (letra == 'a'):
            palabraNueva += 'apa'
        elif (letra == 'e'):
            palabraNueva += 'epe'
        elif (letra == 'i'):
            palabraNueva += 'ipi'
        elif (letra == 'o'):
            palabraNueva += 'opo'
        elif (letra == 'u'):
            palabraNueva += 'upu'
        else:
            palabraNueva += letra
    return palabraNueva
print (modificarPalabra('geringosa'))

#3)Denir una función pertenece(lista, elem) que tome una lista y un
# elemento, y devuelva True si la lista tiene al elemento dado y False en caso
# contrario.
def pertenece(lista, elem):
    #return elem in lista
    res = False
    for i in range(0, len(lista) - 1, 1):
        if lista[i] == elem:
            res = True
    return res

# 4) Denir una función mas_larga(lista1, lista2) que tome dos listas y
# devuelva la más larga.
def mas_larga(lista1, lista2):
    if (len(lista1) >= len(lista2)):
        return lista1
    else:
        return lista2
    
# 5) Una pelota de goma es arrojada desde una altura de 100 metros y cada vez que
# toca el piso salta 3/5 de la altura desde la que cayó. Escribí un programa
# rebotes.py que imprima una tabla mostrando las alturas que alcanza en cada uno
# de sus primeros diez rebotes.
# def rebotesPelota(altura):
    
    
    
    
# 6)Denir la función mezclar(cadena1, cadena2) que tome dos strings y
# devuelva el resultado de intercalar elemento a elemento. Por ejemplo: si
# intercalamos Pepe con Jose daría PJeopsee. En el caso de Pepe con Josefa daría
# PJeopseefa.

def mezclar(cadena1, cadena2):
    palabraMezclada = ''
    palabraMasLarga = max(len(cadena1), len(cadena2))
    for i in range (0, palabraMasLarga, 1):
        if (i >= len(cadena1)):
            palabraMezclada += cadena2[i]
        elif (i >= len(cadena2)):
            palabraMezclada += cadena1[i]
        else:
            palabraMezclada += cadena1[i]
            palabraMezclada += cadena2[i]
    return palabraMezclada
print(mezclar('Pepe', 'Jose'))            

# 7)David solicitó un crédito a 30 años para comprar una vivienda, con una tasa fija
# nominal anual del 5%. Pidió $500000 al banco y acordó un pago mensual fijo de
# $2684,11.

# a. Escribir un programa que calcula el monto total que pagará David a lo
# largo de los años. Deberías obtener que en total paga $966279.6.
def pagarCredito(montoMes, anios):
    cantidadMeses = anios*12
    return cantidadMeses * montoMes
print(pagarCredito(2684.11, 30))    

# b. Supongamos que David adelanta pagos extra de $1000/mes durante los
# primeros 12 meses de la hipoteca. Modicá el programa para incorporar
# estos pagos extra y que imprima el monto total pagado junto con la
# cantidad de meses requeridos. Deberías obtener que el pago total es de
# $929965.62 en 342 meses.
# Datos iniciales
principal = 500000
annual_rate = 0.05
monthly_rate = annual_rate / 12
monthly_payment = 2684.11
extra_payment = 1000
total_paid = 0
months = 0

# Realizar pagos
while principal > 0:
    months += 1
    # Para los primeros 12 meses, se incluye el pago extra
    if months <= 12:
        principal = principal * (1 + monthly_rate) - (monthly_payment + extra_payment)
    else:
        principal = principal * (1 + monthly_rate) - monthly_payment
    
    # Acumulamos el pago total
    if principal < 0:
        total_paid += (monthly_payment + principal)
    else:
        total_paid += monthly_payment

# Resultados
print(f'Monto total pagado: ${total_paid:.2f}')
print(f'Meses requeridos: {months}')

def montoTasaFija(porcentaje, anios, monto_inicial):
    res = monto_inicial
    for i in range(1, anios, 1):
        agregar = monto_inicial * porcentaje
        res += agregar
    return res
print (montoTasaFija(0.05, 30, 500000))
def pagarCreditoPagosExtra(montoMes, anios):
    
    primerAnio = (montoMes+1000) * 12
    
    
    
print(pagarCreditoPagosExtra(2684.11, 30)) 

# c. ¿Cuánto pagaría David si agrega $1000 por mes durante cuatro años,
# comenzando en el sexto año de la hipoteca (es decir, luego de 5 años)?
# Modicá tu programa de forma que la información sobre pagos extras sea
# incorporada de manera versátil. Sugerimos utilizar los parámetros:
# pago_extra_monto, pago_extra_mes_comienzo, pago_extra_mes_fin.
def calcular_hipoteca(principal, annual_rate, monthly_payment, pago_extra_monto, pago_extra_mes_comienzo, pago_extra_mes_fin):
    monthly_rate = annual_rate / 12
    total_paid = 0
    months = 0

    while principal > 0:
        months += 1
        if pago_extra_mes_comienzo <= months <= pago_extra_mes_fin:
            principal = principal * (1 + monthly_rate) - (monthly_payment + pago_extra_monto)
        else:
            principal = principal * (1 + monthly_rate) - monthly_payment
        
        if principal < 0:
            total_paid += (monthly_payment + principal)
        else:
            total_paid += monthly_payment

    return total_paid, months

# Datos iniciales
principal = 500000
annual_rate = 0.05
monthly_payment = 2684.11
pago_extra_monto = 1000
pago_extra_mes_comienzo = 61  # Comienza en el mes 61 (después de 5 años)
pago_extra_mes_fin = 108      # Termina en el mes 108 (después de 4 años adicionales)

# Cálculo
total_paid, months = calcular_hipoteca(principal, annual_rate, monthly_payment, pago_extra_monto, pago_extra_mes_comienzo, pago_extra_mes_fin)

# Resultados
print(f'Monto total pagado: ${total_paid:.2f}')
print(f'Meses requeridos: {months}')

# 8)Construí una función traductor_geringoso(lista) que, a partir de una lista de
# palabras, devuelva un diccionario geringoso. Las claves del diccionario deben ser
# las palabras de la lista y los valores deben ser sus traducciones al geringoso.
# Por ejemplo, al tomar la lista ['banana', 'manzana', 'mandarina'] debe
# devolver {'banana': 'bapanapanapa', 'manzana': 'mapanzapanapa',
# 'mandarina': 'mapandaparipinapa'}.
def traductor_geringoso(lista):
    res = {}
    for palabra in lista:
        traduccion = ''
        for letra in palabra:
            if (letra == 'A'):
                traduccion += 'ApA'
            elif (letra == 'E'):
                traduccion += 'EpE'
            elif (letra == 'I'):
                traduccion += 'IpI'
            elif (letra == 'O'):
                traduccion += 'OpO'
            elif (letra == 'U'):
                traduccion += 'UpU'
            elif (letra == 'a'):
                traduccion += 'apa'
            elif (letra == 'e'):
                traduccion += 'epe'
            elif (letra == 'i'):
                traduccion += 'ipi'
            elif (letra == 'o'):
                traduccion += 'opo'
            elif (letra == 'u'):
                traduccion += 'upu'
            else:
                traduccion += letra
        res[palabra] = traduccion
    return res
print(traductor_geringoso(['banana', 'manzana', 'mandarina']))
           