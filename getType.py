from geopy.distance import geodesic
import requests
import json

def getTypeApi():
    r = requests.get("https://testapi.zeabur.app/result")
    recommend_list = json.loads(r.text)
    return recommend_list

def getType(lat, lng):
  recommend_list = getTypeApi()
  dist_list = [[geodesic((lat, lng), (x['lat'], x['lng'])).km, x['recommend']] for x in recommend_list]
  txt = min(dist_list)[1]
  x = txt.replace(" ", "")
  resType1 = x[2:6]
  resType2 = x[8:12]
  resType3 = x[14:18]
  return resType1, resType2, resType3
