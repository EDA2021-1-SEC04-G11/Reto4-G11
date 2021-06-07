"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import config as cf
from App import model
import csv
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    loadLP(analyzer)
    loadServices(analyzer)
    loadcountry(analyzer)
    model.cargar_p(analyzer)
  
    model.connect_capital(analyzer)
    

def loadServices(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = 'connections.csv'
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
  
    for service in input_file:
        
        service["origin"]=service.pop('\ufefforigin')
        service["cable_length"] = service["cable_length"].replace(" km","").replace(",","")
        
        if service['cable_length'] == 'n.a.':
            service['cable_length'] = 0
    
        model.cargar_grafos(analyzer, service)
        model.add_cable(analyzer,service)
    
    #model.addRouteConnections(analyzer)

    return analyzer

def loadLP(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    lpfile = 'landing_points.csv'
    lpfile = cf.data_dir + lpfile
    input_file = csv.DictReader(open(lpfile, encoding="utf-8"),
                                delimiter=",")
  
    for service in input_file:
        model.add_landingPoint(analyzer,service)
        
def loadcountry(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    country_file = 'countries.csv'
    country_file = cf.data_dir + country_file
    input_file = csv.DictReader(open(country_file, encoding="utf-8"),
                                delimiter=",")
  
    for service in input_file:
        model.add_country(analyzer,service)
        


def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def req1(cont,lp1,lp2):
    # Funciones Iniciales de tiempo y memoria 
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    # Función de carga 
    answer = model.req1(cont,lp1,lp2)
    # toma de memoria 
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print("Tiempo [ms]: ",delta_time)
    print("Memoria [kB]: ", delta_memory)
    return answer
def req2(cont):
    # Funciones Iniciales de tiempo y memoria 
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    # Función de carga 
    answer= model.req2(cont)
    # toma de memoria 
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print("Tiempo [ms]: ",delta_time)
    print("Memoria [kB]: ", delta_memory)
    return answer

def req3(analyzer,lp1,lp2):
    # Funciones Iniciales de tiempo y memoria 
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    # Función de carga 
    answer= model.req3(analyzer,lp1,lp2)
    # toma de memoria 
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print("Tiempo [ms]: ",delta_time)
    print("Memoria [kB]: ", delta_memory)
    return answer

def req4(cont):
    # Funciones Iniciales de tiempo y memoria 
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    # Función de carga 
    answer= model.req4(cont)
    # toma de memoria 
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print("Tiempo [ms]: ",delta_time)
    print("Memoria [kB]: ", delta_memory)
    return answer

def req5(cont, lp):
    # Funciones Iniciales de tiempo y memoria 
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    # Función de carga 
    answer= model.req5(cont,lp)
    # toma de memoria 
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print("Tiempo [ms]: ",delta_time)
    print("Memoria [kB]: ", delta_memory)
    return answer

def req6(cont, pais, cable):
    return (model.req6(cont,pais,cable))

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def countrySize(analyzer):
    """
    Número de libros en el catago
    """
    return model.countrySize(analyzer)

def last_country(analyzer):
    return model.last_country(analyzer)

def first_lp(analyzer):
    return model.first_lp(analyzer)

# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory