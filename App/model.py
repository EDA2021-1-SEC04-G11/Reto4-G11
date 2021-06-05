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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from haversine import haversine, Unit
import os 

import folium
from numpy import split
import pandas as pd 
import config
from haversine import haversine, Unit
import sys
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import prim as p 
from DISClib.Algorithms.Graphs import bfs as b
from DISClib.DataStructures import adjlist as adj 
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as mt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
sys.setrecursionlimit(2 ** 20)
# -----------------------------------------------------
# API del TAD Analyzer
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landing': None,
                    'connections': None,
                    'countries':None,
                    "lista":None
                    }

        analyzer['landing'] = m.newMap(numelements=14000,
                                     maptype='PROBING')
        analyzer['countries'] = m.newMap(numelements=500,
                                     maptype='PROBING')

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        analyzer["lista"] = lt.newList("ARRAY_LIST")
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# ==============================
# Funciones para Cargar 
# ==============================

def cargar_grafos(analyzer, service):
    
    origin_id = formatVertexorigin(analyzer,service)
    destination_id = formatVertexdestination(analyzer,service)
    arc = float(service["cable_length"])

    if not (gr.containsVertex(analyzer["connections"],origin_id)):
        gr.insertVertex(analyzer["connections"],origin_id)
        lt.addLast(analyzer["lista"],origin_id)
    if not (gr.containsVertex(analyzer["connections"],destination_id)):
        gr.insertVertex(analyzer["connections"],destination_id)
        lt.addLast(analyzer["lista"],destination_id)
    gr.addEdge(analyzer["connections"],origin_id,destination_id,arc)
    gr.addEdge(analyzer["connections"],destination_id,origin_id,arc)
    
 
def cargar_p(analyzer):
    for x  in lt.iterator(analyzer["lista"]):
        
        punto=x.split("*")
        punto=punto[0]
       
        for y in lt.iterator(analyzer["lista"]):
            punto2=y.split("*")
            punto2=punto[0]

            if punto == punto2 and x != y :
                gr.addEdge(analyzer["connections"],x,y,(0.1))
                gr.addEdge(analyzer["connections"],y,x,(0.1))

def connect_capital(analyzer):
    for x  in lt.iterator(analyzer["lista"]):
    
        punto=x.split("*")
        punto=punto[0]
        
        dato =m.get(analyzer["landing"],punto)
        
        if dato is not None:
            valor=me.getValue(dato)
            paisciudad=(valor["elements"][0]["name"])
            latitudoriginal=(valor["elements"][0]["latitude"])
            longitudeoriginal=(valor["elements"][0]["longitude"])
            hola=paisciudad.split(",")
            hola=hola[-1]
            hola=hola.replace(" ","")
            value=m.get(analyzer["countries"],hola)
           
            if value is not None:
                va=me.getValue(value)
                
                latituddestino=(va["elements"][0]["CapitalLatitude"])
                longitudestino=(va["elements"][0]["CapitalLongitude"])
                nombre=(va["elements"][0]["CountryName"])+("-")+((va["elements"][0]["CountryCode"]))
                origen=(float(latitudoriginal),float(longitudeoriginal))
                destino=(float(latituddestino),float(longitudestino))
                longitud=haversine(origen,destino)
                
                if not (gr.containsVertex(analyzer["connections"],nombre)):
                    gr.insertVertex(analyzer["connections"],nombre)
                   

                gr.addEdge(analyzer["connections"],nombre,x,(longitud))
                gr.addEdge(analyzer["connections"],x,nombre,(longitud))
        

                
               

def add_country(analyzer,service):
    
    artist_n=service["CountryName"].strip()

    artist = analyzer['countries']
    moj= m.contains(artist,artist_n)
    if moj:
        valoactual = m.get(artist,artist_n) 
        valor = me.getValue(valoactual)
    else:
        m.put(artist,artist_n,lt.newList("ARRAY_LIST"))
        pays = m.get(artist,artist_n)
        valor= me.getValue(pays)
    
    lt.addLast(valor,service)

def add_landingPoint(analyzer,service):
   

    
    
    artist_n=service["landing_point_id"].strip()

    artist = analyzer['landing']
    moj= m.contains(artist,artist_n)
    if moj:
        valoactual = m.get(artist,artist_n) 
        valor = me.getValue(valoactual)
    else:
        m.put(artist,artist_n,lt.newList("ARRAY_LIST"))
        pays = m.get(artist,artist_n)
        valor= me.getValue(pays)
    
    lt.addLast(valor,service)
    
    

            
# Funciones de consulta
        
# ==============================
# Funciones de formato 
# ==============================

def formatVertexorigin(analyzer, service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['origin'] + '*'
    dato =m.get(analyzer["landing"],service['origin'])
    valor=me.getValue(dato)
    paisciudad=(valor["elements"][0]["name"])
    hola=paisciudad.split(",")
    hola=hola[0]
    hola=hola.replace(" ","")
    name= name + hola + "*"
    name = name + service['cable_name']
    
    return name

def formatVertexdestination(analyzer, service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['destination'] + '*'
    dato =m.get(analyzer["landing"],service['destination'])
    valor=me.getValue(dato)
    paisciudad=(valor["elements"][0]["name"])
    hola=paisciudad.split(",")
    hola=hola[0]
    hola=hola.replace(" ","")
    name= name + hola + "*"
    name = name + service['cable_name']
    
    return name

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer


#-------------------------------
# REQUERIMIENTO 1
#-------------------------------
def req1(analyzer,lp1,lp2):
    kosa = scc.KosarajuSCC(analyzer["connections"])
    lista1=[]
    lista2=[]
    for x  in lt.iterator(analyzer["lista"]):
        hola=x.split("*")
        hola=(hola[1])
        
        if hola == lp1:
            lista1.append(x)
            dato1= x
        if hola == lp2:
            lista2.append(x)
            dato2 = x
    pos=(dato1.split("*"))
    pos=pos[0]
    poss=dato2.split("*")
    poss=poss[0]
    
    dato =m.get(analyzer["landing"],pos)
    datoo=m.get(analyzer["landing"],poss)
    valor=me.getValue(dato)
    valorr=me.getValue(datoo)
    pos1l=float(valor["elements"][0]["latitude"])
    pos1la=float(valor["elements"][0]["longitude"])
    pos2l=float(valorr["elements"][0]["latitude"])
    pos2la=float(valorr["elements"][0]["longitude"])
    
    ma=folium.Map()
    folium.Marker(
        location=[pos1l,pos1la],
        popup=lp1
    
        ).add_to(ma)
    folium.Marker(
        location=[pos2l,pos2la],
        popup=lp2
    
    ).add_to(ma)

    aline=folium.PolyLine(locations=[(pos1l,pos1la),(pos2l,pos2la)],weight=2,color = 'blue')
    ma.add_child(aline)
    ma.save("Req1map.html")
    

    resul=False
    ram=len(lista1)
    if len(lista1) >= len(lista2):
        ram= len(lista2)
    
    for x in range(0,ram):
        var = scc.stronglyConnected(kosa, lista1[x], lista2[x])
        if var == True:
            resul=True
    number_scc = scc.connectedComponents(kosa)
    return resul, number_scc
    

#-------------------------------
# REQUERIMIENTO 2
#-------------------------------
def req2(analyzer):
    maxi=0
    dato=None
    lis = lt.newList()
    lista = m.keySet(analyzer["landing"])
    for x  in lt.iterator(lista):
        contador =0
        for y  in lt.iterator(analyzer["lista"]):
            z = y.split("*")
            z = z[0]
            if x == z:
                var = adj.adjacents(analyzer["connections"],y)
                
                num =lt.size(var)
                
                contador += num
                
        if contador > maxi:
            maxi = contador
            dato=x

    dator =m.get(analyzer["landing"],dato)
    valor=me.getValue(dator)
    pos1l=float(valor["elements"][0]["latitude"])
    pos1la=float(valor["elements"][0]["longitude"])
    lp1=(valor["elements"][0]["name"])
    ma=folium.Map()
    folium.Marker(
        location=[pos1l,pos1la],
        popup=lp1
    
        ).add_to(ma)

    for x  in lt.iterator(analyzer["lista"]):
        z = x.split("*")
        z = z[0]
        if z == dato:
            
            hol=adj.adjacents(analyzer["connections"],x)
            for i in lt.iterator(hol):
                
                i=i.split("*")
                i=i[0]
                
                if m.contains(analyzer["landing"], i):

                
                    datorr =m.get(analyzer["landing"],i)
                    valorr=me.getValue(datorr)

                
                pos2l=float(valorr["elements"][0]["latitude"])
                pos2la=float(valorr["elements"][0]["longitude"])
                lp2=(valorr["elements"][0]["name"])


                folium.Marker(
                    location=[pos2l,pos2la],
                    popup=lp2

    
                    ).add_to(ma)
                aline=folium.PolyLine(locations=[(pos1l,pos1la),(pos2l,pos2la)],weight=2,color = 'blue')
                ma.add_child(aline)


           
            if lt.isPresent(lis, x) == 0:

                

                lt.addLast(lis,x)
            

    
    
    print("Landing point mas conectado  " +str(dato))
    print("Total landing points cables conectado " +str(maxi))
    print("Total paises conectados " +str(lt.size(lis)))
    ma.save("Req2map.html")
    return dato

            
            
        
#-------------------------------
# REQUERIMIENTO 3
#-------------------------------
def req3(analyzer,lp1,lp2):
    pais1=m.get(analyzer["countries"],lp1)
    pais1=me.getValue(pais1)
    paisn1=(pais1["elements"][0]["CountryName"])+("-")+((pais1["elements"][0]["CountryCode"]))
    pais2=m.get(analyzer["countries"],lp2)
    pais2=me.getValue(pais2)
    paisn2=(pais2["elements"][0]["CountryName"])+("-")+((pais2["elements"][0]["CountryCode"]))
    print(paisn1)
    print(paisn2)
    
    valor = djk.Dijkstra(analyzer["connections"], paisn1)
    distancia_t =djk.distTo(valor, paisn2)
    ruta =djk.pathTo(valor, paisn2)
    
    return (distancia_t, ruta)




    return None
#-------------------------------
# REQUERIMIENTO 4
#-------------------------------

def req4(analyzer):
   v= '5779*Paddington*Australia-Japan Cable (AJC)'
   h = b.BreadhtFisrtSearch(analyzer["connections"],'5779*Paddington*Australia-Japan Cable (AJC)')
   
   hello = p.PrimMST(analyzer["connections"])
   prim = p.scan(analyzer["connections"], hello, v)
   cf = p.edgesMST(analyzer["connections"],hello)
   print(prim)

   
   
   
#-------------------------------
# REQUERIMIENTO 5
#-------------------------------




# ==============================
# Funciones de Comparacion
# ==============================
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

# ==============================
# Funciones de impresión 
# ==============================

def last_country(analyzer):
    keys = m.keySet(analyzer["countries"])
    key = lt.lastElement(keys)
    ult = m.get(analyzer["countries"],key)
    answer= ult["value"]["elements"][0]
    return answer

def first_lp(analyzer):
    keys = m.keySet(analyzer["landing"])
    key = lt.firstElement(keys)
    ult = m.get(analyzer["landing"],key)
    answer= ult["value"]["elements"][0]
    return answer

def countrySize(analyzer):
    """
    Número de libros en el catago
    """
    return m.size(analyzer['countries'])

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])
