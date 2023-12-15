# Author: Mees Altena, 24-04-2020
# Licence: MIT 
import re
import folium
from folium.plugins import HeatMap
import ipinfo
import sys
import time
from collections import Counter

# ipinfo api key here if you're not using sys arguments.
api_key = ""

# Filename of the txt with the output of: grep "authentication failure\| Failed password" /var/log/auth.log > failed_attempts.txt
try:
    filename = sys.argv[1]
except IndexError:
    if(api_key == ""):
        print("Usage: SSHHeatmap.py <source_filename> <api key> <attempts_threshold> <heatmap_filename>")
        print("To run SSHHeatmap without arguments, manually set an api key.")
        quit()
    filename = "failed_attempts.txt"
    pass

try:
    api_key = sys.argv[2]
except IndexError:
    if(api_key == ""):
        raise IndexError("API key not found. Please pass your ipinfo.io api key as the second argument, or set it manually.")

try:
    min_attempts = int(sys.argv[3])
except IndexError:
    min_attempts = 30
    pass    

try:
    heatmap_filename = sys.argv[4]
except IndexError:
    heatmap_filename = 'heatmap.html'
    pass

ip_handler = ipinfo.getHandler(api_key)

def read_file_get_ips(filename):
    pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    with open(filename) as f:
        file = f.read()
        ips = pattern.findall(file)

        print(f"Read file {filename} and got {len(ips)} login attempts.")
        return ips
    
def get_applicable_ips(ips):
    counts = Counter(ips).most_common()
    meet_minimum = [x[0] for x in counts if x[1] > min_attempts]
    print(f"No. of ips with at least {min_attempts} login attempts: {len(meet_minimum)}")
    return meet_minimum

def get_ip_coordinates(ips):
    try:
        start = time.process_time()
        batchDetails = ip_handler.getBatchDetails(ips, batch_size=100).values()
        coords =[x['loc'].split(',') for x in batchDetails if 'loc' in x.keys()]
        print(f"Fetched {len(coords)}/{len(ips)} coordinates in {round(time.process_time() - start, 3)} seconds.")
    except Exception as ex:
        print(ex)
         
    return coords       

def generate_and_save_heatmap(coords):        
    m = folium.Map(tiles="OpenStreetMap", location=[20,10], zoom_start=2)
    # mess around with these values to change how the heatmap looks
    HeatMap(data = coords, radius=15, blur=20, max_zoom=2).add_to(m)
    m.save(heatmap_filename) 
    print(f"Done. heatmap saved as {heatmap_filename}")  

def main():    
    ips = read_file_get_ips(filename)
    ips_count = get_applicable_ips(ips)
    coords = get_ip_coordinates(ips_count)
    generate_and_save_heatmap(coords)

main()
