import math


# TODO: Implement with JSON file
mics = [
    {"name": "Mic1",
     "latitude": 58.40058,
     "longitude": 15.57636},
     {"name": "Mic2",
     "latitude": 58.40072,
     "longitude": 15.57634},
     {"name": "Mic3",
     "latitude": 58.40072,
     "longitude": 15.57613},
     {"name": "Mic4",
     "latitude": 58.40063,
     "longitude": 15.57621},
     {"name": "Mic5",
     "latitude": 58.40067,
     "longitude": 15.57647}
     ]


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Radius of Earth in meters
    R = 6371000

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    distance = 2 * R * math.asin(
        math.sqrt(
            math.sin(dlat / 2) ** 2 + 
                  math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                  ))

    
    return distance


def set_coords(mics):
    """
    Sets the the first microphone as the origin (0,0) and calculates the x and y coordinates for the other microphones

    mics: list of dictionaries with the keys "latitude" and "longitude"
    """
    mics[0]["x"] = 0
    mics[0]["y"] = 0
    
    for mic in mics[1:]:
        print(mic)
        mic["x"] = haversine(mic["longitude"], mics[0]["latitude"], mic["longitude"], mic["latitude"])
        if mics[0]["latitude"] > mic["latitude"]:
            mic["x"] = -mic["x"]
        mic["y"] = haversine(mics[0]["longitude"], mic["latitude"], mic["longitude"], mic["latitude"])
        if mics[0]["longitude"] > mic["longitude"]:
            mic["y"] = -mic["y"]
    

    return mics

print(set_coords(mics))

        
        










