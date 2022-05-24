# -*- coding: utf-8 -*-
"""
Created on Sun May 15 21:38:25 2022

@author: User
"""

import pandas as pd
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go

matrix = pd.read_csv("matrixCopy.csv")
listOfDestinations = pd.DataFrame(matrix, columns=['0'])
listOfDestinations = list(listOfDestinations['0'])
listOfDestinations.pop(0)

listOfEdges = []

for i in listOfDestinations:
    for j in listOfDestinations:
        if i!=j:
            listOfEdges.append((i,j))
            

g = nx.Graph(listOfEdges)

def findPos(string, listOfDestinations):
    for i in range(len(listOfDestinations)):
        if listOfDestinations[i] == string:
            return i
  
def addEdges(g):
    for i in range(0, len(listOfEdges)):
        start = listOfEdges[i][0] 
        end = listOfEdges[i][1]
        indexI = findPos(start, listOfDestinations)
        indexJ = findPos(end, listOfDestinations)
        if start!='214,  Kursumlijska Banja' and end!='214,  Kursumlijska Banja':
            w = matrix.iloc[indexI+1].iloc[indexJ+2].split(' ')[0]
            g.add_edge(start, end, weight = w)
        
        
def removeEdges(g):
    for i in range(2,161):
        print(i)
        for j in range(i+1,161):
            for k in range(j+1,161):
                pom1 = matrix.iloc[0].iloc[i]
                pom2 = matrix.iloc[0].iloc[j]
                pom3 = matrix.iloc[0].iloc[k]
                distance1 = float(matrix.iloc[i-1].iloc[j].split(' ')[0])
                distance2 = float(matrix.iloc[j-1].iloc[k].split(' ')[0])
                distance3 = float(matrix.iloc[k-1].iloc[i].split(' ')[0])
                if(distance1>distance2 and distance1>distance3):
                    if(abs(distance1-(distance2+distance3))<25):     
                        if g.has_edge(pom1,pom2):
                            g.remove_edge(pom1,pom2)
                elif(distance2>distance3 and distance2>distance1):
                    if(abs(distance2-(distance3+distance1))<25):        
                        if g.has_edge(pom2,pom3):
                                g.remove_edge(pom2,pom3)
                elif(distance3>distance1 and distance3>distance2):
                    if(abs(distance3-(distance1+distance2))<25): 
                        if g.has_edge(pom1,pom3):
                            g.remove_edge(pom1,pom3)


addEdges(g)
print('Number of edges in complete 160 nodes graph: ' + str(g.number_of_edges()))
removeEdges(g)     
print('Number of edges after removing transitive edges: ' + str(g.number_of_edges()))

#making a list so i can use it to visualize properly
listOfEdgesNew = []    
for e in g.edges():
    listOfEdgesNew.append(e)


def writeEdgesToFile(edges):
    with open(r'listaGrana.txt', 'w', encoding="utf-16") as fp:
         for item in edges:
             # write each item on a new line
             fp.write(str(item) + "\n")
         print('List of edges is written')

coordinates = pd.read_csv("noviCopy.csv")
def plotDots(coordinates):
    figure = px.scatter_mapbox(
        coordinates,
        lat = "Latitude",
        lon = "Longitude",
        hover_name = "City name",
        center = {"lat": 43.92441, "lon": 21.01117},
        width = 1000,
        height = 1000, 
        zoom = 7
    )  
    return figure

figure = plotDots(coordinates)
figure.update_layout(mapbox_style="open-street-map")

def drawEdges(edges, figure):
        
    for i in range(0, len(edges)):
        city1 = edges[i][0]
        city2 = edges[i][1]
        lat1 = str(coordinates.loc[coordinates['City name'] == city1]['Latitude']).split(' ')[4].split('\n')[0]
        long1 = str(coordinates.loc[coordinates['City name'] == city1]['Longitude']).split(' ')[4].split('\n')[0]
        lat2 = str(coordinates.loc[coordinates['City name'] == city2]['Latitude']).split(' ')[4].split('\n')[0]
        long2 = str(coordinates.loc[coordinates['City name'] == city2]['Longitude']).split(' ')[4].split('\n')[0]
        lons = [long1, long2]
        lats = [lat1, lat2]
        figure.add_trace(
            go.Scattermapbox(
                mode = "markers+lines",
                marker=dict(size=10, color='black'),
                name = "Udaljenost " + str(city1) + " i "+ str(city2) + " je " +
                    str(g.get_edge_data(city1, city2)['weight']) + "km",
                lon = lons,
                lat = lats))      
        
        
writeEdgesToFile(listOfEdgesNew)
drawEdges(listOfEdgesNew, figure)
figure.update_layout(height=1500, width=1600, autosize=False, mapbox_style="open-street-map")
figure.write_html('figura.html', auto_open=True)
nx.write_adjlist(g, "test.adjlist")

print("Starting analysis")
def findMetrics():
    df = pd.DataFrame(columns = ['Name', 'nodeECC', 'clusteringCOEF',
                                 'eccentricityCENT', 'degreeCent', 
                                 'closenessCENT', 'betweenessCENT',
                                 'eigenCENT'] )
    dfDC = nx.degree_centrality(g) 
    dfCC = nx.closeness_centrality(g)
    dfBC = nx.betweenness_centrality(g)
    dfEC = nx.eigenvector_centrality(g, max_iter = 500)
    for i in range(0, len(list(g.nodes()))):
        node_eccentricity = nx.eccentricity(g, list(g.nodes())[i])
        clustering_coefficent = nx.clustering(g, list(g.nodes())[i])
        eccentricity_centrality = 1/node_eccentricity
        degree_centrality = dfDC[list(g.nodes())[i]]
        closeness_centrality = dfCC[list(g.nodes())[i]]
        betweenness_centrality = dfBC[list(g.nodes())[i]]
        eigenvector_centrality = dfEC[list(g.nodes())[i]]
        df = df.append({'Name' : list(g.nodes)[i], 'nodeECC' : node_eccentricity, 
                        'clusteringCOEF' : clustering_coefficent, 'eccentricityCENT' : eccentricity_centrality,
                        'degreeCent': degree_centrality, 'closenessCENT' : closeness_centrality,
                        'betweenessCENT': betweenness_centrality,'eigenCENT': eigenvector_centrality },
                       ignore_index = True)
    return df

df = findMetrics()
df.to_csv('analysis.csv', encoding = "UTF-8")
print("Analysis is done, saved in analysis.csv")

print("Radius of a graph is: " + str(nx.radius(g)))
print("Diameter of a graph is: " + str(nx.diameter(g)))
clust_coefficients = nx.clustering(g)
avg_clust = sum(clust_coefficients.values()) / len(clust_coefficients)
print("Clustering coefficient of a graph is " + str(avg_clust))

