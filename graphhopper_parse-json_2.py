import requests
import urllib.parse
#API Endpoints
route_url = "https://graphhopper.com/api/1/route?"

#Locations
loc1 = "Washington, D.C."
loc2 = "Baltimore, Maryland"

#API Key
key = "e9a338f2-9253-4dd4-9344-7b46fc1bd2ea"

#Geocoding Function
def geocoding (location, key):
      geocode_url = "https://graphhopper.com/api/1/geocode?"
      url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1",
      "key":key})
      replydata = requests.get(url)
      json_data = replydata.json()
      json_status = replydata.status_code

      if json_status == 200:
         json_data = requests.get(url).json()
         lat = json_data["hits"][0]["point"]["lat"]
         lng = json_data["hits"][0]["point"]["lng"]
         name = json_data["hits"][0]["name"]
         value = json_data["hits"][0]["osm_value"]

         #If country exists in returned request object
         if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
         else:
            country=""

         #If state exists in returned request object
         if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
         else:
            state=""

         #If country and state is not null
         if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
         #if only state is not null
         elif len(state) !=0: 
              new_loc = name + ", " + country
         #If both are null
         else:
            new_loc = name
         
         print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url) 
         
      else:
         lat="null"
         lng="null"

      return json_status,lat,lng

orig = geocoding(loc1, key)
print(orig)
dest = geocoding(loc2, key)
print(dest) 
