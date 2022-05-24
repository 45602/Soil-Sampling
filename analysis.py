# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:22:37 2022

@author: User
"""
import pandas as pd
import networkx as nx


g = nx.read_adjlist("test.adjlist")

def findMetrics():
    df = pd.DataFrame(columns = ['Name', 'nodeECC', 'clusteringCOEF',
                                 'eccentricityCENT', 'degreeCent', 
                                 'closenessCENT', 'betweenessCENT',
                                 'eigenCENT'] )
    dfDC = nx.degree_centrality(g) 
    dfCC = nx.closeness_centrality(g)
    dfBC = nx.betweenness_centrality(g)
    dfEC = nx.eigenvector_centrality(g)
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
