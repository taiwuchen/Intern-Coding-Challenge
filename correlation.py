import csv
import json
import math

# Haversine formula to calculate distance between two points in meters
def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    diff_lon = lon2 - lon1
    diff_lat = lat2 - lat1
    chord_length_squared = math.sin(diff_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon/2)**2
    angular_distance = 2 * math.asin(math.sqrt(chord_length_squared))
    earth_radius = 6371000  # In meters
    return angular_distance * earth_radius

# Check if the coordinates are valid
def is_valid_coordinate(lat, lon):
    return -90 <= lat <= 90 and -180 <= lon <= 180

# Read Sensor 1 data (CSV)
valid_sensor1_data = []
with open('SensorData1.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        id_val = int(row['id'])
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        
        if is_valid_coordinate(lat, lon):
            valid_sensor1_data.append({
                'id': id_val,
                'latitude': lat,
                'longitude': lon
            })

# Read Sensor 2 data (JSON)
valid_sensor2_data = []
with open('SensorData2.json', 'r') as json_file:
    sensor2_data = json.load(json_file)
    for reading in sensor2_data:
        if is_valid_coordinate(reading['latitude'], reading['longitude']):
            valid_sensor2_data.append(reading)

# Find matching pairs within 100 meters
matches = {}
for s1 in valid_sensor1_data:
    min_distance = float('inf')
    closest_s2_id = None
    
    for s2 in valid_sensor2_data:
        distance = haversine(s1['latitude'], s1['longitude'], s2['latitude'], s2['longitude'])
        
        if distance < min_distance and distance <= 100:  # Make sure they are within 100-meter accuracy
            min_distance = distance
            closest_s2_id = s2['id']
    
    if closest_s2_id is not None:
        matches[str(s1['id'])] = closest_s2_id

# Write result to output file
with open('output.json', 'w') as outfile:
    json.dump(matches, outfile, indent=4)

print(f"Processing complete. Found {len(matches)} matching pairs.")