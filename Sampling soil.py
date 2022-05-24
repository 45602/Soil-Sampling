# -*- coding: utf-8 -*-
"""
Created on Sun May  8 17:57:24 2022

@author: User
"""
from geopy.geocoders import Nominatim
import pandas as pd
import googlemaps
import numpy as np

#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)
#reading only needed data from csv file

#this part of code takes coordinates from final, finds cities and makes new csv file out of it 

csv_data = pd.read_csv('FINAL UAP 160 test.csv')
coordinates = pd.DataFrame(csv_data, columns=["Longitude", "Latitude"])
coordinates["City name"] = " "
geolocator = Nominatim(user_agent="geoapiExercises")
"""
for i in range(coordinates.shape[0]):
    string = "{},{}".format(coordinates["Latitude"].iloc[i], coordinates["Longitude"].iloc[i])
    location = geolocator.reverse(string);
    city = location.raw["address"]
    
    for key in city.keys():
        if key == "city_district":
            coordinates["City name"].iloc[i] = city["city_district"]
        elif key == "village":
            coordinates["City name"].iloc[i] = city["village"]
        elif key == "town":
            coordinates["City name"].iloc[i] = city["town"]
        elif key == "suburb":
            coordinates["City name"].iloc[i] = city["suburb"]
       
noviSadData = {"Longitude": 19.833549, "Latitude":45.267136, "City name": "Novi Sad"}
coordinates = coordinates.append(noviSadData, ignore_index=True)
coordinates.to_csv('novi.csv', encoding='UTF-8') 
coordinates.to_csv('noviReadable.csv', encoding='UTF-16') 
#utf 8 is not readable but i will use it when storing data
#utf 16 is readable but i cant use it for reading because read_csv doesnt allow it 
"""
print("Pronasao mesta na osnovu koordinata, sacuvao u novi i noviReadable")
#konvertovao si u imena mesta ali na osnovu njih ne mozes da trazis tako da trazis na osnovu koordinata
#sve koordinate
destinations = list()
csv_data = pd.read_csv("novi.csv")
for i in range(0, 160):
    destinations.append("{},{}".format(coordinates["Latitude"].iloc[i], coordinates["Longitude"].iloc[i]))

#metoda koja transformise to sto sam dobio u gmaps.distance_matrix, inace se dobijalo nesto skrnavo
#"{'destination_addresses': ['Zagubica, Serbia'], 'origin_addresses': ['Novi Sad, Serbia'], 'rows': 
    #[{'elements': 
        #[{'distance': {'text': '264 km', 'value': 264227}, 'duration': {'text': '3 hours 36 mins', 'value': 12943}, 'status': 'OK'}]}], 'status': 'OK'}"
def transformData(distanceDF):
    #destination_address = distanceDF.get('destination_addresses')[0] #kod iloca, pisi [] umesto ()
    #origin_address = distanceDF.get('origin_addresses')[0]
    rows = distanceDF.get('rows')[0].get('elements') 
    if('distance' not  in rows[0]):
        distance = 0
        duration = 0
    else:
        distance = rows[0].get('distance').get('text')
        duration = rows[0].get('duration').get('text')
    #pristupas koloni rows, ona je tipa lista, pristupas nultom elementu liste to 0 ne radi nista, distance matrix 
    #vraca listu od jednog elementa i onda u toj listi pristupas vrednostima -> elements   
    #df = {"destination_address": destination_address, "origin_address":origin_address, "distance and duration":distance + ", " + duration}
    df = str(distance) + "," + str(duration) 
    return df 


#matrix filled with data

def fillTheMatrix():
    dm = np.empty((161,161), dtype=np.dtype('U100'))
    #make first row and first column, initially with coordinates
    for i in range(0, 10):
        dm[0][i+1] = destinations[i]
        dm[i+1][0] = destinations[i]

    #fill the rest
    for i in range(1, 10):
        for j in range(1, i):
            distanceDF = gmaps.distance_matrix(dm[0][j], dm[i][0])
            distance = transformData(distanceDF)
            dm[i][j] = distance
            dm[j][i] = distance
    
    #overwrite the first row for good looks
    for i in range(0, 10):
        coordinatesFormatted = "{},{}".format(coordinates["Latitude"].iloc[i], coordinates["Longitude"].iloc[i])
        location = geolocator.reverse(coordinatesFormatted, language = "en-US");
        string = str(location).split(",")
        
        dm[0][i+1] = string[0] + ", " + string[1]
        dm[i+1][0] = string[0] + ", " + string[1]
        
    return dm

#converted matrix into dataframe just so i can print it normally
def convertMatrixForPrint(matrix):
    #print(matrix)
    mdf = pd.DataFrame(matrix)
    mdf.to_csv('matrixTEST.csv', encoding = "UTF-8") 
    np.savetxt('matrixFormat.txt', matrix, fmt='%s')

# = fillTheMatrix()
#convertMatrixForPrint(dm)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



