'''
==========================================
run:

from placeInfo import findRestaurant
restaurant_info = findRestaurant(lat, lng)

restaurant_info is a dict()
==========================================
'''


import googlemaps
import requests
import pandas as pd
import time
PLACE_API_KEY = 'AIzaSyAfxiZ36COzkAF__lM05Er6teR2fYMmZog'

def findNearBy(lat, lng, radius = 1000, PLACE_API_KEY = PLACE_API_KEY):
  url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&radius='+str(radius)+'&type=restaurant&language=zh-TW&key='+PLACE_API_KEY
  payload={}
  headers = {}
  response = requests.request("GET", url, headers=headers, data=payload)

  try:
    nextPageToken = response.json()["next_page_token"]
    ifNextPage = True
  except:
    ifNextPage = False
  results = response.json()['results']
  PLACE_INFO = [[results[x]['place_id'], results[x]['geometry']['location']['lat'], results[x]['geometry']['location']['lng']] for x in range(len(results))]

  while(ifNextPage):
    time.sleep(2)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&radius='+str(radius)+'&type=restaurant&language=zh-TW&key='+PLACE_API_KEY+'&pagetoken='+nextPageToken
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
      nextPageToken = response.json()["next_page_token"]
    except:
      ifNextPage = False
    results = response.json()['results']
    PLACE_INFO.extend([[results[x]['place_id'], results[x]['geometry']['location']['lat'], results[x]['geometry']['location']['lng']] for x in range(len(results))])

  return PLACE_INFO

def findDetail(place_id, lat, lng, PLACE_API_KEY = PLACE_API_KEY):
  url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id='+str(place_id)+'&language=zh-TW&key='+PLACE_API_KEY
  payload = {}
  headers = {}
  response = requests.request("GET", url, headers=headers, data=payload)
  results = response.json()['result']
  Address = results['formatted_address']
  Name = results['name']
  Open_hour =  results['opening_hours']['weekday_text']
  Review = results['reviews']

  d = dict()
  d['place_id'] = place_id
  d['lat'] = lat
  d['lng'] = lng
  d['address'] = Address
  d['open_hour'] = Open_hour
  d['review'] = Review

  return Name, d

def findRestaurant(lat, lng):
  places = findNearBy(lat, lng)
  restaurant_INFO = dict()
  for place_id, lat, lng in places:
    try:
      name, d = findDetail(place_id, lat, lng)
      restaurant_INFO[name] = d
      restaurant_INFO[name]['name'] = name
    except:
      pass
  return restaurant_INFO