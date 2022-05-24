# -*- coding: utf-8 -*-
"""
Created on Thu May 12 20:34:41 2022

@author: User
"""
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import networkx as nx
from transliterate import translit

matrix = pd.read_csv("matrix.csv")
listOfDestinations = pd.DataFrame(matrix, columns=['0'])
listOfDestinations = list(listOfDestinations['0'])

edges = {}
for i in listOfDestinations:
    edges = {key: {} for key in listOfDestinations}

def findAllEdges():
    edges = {}
    for i in listOfDestinations:
        edges = {key: {} for key in listOfDestinations}

    for i in range(1,161):
        miniDict = edges.get(matrix.iloc[0].iloc[i])
        for j in range(1,161):
            if '[matrix.iloc[j].iloc[0]]' not in miniDict.keys():
                edges[matrix.iloc[0].iloc[i]][matrix.iloc[j].iloc[1]] = [matrix.iloc[j].iloc[i]]
    
    return edges

def removeEdges(edges):
    edges = findAllEdges()
    for i in range(1,10):
        for j in range(1,10):
            for k in range(1, 10):
                if(k != i and k != j and i!=j):
                    site1 = matrix.iloc[i].iloc[1]
                    site2 = matrix.iloc[j].iloc[1]
                    site3 = matrix.iloc[k].iloc[1]
        
                    if(site2 in edges[site1].keys()):
                        del edges[site1][site2]
   
    return edges




#edges = removeEdges(edges)
newDF = pd.DataFrame(edges)
newDF.to_csv("izbaceneEdges.csv")
coordinates = pd.read_csv("noviCopy.csv")
def plotDots(df):
    fig = px.scatter_mapbox(
        df,
        lat = "Latitude",
        lon = "Longitude",
        hover_name = "City name",
        center = {"lat": 43.92441, "lon": 21.01117},
        width = 1000,
        height = 1000, 
        zoom = 7
    )  
    return fig

#fig2 = px.line_geo(df, locations="City name")
#fig3 = go.Figure(data=fig.data + fig2.data)
fig = plotDots(coordinates)
fig.update_layout(mapbox_style="open-street-map")
fig.write_html('figura.html', auto_open=True)

#fig2 = px.line_mapbox(us_cities, lat="lat", lon="lon", color="State", zoom=3, height=300)


        








