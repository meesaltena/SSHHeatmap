# Author: Mees Altena, 24-04-2020
# Licence: MIT 
import re
import folium
import ipinfo
import argparse
from sys import exit
from folium.plugins import HeatMap
from time import process_time
from collections import Counter

# Set ipinfo api key here if you're not using arguments.
key = ""

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--input",
                    default="failed_attempts.txt",
                    help="Input filepath of: grep \"authentication failure\| Failed password\" /var/log/auth.log > [filename]")
parser.add_argument("-t", "--threshold", 
                    default=50,
                    type=int,
                    help="Minimum number of attempts before an ip is included in the heatmap")
parser.add_argument("-o", "--output",
                    default="heatmap.html",
                    help="Filename of the heatmap output")
required = parser.add_argument_group('required arguments')
required.add_argument("-k", "--key",
                    default = key,
                    required = (key == ""),
                    metavar = "API_KEY",
                    help="ipinfo.io api key")
args = parser.parse_args()

ip_handler = ipinfo.getHandler(args.key)

def read_file_get_ips():
    pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    with open(args.input) as f:
        file = f.read()
        ips = pattern.findall(file)
        print(f"Read file {args.input} and got {len(ips)} login attempts.")
        return ips
    
def get_applicable_ips(ips):
    counts = Counter(ips).most_common()
    meet_minimum = [x[0] for x in counts if x[1] > args.threshold]
    print(f"No. of ips with at least {args.threshold} login attempts: {len(meet_minimum)}")
    return meet_minimum

def get_ip_coordinates(ips):
    try:
        start = process_time()
        batchresult = ip_handler.getBatchDetails(ips, batch_size=100).values()            
        coords =[x['loc'].split(',') for x in batchresult if 'loc' in x.keys()]
        print(f"Fetched {len(coords)}/{len(ips)} coordinates in {round(process_time() - start, 3)} seconds.")
        return coords
    except Exception as ex:
        print(ex)
        exit(1)
       
def generate_and_save_heatmap(coords):        
    m = folium.Map(tiles="OpenStreetMap", location=[20,10], zoom_start=2)
    # mess around with these values to change how the heatmap looks
    HeatMap(data = coords, radius=15, blur=20, max_zoom=2).add_to(m)
    m.save(args.output) 
    print(f"Done. heatmap saved as {args.output}")  

def main():    
    ips = read_file_get_ips()
    ips_count = get_applicable_ips(ips)
    coords = get_ip_coordinates(ips_count)
    generate_and_save_heatmap(coords)

main()
