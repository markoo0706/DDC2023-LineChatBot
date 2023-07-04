import geopy
import requests

def getTypeApi():
    r = requests.get("https://testapi.zeabur.app/result")
    recommend_list = json.loads(r.text)
    return recommend_list

def getType(lat, lng):
  recommend_list = getTypeApi()
  dist_list = [[geopy.distance.geodesic((lat, lng), (x['lat'], x['lng'])).km, x['recommend']] for x in recommend_list]
  type = min(dist)[1].split()
  return type[0][2:], type[1][2:], type[2][2:]
