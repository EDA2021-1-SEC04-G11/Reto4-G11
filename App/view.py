"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
import threading
from App import controller
from DISClib.ADT import stack
from DISClib.ADT import list as lt
assert config


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Req 1: Identificar los clústers de información ")
    print("3- Req 2: Identificar puntos de conexión críticos de la red")
    print("4- Req 3: La ruta de menor distancia")
    print("5- Req 4: Identificar la infraestructura crítica de la red")
    print("6- Req 5: Análisis de fallas")
    print("7- Req 6: Los mejores canales para transmitir")
    print("8- Req 7: La mejor ruta de comunicaciones")
    print("8- Req 8: Graficando los grafos")
    
    
catalog = None


def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.init()

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
       
        cont = controller.init()
        answer = controller.loadData(cont)
        
        numvertex = controller.totalStops(cont)
        numedges = controller.totalConnections(cont)
        last_ct = controller.last_country(cont)
        total_countries = controller.countrySize(cont)
        first_lp = controller.first_lp(cont)
        
        print("Total de landing points:", numvertex)
        print("Total de conexiones entre landing-points", numedges)
        print("Total de países:", total_countries)
        print("Primer landing point:", first_lp)
        print("último país", last_ct)

    elif int(inputs[0]) == 2:
        print("RedondoBeach, VungTau, Songkhla")
        lp1 = input("Ingrese el nombre del landing point1: ")
        lp2= (input("Ingrese el nombre del landing point2: "))
       
        result = controller.req1(cont,lp1,lp2)
        print("Número de clústers presentes en la red:", result[1])
        print("Los dos lp se enceuntran en el mismo clúster:", result[0])
    elif int(inputs[0]) == 3:
        
        result=controller.req2(cont)
        
    elif int(inputs[0]) == 4:
        
        pais_A = input("Ingrese el país A:")
        pais_B = input("Ingrese el país B:")

        result = controller.req3(cont,pais_A,pais_B)
        print("Distancia Total: {} \n Ruta: {}".format(result[0],result[1]))
    elif int(inputs[0]) == 5:
        result=controller.req4(cont)
    elif int(inputs[0]) == 6:
        lp = input("Ingrese el landing point que le gustaría consultar")
        result = controller.req5(cont,lp)
        print("Lista de países afectados:\n{}".format(result[0]))
        print("Número de países {}".format(result[1]))
    elif int(inputs[0]) == 7:
        print("Probar con: \nCuba,ALBA-1")
        pais = input("Ingrese el pais: ")
        cable = input("Ingrese el cable: ")

        result = controller.req6(cont,pais,cable)

        
    elif int(inputs[0]) == 8:
        pass
    else:
        sys.exit(0)
sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()