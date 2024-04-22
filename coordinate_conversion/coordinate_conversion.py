import math
import time


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    Args:
        lat1 (float): latitude of the first point
        lon1 (float): longitude of the first point
        lat2 (float): latitude of the second point
        lon2 (float): longitude of the second point
    Returns:
        float: distance between the two points in meters
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

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

    return round(distance, 2)


def set_coords(mics):
    """
    Sets the mic coordinates in the x, y plane (meters)
    Args:
        mics (list): dictionaries with the keys "latitude" and "longitude"
    Returns:
        list: same list as args but with added keys "x" and "y"

    """

    # First mic is assusmed to be the origin
    mics[0]["x"] = 0
    mics[0]["y"] = 0

    for mic in mics[1:]:
        mic["x"] = haversine(
            mics[0]["latitude"],
            mic["longitude"],
            mic["latitude"],
            mic["longitude"])
        if mics[0]["latitude"] > mic["latitude"]:
            mic["x"] = -mic["x"]
        mic["y"] = haversine(
            mic["latitude"],
            mics[0]["longitude"],
            mic["latitude"],
            mic["longitude"])
        if mics[0]["longitude"] > mic["longitude"]:
            mic["y"] = -mic["y"]

    return mics


def get_lat_long(mic, x, y):
    """
    Get the latitude and longitude of a point in the x, y plane
    Args:
        mic (dict): dictionary of the mic with coord (0, 0) in the x, y plane 
        x (float): x coordinate of the point
        y (float): y coordinate of the point
    Returns:
        tuple: latitude and longitude of the point
    """

    # May change depending on the accuracy needed
    ACCURACY = 1
    step_lat = 0.0000001
    step_long = 0.0000001

    if x < 0:
        step_lat = -step_lat
    if y < 0:
        step_long = -step_long

    # First mic is assusmed to be the origin, based on set_coords function
    curr_pos = {
        "latitude": mic["latitude"],
        "longitude": mic["longitude"],
        "x": 0,
        "y": 0}
    while True:
        if abs(curr_pos["x"] - x) > ACCURACY:
            curr_pos["latitude"] += step_lat
        if abs(curr_pos["y"] - y) > ACCURACY:
            curr_pos["longitude"] += step_long

        curr_pos = set_coords([mics[0], curr_pos])[1]

        if abs(
                curr_pos["x"] -
                x) <= ACCURACY and abs(
                curr_pos["y"] -
                y) <= ACCURACY:
            return curr_pos["latitude"], curr_pos["longitude"]


if __name__ == "__main__":
    # TODO: Implement with JSON file
    mics = [
        {"name": "Mic1",
         "latitude": 47.80706954562163,
         "longitude": 107.52836260177818},
        {"name": "Mic2",
         "latitude": 47.80918748769113,
         "longitude": 107.53115401209999},
    ]
    print(set_coords(mics))
    start_time = time.time()
    print("LAT_LONG: ", get_lat_long(mics[0], 208.46 / 2, 235.5/ 2))
    print("--- %s seconds ---" % (time.time() - start_time))
