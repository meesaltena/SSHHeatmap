# SSHHeatmap
Generates a heatmap of IPs that made failed SSH login attempts on linux systems, using /var/log/auth.log to get failed attempts. Uses the ipinfo.io library to fetch the IP address coordinates, and folium to generate the heatmap.

<img src="https://i.imgur.com/ZNoACD0.png"></img>

## Dependencies
- Python >3.5
- folium
- ipinfo
- requests

```bash
pip install -r requirements.txt
````


## Installation & Usage

Use wget (or curl, or git clone) to download the script.
```bash
wget https://raw.githubusercontent.com/meesaltena/SSHHeatmap/master/SSHHeatmap.py
```

Use grep to generate a text file that contains the logging entries of failed ssh connection attempts. Pattern matches login attempts with a password as well as an ssh key. 
```bash
grep "authentication failure\| Failed password" /var/log/auth.log > failed_attempts.txt
```
Or use /var/log/secure if /var/log/auth.log doesn't exist
```bash
grep "authentication failure\| Failed password" /var/log/secure > failed_attempts.txt
```
Get a free [ipinfo](https://ipinfo.io/) api key.

Run the script, passing the required ipinfo api key. You can run it without arguments buy setting the key manually.

```bash
python SSHHeatmap.py -k API_KEY
```

You can pass the following optional arguments:

```bash
python SSHHeatmap.py [-h] [-i INPUT] [-t THRESHOLD] [-o OUTPUT] -k API_KEY
```
 
- -i INPUT, --input INPUT: 
  - Input filepath of: grep "authentication failure\| Failed password" /var/log/auth.log > [filename] (default: failed_attempts.txt)
- -t THRESHOLD, --threshold THRESHOLD:
  - Minimum number of attempts before an ip is included in the heatmap (default: 50)
- -o OUTPUT, --output OUTPUT:
  - Filename of the heatmap output (default: heatmap.html)

Open the generated heatmap HTML file in a browser.

## Possible improvements
- use local geoip database for location lookup instead of ipinfo api call
- add legend to folium map

## License
[MIT](https://choosealicense.com/licenses/mit/)
