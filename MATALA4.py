#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 23:40:36 2021

@author: bnzr
"""

import requests


def calc_location(city, apikey):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={apikey}'
    response = requests.get(url).json()
    result = response['results']
    geometry_data = result[0]['geometry']
    return geometry_data['location']


apikey = " " #Attached to moodle
fhand = open('dests.txt', 'r', encoding='UTF-8')
origin_city = 'תל אביב'
output = dict()
origin = calc_location(origin_city, apikey)
for line in fhand.readlines():
    city_name = line.strip()
    try:
        dist = list()
        city = list()
        dest = calc_location(city_name, apikey)
        lat = dest['lat']
        lng = dest['lng']
        source_lat = origin['lat']
        source_lng = origin['lng']
        city.append(f'lat: {lat}')
        city.append(f'lng: {lng}')
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={source_lat},{source_lng}&destinations={lat},{lng}&key={apikey}'
        response = requests.get(url).json()
        rows = response['rows'][0]
        elements = rows['elements'][0]
        distance = elements['distance']
        distance_value = str(distance['value'] / 1000)
        dist.append(f'distance: {distance_value} km')
        duration = elements['duration']
        duration_txt = duration['text']
        dist.append(f'duration: {duration_txt}')
        city.append(dist)
        output[city_name] = tuple(city)
    except Exception as e:
        print(str(e))
        break
    finally:
        fhand.close()
print(str(output))
