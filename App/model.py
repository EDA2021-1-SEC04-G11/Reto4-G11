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

from DISClib.Algorithms.Graphs.dfs import pathTo
from folium.map import Icon
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
from DISClib.Algorithms.Sorting import shellsort as s
from DISClib.Algorithms.Graphs import bfs as b
from DISClib.DataStructures import adjlist as adj 
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as mt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bel
from DISClib.Utils import error as error
assert config
from ip2geotools.databases.noncommercial import DbIpCity
import ipapi
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
                    "cable":None,
                    "lista":None,
                    "graph": None
                    }

        analyzer['landing'] = m.newMap(numelements=14000,
                                     maptype='PROBING')
        analyzer['cable'] = m.newMap(numelements=14000,
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
            hola=hola[1:]
            
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



def add_cable(analyzer,service):
    
    artist_n=service["cable_name"].strip()

    artist = analyzer['cable']
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
    
    ma=folium.Map()
    
    valor = djk.Dijkstra(analyzer["connections"], paisn1)
    distancia_t =djk.distTo(valor, paisn2)
    ruta =djk.pathTo(valor, paisn2)
    #grafica
    for x in lt.iterator(ruta):
     

        if "*" in (x["vertexA"]):
            ht=x["vertexA"]
            ht=ht.split("*")
            
            nombre=ht[1]
            ht=ht[0]
            dato =m.get(analyzer["landing"],ht)
            valor=me.getValue(dato)
            pos1l=float(valor["elements"][0]["latitude"])
            pos1la=float(valor["elements"][0]["longitude"])
            folium.Marker(
                location=[pos1l,pos1la],
                popup=nombre
    
                ).add_to(ma)
        else:

                ht=x["vertexA"]
                ht=ht.split("-")
                nombre=ht[0]
                ht=ht[0]
                dato =m.get(analyzer["countries"],ht)
                valor=me.getValue(dato)
                pos1l=float(valor["elements"][0]["CapitalLatitude"])
                pos1la=float(valor["elements"][0]["CapitalLongitude"])
                folium.Marker(
                    location=[pos1l,pos1la],
                    popup=nombre
        
                    ).add_to(ma)


        
           

        if "*" in (x["vertexB"]):
            ht=x["vertexB"]
            ht=ht.split("*")
            nombre=ht[1]
            ht=ht[0]
            dato =m.get(analyzer["landing"],ht)
            valor=me.getValue(dato)
            pos2l=float(valor["elements"][0]["latitude"])
            pos2la=float(valor["elements"][0]["longitude"])
            folium.Marker(
                location=[pos2l,pos2la],
                popup=nombre
    
                ).add_to(ma)
        else:

            ht=x["vertexB"]
            ht=ht.split("-")
            nombre=ht[0]
            ht=ht[0]
            
            dato =m.get(analyzer["countries"],ht)
            

            valor=me.getValue(dato)
            pos2l=float(valor["elements"][0]["CapitalLatitude"])
            pos2la=float(valor["elements"][0]["CapitalLongitude"])
            folium.Marker(
                    location=[pos2l,pos2la],
                    popup=nombre
        
                    ).add_to(ma)
        aline=folium.PolyLine(locations=[(pos1l,pos1la),(pos2l,pos2la)],weight=2,color = 'blue')
        ma.add_child(aline)
        ma.save("Req3map.html")

        
            

    
    return (distancia_t, ruta)




    return None
#-------------------------------
# REQUERIMIENTO 4
#-------------------------------

def req4(analyzer):
   """
   Debe retornar el número de nodos, el costo total, conexión más larga, conexión más corta 
   edgeTo: key: Vértices, Valores: nodos a los que se conecta 

   """
   lis=[]
   v= '5779*Paddington*Australia-Japan Cable (AJC)'
   h = b.BreadhtFisrtSearch(analyzer["connections"],'10383*Iskele*Turcyos-2')
   
   
   grafo = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=50,
                                              comparefunction=compareStopIds)
   
   listacero=[]
   graph= analyzer["connections"]
   search = p.PrimMST(graph)
   vert=(search["distTo"])
   keys=m.keySet(vert)
   for x in lt.iterator(keys):
       dat=m.get(vert,x)
       if dat["value"] == 0.0:
           listacero.append(dat["key"])
   
   
   
   arbol=(search["edgeTo"])
   
   valor=m.valueSet(arbol)
   for x in lt.iterator(valor):
       if not (gr.containsVertex(grafo,x["vertexA"])):
           
           gr.insertVertex(grafo,x["vertexA"])
           lis.append(x["vertexA"])
           
       if not (gr.containsVertex(grafo,x["vertexB"])):
           gr.insertVertex(grafo,x["vertexB"])
           lis.append(x["vertexB"])
           
       gr.addEdge(grafo,x["vertexA"],x["vertexB"],x["weight"])
       gr.addEdge(grafo,x["vertexB"],x["vertexA"],x["weight"])

   peso=p.weightMST(graph,search)
   print("Peso total : "+str(peso))

   print("Numeros de nodos conectados : "+str(gr.numVertices(grafo)))
   print(len(lis))
   cont=0
   max=0
   
   conts = djk.Dijkstra(analyzer["connections"],("Liberia-LR"))
        
        
       
           
   for x in (lis):
                    if (gr.containsVertex(grafo,x)):
                        if djk.hasPathTo(conts, x):
                                        distancia_t =djk.pathTo(conts, (x))
                                        jf=lt.size(distancia_t)
                                        pjf=int(jf)
                                        
                                        
                                        if pjf > max :
                                            max=pjf
                                           
                                            importa=x
                                            grafoi=conts
                                          
                                           
                                    
                                    

   ma=folium.Map()


                            
   ruta=(djk.pathTo(grafoi, importa))
  
   for x in lt.iterator(ruta):
     

        if "*" in (x["vertexA"]):
            ht=x["vertexA"]
            ht=ht.split("*")
            
            nombre=ht[1]
            ht=ht[0]
            dato =m.get(analyzer["landing"],ht)
            valor=me.getValue(dato)
            pos1l=float(valor["elements"][0]["latitude"])
            pos1la=float(valor["elements"][0]["longitude"])
            folium.Marker(
                location=[pos1l,pos1la],
                popup=nombre
    
                ).add_to(ma)
        else:

                ht=x["vertexA"]
                ht=ht.split("-")
                nombre=ht[0]
                ht=ht[0]
                dato =m.get(analyzer["countries"],ht)
                valor=me.getValue(dato)
                pos1l=float(valor["elements"][0]["CapitalLatitude"])
                pos1la=float(valor["elements"][0]["CapitalLongitude"])
                folium.Marker(
                    location=[pos1l,pos1la],
                    popup=nombre
        
                    ).add_to(ma)


        
           

        if "*" in (x["vertexB"]):
            ht=x["vertexB"]
            ht=ht.split("*")
            nombre=ht[1]
            ht=ht[0]
            dato =m.get(analyzer["landing"],ht)
            valor=me.getValue(dato)
            pos2l=float(valor["elements"][0]["latitude"])
            pos2la=float(valor["elements"][0]["longitude"])
            folium.Marker(
                location=[pos2l,pos2la],
                popup=nombre
    
                ).add_to(ma)
        else:

            ht=x["vertexB"]
            ht=ht.split("-")
            nombre=ht[0]
            ht=ht[0]
            
            dato =m.get(analyzer["countries"],ht)
            

            valor=me.getValue(dato)
            pos2l=float(valor["elements"][0]["CapitalLatitude"])
            pos2la=float(valor["elements"][0]["CapitalLongitude"])
            folium.Marker(
                    location=[pos2l,pos2la],
                    popup=nombre
        
                    ).add_to(ma)
        aline=folium.PolyLine(locations=[(pos1l,pos1la),(pos2l,pos2la)],weight=2,color = 'blue')
        ma.add_child(aline)
        ma.save("Req4map.html")
   print(ruta)
   
   
      
#-------------------------------
# REQUERIMIENTO 5
#-------------------------------


def req5(analyzer, lp):
    lista=[]
    lis = lt.newList()
    listad=lt.newList()

    for x  in lt.iterator(analyzer["lista"]):
        if lp in x :
            vert=x
            lista.append(x)
            
            dato=x.split("*")
            dato=dato[0]
            va=m.get(analyzer["landing"],dato)
            da=me.getValue(va)
            name=(da["elements"][0]["name"])
            lt1=float(da["elements"][0]["latitude"])
            lpt1=float(da["elements"][0]["longitude"])
            ma=folium.Map()
            folium.CircleMarker(
                radius=(25),
                location=[lt1,lpt1],
                popup=name,
                color="#a83a32",
                fill_color="#a83a32"
                

    
                ).add_to(ma)
            
            hol=adj.adjacents(analyzer["connections"],x)
            for i in lt.iterator(hol):
                if lt.isPresent(lis, i) == 0:
                    lt.addLast(lis,i)
  
    for y in range(0,len(lista)):

         for x in lt.iterator(lis):
        
            peso=gr.getEdge(analyzer["connections"],lista[y],x)
            if peso is not None :
                dis=peso["weight"]
                peso=peso["vertexB"]
                
                if "*" in peso:
                    peso=peso.split("*")
                    peso=peso[0]
                    valor=m.get(analyzer["landing"],peso)
                    dato=me.getValue(valor)
                    peso=(dato["elements"][0]["name"])
                    lt2=float(dato["elements"][0]["latitude"])
                    lpt2=float(dato["elements"][0]["longitude"])
                    
                    folium.Marker(
                        location=[lt2,lpt2],
                        popup=peso

    
                        ).add_to(ma)
                    
                    aline=folium.PolyLine(locations=[(lt1,lpt1),(lt2,lpt2)],weight=2,color = 'blue')
                    ma.add_child(aline)
                
                


                    if lt.isPresent(listad, (peso,dis)) == 0:   
                        lt.addLast(listad,(peso,dis))

    s.sort(listad,cmpdistance)
    ma.save("Req5map.html")
    
    return (listad,lt.size(listad))
            
        

#-------------------------------
# REQUERIMIENTO 6
#-------------------------------

def req6(analyzer, pais, cable):
    lis=lt.newList()
    las=lt.newList()
    for y  in lt.iterator(analyzer["lista"]):
        if cable in y:
            cabled=y.split("*")
            cabled=cabled[0]
            valor=m.get(analyzer["landing"],cabled)
            dato=me.getValue(valor)
            lt2=(dato["elements"][0]["name"])
            if pais in lt2:
                lt.addLast(lis,y)
    for x in lt.iterator(lis):
        adya=gr.adjacents(analyzer["connections"],x)
        for y in lt.iterator(adya):
            if lt.isPresent(las, y) == 0:
                lt.addLast(las,y)
    anchodebanda=valor=m.get(analyzer["cable"],cable)
    anchodebanda=me.getValue(anchodebanda)
    anchodebanda=anchodebanda["elements"][0]["capacityTBPS"]
    for x in lt.iterator(las):
        if  ("*") in x:
            dato=x.split("*")
            dato=dato[0]
            valor=m.get(analyzer["landing"],dato)
            va=me.getValue(valor)
            pais=va["elements"][0]["name"] 
            pais=pais.split(",")
            pais=pais[1]
            pais=pais.replace(" ","")
            value=m.get(analyzer["countries"],pais)
            
            v=me.getValue(value)
            velo=v["elements"][0]["Internet users"]
            ancho=(float(anchodebanda))/(float(velo))
            print(pais, ancho)

            
#-------------------------------
# REQUERIMIENTO 7
#-------------------------------

def req7(analyzer,ip_1,ip_2):
    # Se utiliza la librería y encuentra países 
    country_1 = ipapi.location(ip=ip_1,output='country_name')
    country_2 = ipapi.location(ip=ip_2,output='country_name')
    print(req3(analyzer,country_1,country_2))

   

    
    
                

            

    
    


            

                



    
            

    

                

               
                
                
                
            


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

def cmpdistance(route1,route2):
    return (float(route1[1])) > (float(route2[1]))

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
