import requests
import urllib.parse
#API Endpoints
route_url = "https://graphhopper.com/api/1/route?"

#API Key
key = "e9a338f2-9253-4dd4-9344-7b46fc1bd2ea"

def createNewFile(filename):
   open(filename, "x")

def appendToFile(file, content):
   f = open(file, "a")
   f.write(content)
   f.close()

#Geocoding Function
def geocoding (location, key):
      while location == "":
         location = input("Enter the location again: ")

      geocode_url = "https://graphhopper.com/api/1/geocode?"
      url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1",
      "key":key})
      replydata = requests.get(url)
      json_data = replydata.json()
      json_status = replydata.status_code

      if json_status == 200 and len(json_data["hits"]) !=0:
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
         
         #print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url) 

      else:
         lat="null"
         lng="null"
         new_loc=location
         if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " +
            json_data["message"]) 

      return json_status,lat,lng,new_loc

#User Input for Locations
while True:
 print("\n+++++++++++++++++++++++++++++++++++++++++++++")
 print("Vehicle profiles available on Graphhopper:")
 print("+++++++++++++++++++++++++++++++++++++++++++++")
 print("car, bike, foot")
 print("+++++++++++++++++++++++++++++++++++++++++++++")
 profile=["car", "bike", "foot"]
 vehicle = input("Enter a vehicle profile from the list above: ")
 if vehicle == "quit" or vehicle == "q":
   break
 elif vehicle in profile:
   vehicle = vehicle
 else:
   vehicle = "car"
   print("No valid vehicle profile was entered. Using the car profile.")
 loc1 = input("Starting Location: ")
 if loc1 == "quit" or loc1 == "q":
   break
 orig = geocoding(loc1, key)

# Prompt users for N amount of destinations
 num_destinations = int(input("Enter the number of destinations: "))
 destinations = []
 for i in range(num_destinations):
    loc = input(f"Destination {i + 1}: ")
    if loc in ["quit", "q"]:
        break
    dest = geocoding(loc, key)
    destinations.append(dest)

 # Enable saving directions to file
 saveToFile = input("Save directions to file? (y/n): ")
 while True:
   if saveToFile == "y" or saveToFile == "yes":
      saveToFile = True
      break
   elif saveToFile == "n" or saveToFile == "no":
      saveToFile = False
      break
   elif saveToFile == "quit" or saveToFile == "q":
      break
   else:
      saveToFile = input("Save directions to file? (y/n): ")
 if saveToFile == "quit" or saveToFile == "q":
   break
 
 # Prompt user for filename
 if saveToFile == True:
    while True: 
      fileName = input("Input desired filename: ")
      if fileName == "":
         fileName = input("File name cannot be empty: ")
      else:
         break


 print("=================================================")

 #If origin and destination is present
 if orig[0] == 200 and all(dest[0] == 200 for dest in destinations):
   points = f"&point={orig[1]}%2C{orig[2]}"
   
   # Create file to save routing instructions to
   if saveToFile and fileName:
      createNewFile(fileName)
   for dest in destinations:
        points += f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + points
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print(f"Routing API Status: {paths_status}\nRouting API URL:\n{paths_url}")
        print("=================================================")
        print(f"Directions from {orig[3]} to {', '.join(dest[3] for dest in destinations)} by {vehicle}")
        print("=================================================")
        if paths_status == 200:
            miles = paths_data["paths"][0]["distance"] / 1000 / 1.61
            km = paths_data["paths"][0]["distance"] / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print(f"Distance Traveled: {miles:.1f} miles / {km:.1f} km")
            print(f"Trip Duration: {hr:02d}:{min:02d}:{sec:02d}")
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                if saveToFile and fileName:
                    appendToFile(fileName, f"\n {path} ( {distance / 1000:.1f} km / {distance / 1000 / 1.61:.1f} miles )")
                    appendToFile(fileName, "\n =============================================")
                print(f"{path} ( {distance / 1000:.1f} km / {distance / 1000 / 1.61:.1f} miles )")
                print("=============================================")
        else:
            print(f"Error message: {paths_data['message']}")
            print("*************************************************")
 else:
    print(orig[0])
    for dest in destinations:
        print(dest[0])

