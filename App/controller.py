﻿"""
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
        service["cable_length"] = service["cable_length"].replace(" km","")
        
        if service['cable_length'] == 'n.a.':
            service['cable_length'] = 0
    
        model.cargar_grafos(analyzer, service)
    
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
    return model.req1(cont,lp1,lp2)


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